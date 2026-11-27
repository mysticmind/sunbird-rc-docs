"""One-off migration of the live rc.sunbird.org GitBook site into this VitePress repo.

Usage: python3 scripts/migrate-from-gitbook.py <work_dir> <repo_root> [--fetch]
  --fetch  download llms.txt, every page's Markdown export and the OpenAPI specs into <work_dir> first
  work_dir then holds llms_.txt, raw/<page>.md and openapi/*.yaml

Rerun it only while GitBook is still being edited; after the switch, edit the Markdown here.
"""
import hashlib, html, json, re, shutil, subprocess, sys, time, urllib.parse, urllib.request
from pathlib import Path

LIVE, OUT = Path(sys.argv[1]), Path(sys.argv[2])
SITE = "https://rc.sunbird.org"


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read()


if "--fetch" in sys.argv:
    LIVE.mkdir(parents=True, exist_ok=True)
    llms = _get(SITE + "/llms.txt").decode()
    (LIVE / "llms_.txt").write_text(llms)
    for u in re.findall(r"\((https://rc\.sunbird\.org/[^)]+\.md)\)", llms):
        dest = LIVE / "raw" / u[len(SITE) + 1:]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(_get(u))
        time.sleep(0.2)
    (LIVE / "openapi").mkdir(exist_ok=True)
    for name in ("issue-api", "identity-api", "schema-api"):
        (LIVE / "openapi" / f"{name}.yaml").write_bytes(_get(
            f"https://raw.githubusercontent.com/Sunbird-RC/sunbird-rc-core/main/api-documentation/{name}.yaml"))
IMG_DIR = OUT / "public" / "images"
MEDIA_DIR = OUT / "public" / "media"
report = {"images": 0, "media": 0, "blocks": {}, "unhandled": []}

# ---------------------------------------------------------------- page list from llms.txt
pages, space = [], None
for line in (LIVE / "llms_.txt").read_text().splitlines():
    if line.startswith("## "):
        space = line[3:].strip()
        continue
    m = re.match(r"- \[(.+?)\]\((https://rc\.sunbird\.org/(.+?)\.md)\)(?::\s*(.*))?$", line)
    if m:
        pages.append(dict(space=space, title=m.group(1), path=m.group(3), desc=(m.group(4) or "").strip()))
# GitBook editors strike through a page title (~Title~) to mark a dead or placeholder page.
# Those pages hold only internal notes, so they are not migrated; they are listed for follow-up.
skipped = [p for p in pages if re.fullmatch(r"~.+~", p["title"])]
pages = [p for p in pages if p not in skipped]
for p in skipped:
    stale = OUT / (p["path"] + ".md")
    if stale.exists():
        stale.unlink()  # from an earlier run
# Pages whose content was moved by hand into the home page (index.md); edit it there, not on GitBook.
MERGED_INTO_HOME = {"learn/welcome-aboard"}
for p in [p for p in pages if p["path"] in MERGED_INTO_HOME]:
    stale = OUT / (p["path"] + ".md")
    if stale.exists():
        stale.unlink()
pages = [p for p in pages if p["path"] not in MERGED_INTO_HOME]
report["not_migrated"] = [f'{p["title"].strip("~")} ({p["path"]})' for p in skipped]
print(len(pages), "pages,", len(skipped), "placeholder pages skipped")


# ---------------------------------------------------------------- downloads
def fetch(url, dest_dir, kind):
    url = url.replace("&#x26;", "&").replace("&amp;", "&")
    parsed = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(urllib.parse.unquote(parsed.path))
    name = path.rsplit("/", 1)[-1] or "file"
    stem, _, ext = name.rpartition(".")
    if not stem:
        stem, ext = name, "png"
    stem = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "file"
    h = hashlib.sha1(url.split("?")[0].encode()).hexdigest()[:8]
    fname = f"{stem}-{h}.{ext.lower()}"
    dest = dest_dir / fname
    if not dest.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        for attempt in range(3):
            try:
                dest.write_bytes(urllib.request.urlopen(req, timeout=120).read())
                report[kind] += 1
                break
            except Exception as e:  # noqa
                if attempt == 2:
                    report["unhandled"].append(f"download failed {url}: {e}")
                    return url
                time.sleep(2)
    return f"/{dest_dir.name}/{fname}"


GB = r"https://(?:content\.gitbook\.com|files\.gitbook\.com|[0-9]+-files\.gitbook\.io|rc\.sunbird\.org/~gitbook/image)"


# Corrections to mistakes in the live GitBook content: page path -> [(wrong, right)]
CONTENT_FIXES = {
    "engage/use-case-walkthroughs": [
        # link text named a domain Sunbird does not own; the link itself goes to the real sandbox
        ("[sandbox.rc.org](https://sandbox-rc.sunbird.org/presentation/)",
         "[sandbox-rc.sunbird.org/presentation](https://sandbox-rc.sunbird.org/presentation/)"),
    ],
}


def content_fixes(text, path):
    for wrong, right in CONTENT_FIXES.get(path, []):
        if wrong not in text:
            report["unhandled"].append(f"content fix no longer matches in {path}: {wrong[:50]}")
        text = text.replace(wrong, right)
    return text


LANGUAGES = {"English", "Português", "Português (Brasil)", "Español", "Français", "Hindi", "हिन्दी"}
DETAILS = r"<details(?: open)?>\s*<summary>([^<]+)</summary>\s*(.*?)\s*</details>"


def language_tabs(text):
    """GitBook pages show the same text in several languages as stacked <details> blocks.
    Turn each run of them into tabs; sharedStateKey keeps every group on the page on the same language."""
    def swap(m):
        blocks = re.findall(DETAILS, m.group(0), re.S)
        if len(blocks) < 2 or not all(lang.strip() in LANGUAGES for lang, _ in blocks):
            return m.group(0)
        tabs = "".join(f'<PluginTabsTab label="{html.escape(lang.strip())}">\n\n{body}\n\n</PluginTabsTab>\n'
                       for lang, body in blocks)
        return f'<PluginTabs sharedStateKey="language">\n{tabs}</PluginTabs>\n'
    return re.sub(r"(?:" + DETAILS + r"\s*){2,}", swap, text, flags=re.S)


def gif_to_video(text):
    """Animated GIF screen recordings are 10-25 MB each. Re-encode them as H.264 MP4 at CRF 18
    (visually identical, about 80-90% smaller) and play them like a GIF: autoplay, muted, looping."""
    def swap(m):
        tag, src = m.group(0), m.group(1)
        gif = IMG_DIR / src.rsplit("/", 1)[-1]
        mp4 = MEDIA_DIR / (gif.stem + ".mp4")
        if not mp4.exists():
            if not gif.exists():
                report["unhandled"].append(f"gif missing {gif.name}")
                return tag
            MEDIA_DIR.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(gif), "-movflags", "+faststart",
                            "-pix_fmt", "yuv420p", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-an", str(mp4)], check=True)
            report["gifs_converted"] = report.get("gifs_converted", 0) + 1
        gif.unlink(missing_ok=True)  # the MP4 replaces it; the GIF is not kept in the repo
        alt = re.search(r'alt="([^"]*)"', tag)
        label = f' aria-label="{alt.group(1)}"' if alt and alt.group(1) else ""
        return (f'<video class="gif-video" autoplay muted loop playsinline preload="auto"{label} '
                f'src="/{MEDIA_DIR.name}/{mp4.name}"></video>')
    return re.sub(r'<img src="(/images/[^"]+\.gif)"[^>]*>', swap, text)


def localise_images(text):
    # inside src="..." anything up to the closing quote; in Markdown allow one level of (...) in the URL
    text = re.sub(r'(src=")(' + GB + r'[^"]*)(")', lambda m: m.group(1) + fetch(m.group(2), IMG_DIR, "images") + m.group(3), text)
    text = re.sub(r"(!\[[^\]]*\]\()(" + GB + r"[^\s()]*(?:\([^\s()]*\)[^\s()]*)*)(\))",
                  lambda m: m.group(1) + fetch(m.group(2), IMG_DIR, "images") + m.group(3), text)
    return text


# ---------------------------------------------------------------- GitBook block conversion
TAG = re.compile(r"\{%\s*(end)?([a-z-]+)((?:\s+[a-zA-Z-]+=\"[^\"]*\")*)\s*%\}")


def attrs(s):
    return {k: v for k, v in re.findall(r'([a-zA-Z-]+)="([^"]*)"', s)}


def parse(text):
    """Split into a tree of str and dict(name, attrs, children)."""
    root = {"name": "root", "attrs": {}, "children": []}
    stack, pos = [root], 0
    for m in TAG.finditer(text):
        stack[-1]["children"].append(text[pos:m.start()])
        pos = m.end()
        end, name, a = m.group(1), m.group(2), attrs(m.group(3))
        report["blocks"][name] = report["blocks"].get(name, 0) + (0 if end else 1)
        if name in ("embed", "openapi") and not end:
            node = {"name": name, "attrs": a, "children": []}
            stack[-1]["children"].append(node)
            # GitBook allows these without an end tag; only open a block if the end tag comes first
            close = re.search(r"\{%\s*end" + name + r"\s*%\}", text[m.end():])
            nxt = re.search(r"\{%\s*" + name + r"\s", text[m.end():])
            if close and (not nxt or close.start() < nxt.start()):
                stack.append(node)
            continue
        if end:
            if stack[-1]["name"] == name:
                stack.pop()
            else:
                report["unhandled"].append(f"unbalanced end{name}")
            continue
        node = {"name": name, "attrs": a, "children": []}
        stack[-1]["children"].append(node)
        if name in ("hint", "tabs", "tab", "stepper", "step", "columns", "column", "content-ref", "code", "updates", "update"):
            stack.append(node)
        else:
            report["unhandled"].append(f"unknown tag {name}")
    stack[-1]["children"].append(text[pos:])
    return root


def height(node):
    kids = [c for c in node["children"] if isinstance(c, dict)]
    return 1 + max((height(k) for k in kids), default=0)


HINT = {"info": "info", "warning": "warning", "danger": "danger", "success": "tip"}


def unwrap_url(u):
    return u.strip().strip("<>")


def render(node):
    out = []
    for c in node["children"]:
        out.append(c if isinstance(c, str) else render_block(c))
    return "".join(out)


def render_block(n):
    name, a = n["name"], n["attrs"]
    inner = render(n)
    fence = ":" * (2 + height(n))  # outer containers get more colons than nested ones
    if name == "hint":
        return f"\n{fence} {HINT.get(a.get('style'), 'info')}\n{inner.strip()}\n{fence}\n"
    if name == "tabs":
        return f"\n{fence} tabs\n{inner.strip()}\n{fence}\n"
    if name == "tab":
        return f"\n== {a.get('title', 'Tab').strip()}\n\n{inner.strip()}\n"
    if name == "stepper":
        return f"\n{fence} steps\n{inner.strip()}\n{fence}\n"
    if name == "step":
        return f"\n{fence} step\n{inner.strip()}\n{fence}\n"
    if name == "columns":
        return f"\n{fence} columns\n{inner.strip()}\n{fence}\n"
    if name == "column":
        return f"\n{fence} column\n{inner.strip()}\n{fence}\n"
    if name == "content-ref":
        return f"\n{fence} card\n{inner.strip()}\n{fence}\n"
    if name in ("updates",):
        return f"\n{inner.strip()}\n"
    if name == "update":
        tags = ", ".join(t.replace("-", " ") for t in a.get("tags", "").split(",") if t)
        meta = f'<p class="update-meta">{a.get("date", "")}{" · " + tags if tags else ""}</p>'
        body = inner.strip()
        # put the date line after the release heading
        body = re.sub(r"^(## .*\n)", lambda m: m.group(1) + "\n" + meta + "\n", body, count=1) if body.startswith("## ") else meta + "\n\n" + body
        return f"\n{body}\n\n---\n"
    if name == "code":
        body = inner.strip()
        title = a.get("title")
        ln = a.get("lineNumbers") == "true"

        def addinfo(m):
            info = m.group(1)
            if title:
                info += f" [{title}]"
            if ln:
                info += " :line-numbers"
            return "```" + info + "\n"
        return "\n" + re.sub(r"^```([^\n]*)\n", addinfo, body, count=1) + "\n"
    if name == "embed":
        url = unwrap_url(a.get("url", ""))
        caption = inner.strip()
        yt = re.search(r"(?:youtube\.com/watch\?(?:.*&)?v=|youtu\.be/)([\w-]{11})", url)
        if yt:
            html = (f'<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/{yt.group(1)}" '
                    f'title="{caption or "Video"}" allowfullscreen loading="lazy"></iframe></div>')
        elif re.search(r"\.(mp4|webm|mov)(\?|$)", url):
            html = f'<video class="video-file" controls preload="metadata" src="{fetch(url, MEDIA_DIR, "media")}"></video>'
        else:
            html = f'<p><a href="{url}">{caption or url}</a></p>'
        if caption and not yt:
            caption = ""
        return f"\n{html}\n" + (f'<p class="embed-caption">{caption}</p>\n' if caption else "")
    if name == "openapi":
        src = unwrap_url(a.get("src", ""))
        spec = src.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        return f'\n<ApiOperation spec="{spec}" path="{a.get("path")}" method="{a.get("method")}" />\n'
    report["unhandled"].append(f"render {name}")
    return inner


# ---------------------------------------------------------------- text fixes outside code
def outside_code(text, fn):
    parts = re.split(r"(^```.*?^```[^\n]*$)", text, flags=re.S | re.M)
    for i in range(0, len(parts), 2):
        segs = re.split(r"(`[^`\n]+`)", parts[i])
        for j in range(len(segs)):
            if j % 2 == 0:
                segs[j] = fn(segs[j])
            elif "{{" in segs[j]:  # inline code is still compiled by Vue
                segs[j] = "<code v-pre>" + html.escape(segs[j][1:-1], quote=False) + "</code>"
        parts[i] = "".join(segs)
    return "".join(parts)


# Pages given cleaner URLs than GitBook's (GitBook nests a section's pages under its README).
# The old URLs keep working through small redirect pages in public/.
PATH_MOVES = {
    "learn/readme": "learn/overview",
    "learn/readme/why-do-we-need-sunbird-rc": "learn/why-do-we-need-sunbird-rc",
    "learn/readme/what-sunbird-rc-is-and-what-its-not": "learn/what-sunbird-rc-is-and-what-its-not",
    "learn/readme/core-capabilities": "learn/core-capabilities",
    "learn/readme/workflows": "learn/workflows",
    "learn/readme/possibilities": "learn/possibilities",
    "use/getting-started/developer-setup": "use/developer-setup",
    "use/getting-started/installation": "use/installation",
    "use/getting-started/installation/registry-cli": "use/installation/registry-cli",
    "use/getting-started/installation/docker-compose-setup": "use/installation/docker-compose-setup",
    "use/getting-started/installation/helm-setup": "use/installation/helm-setup",
    "use/getting-started/installation/credentialling-services-setup-dev-docker-helm": "use/installation/credentialling-services-setup-dev-docker-helm",
    "use/getting-started/for-existing-adopters": "use/for-existing-adopters",
    "engage/use-case-walkthroughs": "learn/use-case-walkthroughs",
    "engage/discussions": "community/discussions",
    "engage/contributing": "community/contributing",
    "engage/contribution-guidebook": "community/contribution-guidebook",
    "engage/code-of-conduct": "community/code-of-conduct",
}


# Links that are already broken (404) on the live GitBook site, pointing at pre-restructure paths.
LINK_FIXES = {
    "learn/technical-overview/registry/high-level-architecture": "registry/technical-overview/high-level-architecture",
    "learn/technical-overview/credentialling/high-level-architecture": "credentials/technical-overview/high-level-architecture",
    "api-reference/registry-apis/schema/create-schema": "registry/api-reference/schema/create-schema",
    "api-reference/registry-apis/registry/invite-an-entity": "registry/api-reference/registry/invite-an-entity",
    "api-reference/registry-apis/registry/get-an-entity": "registry/api-reference/registry/get-an-entity",
    "use/developers-guide/functional-registry/schema-setup/schema-configuration": "use/developer-guide/schema-setup/schema-configuration",
    "api-reference/registry-apis": "registry/",
}


def fix_links(t):
    def site_link(m):
        path, frag = m.group(1), m.group(2) or ""
        path = re.sub(r"\.md$", "", path)
        path = LINK_FIXES.get(path, path)
        path = PATH_MOVES.get(path, path)
        return "/" + path + frag
    t = re.sub(r"https://rc\.sunbird\.org/([^\s)\"'#>]*?)(?:\.md)?(#[^\s)\"'>]*)?(?=[\s)\"'>])", site_link, t)
    return t


# GitBook text colours (named, or GitBook tokens like $info) -> VitePress theme colours that adapt to dark mode
MARK_COLOURS = {
    "red": "var(--vp-c-red-1)", "green": "var(--vp-c-green-1)", "blue": "var(--vp-c-indigo-1)",
    "orange": "var(--vp-c-brand-1)", "yellow": "var(--vp-c-yellow-1)", "purple": "var(--vp-c-purple-1)",
    "$primary": "var(--vp-c-brand-1)", "$info": "var(--vp-c-indigo-1)", "$success": "var(--vp-c-green-1)",
    "$warning": "var(--vp-c-yellow-1)", "$danger": "var(--vp-c-red-1)",
}


def fix_mark_colours(t):
    return re.sub(r'(<mark style="color:)([$\w]+)(;?")',
                  lambda m: m.group(1) + MARK_COLOURS.get(m.group(2), m.group(2)) + m.group(3), t)


def text_fixes(t):
    t = fix_mark_colours(t)
    # autolinks <https://x> -> <a> so they also work inside raw HTML blocks
    t = re.sub(r"<(https?://[^>\s]+)>", r'<a href="\1">\1</a>', t)
    # Vue would treat {{ }} as template interpolation
    t = re.sub(r"\{\{.*?\}\}", lambda m: f"<span v-pre>{m.group(0)}</span>", t)
    return t


PAGE_COVERS = {}  # page path -> component to place above the title (GitBook covers are not exported)

CLIENT_TOOLS = {"curl", "httpie", "wget", "postman", "python", "javascript", "node.js", "java", "go"}
RUN = re.compile(r"(?:^#{2,6} [^\n]+\n\n```[^\n]*\n(?:.*?\n)?```\n\n?){2,}", re.M | re.S)
PAIR = re.compile(r"^#{2,6} ([^\n]+)\n\n```([^\n]*)\n(.*?\n)?```", re.M | re.S)


def code_groups(text):
    """Turn runs like '#### cURL' + code, '#### HTTPie' + code into one VitePress code group."""
    def group(m):
        pairs = PAIR.findall(m.group(0))
        if not all(h.strip().lower() in CLIENT_TOOLS for h, _, _ in pairs):
            return m.group(0)  # numbered walkthrough steps etc. stay as they are
        blocks = "".join(f"```{(lang.strip() or 'shell')} [{h.strip()}]\n{code}```\n" for h, lang, code in pairs)
        return f"::: code-group\n{blocks}:::\n\n"
    return RUN.sub(group, text)


def convert(raw, page):
    body = raw.split("\n---\n\n# Agent Instructions")[0]
    lines = body.splitlines()
    if lines and lines[0].startswith("> For the complete documentation index"):
        lines = lines[1:]
    body = "\n".join(lines).strip() + "\n"
    # GitBook's export sometimes puts a closing tag inside the last table row: "| {% endtab %} |   |"
    body = re.sub(r"^\|\s*(\{%\s*end[a-z-]+\s*%\})\s*\|[\s|]*$", r"\n\1", body, flags=re.M)
    body = render(parse(body))
    body = code_groups(body)
    body = localise_images(body)
    body = gif_to_video(body)
    body = language_tabs(body)
    body = content_fixes(body, page.get("live_path", page["path"]))  # keyed by the GitBook path
    body = outside_code(body, text_fixes)
    body = fix_links(body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    # GitBook page covers are not in the Markdown export; add the ones we rebuilt as components
    if page["path"] in PAGE_COVERS:
        body = PAGE_COVERS[page["path"]] + "\n\n" + body
    fm = {"title": page["title"]}
    if page["desc"]:
        fm["description"] = page["desc"]
    head = "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in fm.items()) + "---\n\n"
    return head + body


# ---------------------------------------------------------------- moved pages
for p in pages:
    p["live_path"] = p["path"]
    if p["path"] in PATH_MOVES:
        p["path"] = PATH_MOVES[p["path"]]
for old_path, new_path in PATH_MOVES.items():
    (OUT / (old_path + ".md")).unlink(missing_ok=True)  # copies from earlier runs
    stub = OUT / "public" / (old_path + ".html")
    stub.parent.mkdir(parents=True, exist_ok=True)
    stub.write_text(f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sunbird RC</title>
  <!-- This page moved; keep old links working -->
  <meta http-equiv="refresh" content="0; url=/{new_path}">
  <link rel="canonical" href="https://rc.sunbird.org/{new_path}">
</head>
<body><p>This page moved to <a href="/{new_path}">/{new_path}</a>.</p></body>
</html>
""")
for d in sorted({(OUT / o).parent for o in PATH_MOVES} | {OUT / o for o in PATH_MOVES}, reverse=True):
    if d.is_dir() and not any(d.iterdir()):
        d.rmdir()

# ---------------------------------------------------------------- write pages
for p in pages:
    raw = (LIVE / "raw" / (p["live_path"] + ".md")).read_text()
    dest = OUT / (p["path"] + ".md")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(convert(raw, p))

# openapi specs (vendored copy of sunbird-rc-core/api-documentation)
(OUT / "openapi").mkdir(exist_ok=True)
for f in (LIVE / "openapi").glob("*.yaml"):
    shutil.copy(f, OUT / "openapi" / f.name)

# public/logo.png is a hand-cropped asset kept in the repo; this script does not touch it.


# ---------------------------------------------------------------- sidebar
GROUP_TITLES = {"learn": "Learn", "use": "Use", "engage": "Engage", "help": "Help",
                "technical-overview": "Technical Overview", "api-reference": "API Reference"}


def build(items, prefix_depth):
    groups, order = {}, []
    for p in items:
        seg = p["path"].split("/")[prefix_depth]
        if seg not in groups:
            groups[seg] = []
            order.append(seg)
        groups[seg].append(p)
    result = []
    for seg in order:
        nodes, by_path = [], {}
        for p in groups[seg]:
            node = {"text": p["title"], "link": "/" + p["path"]}
            by_path[p["path"]] = node
            parent = p["path"].rsplit("/", 1)[0]
            while parent and parent not in by_path:
                parent = parent.rsplit("/", 1)[0] if "/" in parent else ""
            if parent:
                by_path[parent].setdefault("items", []).append(node)
                by_path[parent]["collapsed"] = True
            else:
                nodes.append(node)
        result.append({"text": GROUP_TITLES.get(seg, seg.replace("-", " ").title()), "items": nodes})
    return result


kb = [p for p in pages if p["space"] == "RC Knowledge Base"]
reg = [p for p in pages if p["space"] == "Registry"]
cred = [p for p in pages if p["space"] == "Credentials"]


def section(title, items):
    """A collapsible top-level sidebar section; VitePress opens it when the current page is inside."""
    groups = [dict(g, collapsed=True) for g in build(items, 1)]
    return {"text": title, "collapsed": True, "items": groups}


# One sidebar for the whole site, organised by what the reader is doing. Registry and Credentials can be
# adopted on their own, so each is a self-contained section. Only the sidebar is arranged this way:
# every page keeps its live GitBook URL. Labels here override page titles in the sidebar only.
#   (path, label)                         a page
#   (path, label, [children])             a page with sub-pages
#   ("group", label, [children])          a heading without a page
#   ("api", label, space, segment)        an API reference tree, built from the live page order
SIDEBAR = [
    ("group", "Introduction", [
        ("learn/overview", "Overview"),
        ("learn/why-do-we-need-sunbird-rc", "Why Sunbird RC"),
        ("learn/what-sunbird-rc-is-and-what-its-not", "What it is and isn't"),
        ("learn/core-capabilities", "Core capabilities"),
        ("learn/workflows", "How it works"),
        ("learn/possibilities", "Possibilities"),
        ("learn/use-case-walkthroughs", "Use case Walkthroughs"),
        ("learn/adopters", "Adopters"),
    ]),
    ("group", "Get started", [
        ("use/getting-started", "Choose your path"),
        ("use/developer-setup", "Prerequisites"),
        ("use/installation", "Installation options"),
        ("use/releases", "What's new"),
        ("use/for-existing-adopters", "Upgrading"),
    ]),
    ("group", "Registry", [
        ("group", "Architecture", [
            ("registry/technical-overview/high-level-architecture", "Architecture"),
            ("registry/technical-overview/technical-specification-draft", "Technical specification (draft)"),
            ("registry/technical-overview/infrastructure-requirements", "Requirements"),
        ]),
        ("group", "Install", [
            ("use/installation/registry-cli", "Registry CLI"),
            ("use/installation/docker-compose-setup", "Docker Compose"),
            ("use/installation/helm-setup", "Helm (Kubernetes)"),
        ]),
        ("use/developer-guide/schema-setup", "Schemas", [
            ("use/developer-guide/schema-setup/introduction-to-schemas", "Introduction"),
            ("use/developer-guide/schema-setup/creating-your-own-schemas", "Create your own"),
            ("use/developer-guide/schema-setup/schema-configuration", "Configuration"),
            ("use/developer-guide/schema-setup/create-schemas-with-custom-password", "Custom passwords"),
        ]),
        ("group", "Configure and operate", [
            ("use/developer-guide/environment-variable-reference", "Environment variables"),
            ("use/developer-guide/configuration-reference", "Configuration files"),
            ("use/developer-guide/metrics", "Metrics and events"),
            ("use/developer-guide/backup-and-restore", "Backup and restore", [
                ("use/developer-guide/backup-and-restore/postgresql", "PostgreSQL"),
                ("use/developer-guide/backup-and-restore/cassandra", "Cassandra"),
            ]),
        ]),
        ("group", "Identity and access", [
            ("use/developer-guide/generic-iam", "Identity providers (IAM)"),
            ("use/developer-guide/custom-keycloak-build", "Custom Keycloak build"),
            ("use/integrations/sso-with-existing-systems", "SSO with existing systems"),
            ("use/integrations/digilocker-meripehchaan-sso", "DigiLocker MeriPehchaan SSO"),
        ]),
        ("group", "Develop", [
            ("use/developer-guide/working-with-source-code", "Work with the source code"),
            ("use/developer-guide/setup-backend", "Set up the backend"),
            ("use/developer-guide/setup-frontend", "Set up the frontend"),
        ]),
        ("api", "API reference", "Registry", "api-reference"),
        ("use/releases/registry", "Releases", [
            ("use/releases/registry/v2.0.3", "v2.0.3 (latest)"),
            ("use/releases/registry/v1.0.0", "v1.0.0"),
        ]),
    ]),
    ("group", "Credentials", [
        ("group", "Architecture", [
            ("credentials/technical-overview/high-level-architecture", "Architecture"),
            ("credentials/technical-overview/technical-specification-draft", "Technical specification (draft)"),
            ("credentials/technical-overview/tech-stack-and-requirements", "Requirements"),
        ]),
        ("group", "Install", [
            ("use/installation/credentialling-services-setup-dev-docker-helm", "Dev, Docker Compose and Helm"),
        ]),
        ("group", "Wallets and verification", [
            ("use/integrations/wallet-integration", "Wallet integration (OpenID4VC)"),
            ("use/connectors/openid-for-verifiable-credentials-oid4vci", "OpenID4VCI connector"),
            ("use/developer-guide/vc-verification-module", "VC verification module"),
            ("use/integrations/digilocker-integration", "DigiLocker wallet"),
        ]),
        ("api", "API reference", "Credentials", "api-reference"),
        ("use/releases/credentialing", "Releases", [
            ("use/releases/credentialing/v2.1.0-latest-release", "v2.1.0 (latest)"),
            ("use/releases/credentialing/v2.0.3", "v2.0.3"),
            ("use/releases/credentialing/v2.0.0", "v2.0.0"),
        ]),
    ]),
    ("group", "Community", [
        ("community/discussions", "Discussion forum"),
        ("community/contributing", "Contributing"),
        ("community/contribution-guidebook", "Contribution guidebook"),
        ("help/roadmap", "Roadmap"),
        ("community/code-of-conduct", "Code of Conduct"),
    ]),
    ("group", "Reference", [
        ("help/faqs", "FAQs"),
        ("help/terminology", "Glossary"),
        ("concepts",),  # the concepts guide's sections, listed directly
        ("help/external-open-source-software-attributions", "Open source attributions"),
    ]),
]
# Landing pages that only link to their sub-pages; still published, but the sidebar lists the sub-pages instead
UNLISTED = {"use/developer-guide", "use/integrations", "use/connectors",
            "help/comprehensive-overview-electronic-registries-and-verifiable-credentials"}
CONCEPTS = "help/comprehensive-overview-electronic-registries-and-verifiable-credentials"
# Sections shown open; the rest start collapsed and open when the current page is inside them
OPEN = {"Introduction", "Get started", "Registry", "Credentials", "Community", "Reference"}

API_GROUPS = {"Schema": "Schema APIs", "Registry": "Entity APIs", "Attestation API": "Attestation APIs",
              "Claims API": "Claims APIs", "Discovery API": "Discovery APIs", "File storage API": "File storage APIs"}
ACRONYMS = {"id": "ID", "api": "API", "apis": "APIs", "json": "JSON", "vc": "VC", "oid4vc": "OID4VC", "qr": "QR",
            "did": "DID", "sso": "SSO", "iam": "IAM"}


def sentence_case(title):
    words = title.replace("/ ", "or ").split()
    out = []
    for i, w in enumerate(words):
        low = w.lower()
        if low in ACRONYMS:
            out.append(ACRONYMS[low])
        elif i == 0:
            out.append(w[:1].upper() + w[1:])
        elif w.isupper() or any(c.isdigit() for c in w):
            out.append(w)
        else:
            out.append(low)
    return " ".join(out)


by_path = {p["path"]: p for p in pages}
placed = set()


def api_tree(space, segment):
    items = [p for p in pages if p["space"] == space and p["path"].split("/")[1] == segment]
    tree = build(items, 1)[0]["items"]

    def relabel(nodes):
        for n in nodes:
            placed.add(n["link"].lstrip("/"))
            n["text"] = sentence_case(n["text"])
            if "items" in n:
                relabel(n["items"])
    relabel(tree)
    for n in tree:  # group names that say what each set of APIs is for
        n["text"] = API_GROUPS.get(n["text"], n["text"])
    return tree


def concepts_tree():
    items = [p for p in pages if p["path"].startswith(CONCEPTS + "/")]
    tree = build([by_path[CONCEPTS]] + items, 0)[0]["items"][0]  # the guide page, with its sub-pages
    def mark(n):
        placed.add(n["link"].lstrip("/"))
        n["text"] = sentence_case(n["text"])
        for c in n.get("items", []):
            mark(c)
    mark(tree)
    return tree


def render_sidebar(entries, depth=0):
    out = []
    for e in entries:
        if e[0] == "group":
            node = {"text": e[1], "items": render_sidebar(e[2], depth + 1)}
            if depth > 0 or e[1] not in OPEN:
                node["collapsed"] = True
        elif e[0] == "api":
            node = {"text": e[1], "collapsed": True, "items": api_tree(e[2], e[3])}
        elif e[0] == "concepts":
            out.extend(concepts_tree().get("items", []))
            continue
        else:
            path, label = e[0], e[1]
            if path not in by_path:
                report["unhandled"].append(f"sidebar lists a page that does not exist: {path}")
                continue
            placed.add(path)
            node = {"text": label, "link": "/" + path}
            if len(e) > 2:
                node["items"] = render_sidebar(e[2], depth + 1)
                node["collapsed"] = True
        out.append(node)
    return out


# Order: Introduction, Get started, Registry, Credentials, Community, Reference (as listed in SIDEBAR)
sidebar = render_sidebar(SIDEBAR)
# Any page the plan does not mention (for example, one added on GitBook later) goes in a visible group
unsorted = [p for p in pages if p["path"] not in placed and p["path"] not in UNLISTED]
if unsorted:
    sidebar.append({"text": "Not yet sorted", "items": [{"text": p["title"], "link": "/" + p["path"]} for p in unsorted]})
    report["unhandled"].append("pages missing from the sidebar plan: " + ", ".join(p["path"] for p in unsorted))
(OUT / ".vitepress").mkdir(exist_ok=True)
(OUT / ".vitepress" / "sidebar.json").write_text(json.dumps(sidebar, indent=2, ensure_ascii=False) + "\n")

# section landing pages keep the live /registry and /credentials URLs working
for sec, items in (("registry", reg), ("credentials", cred)):
    first = items[0]["path"].split("/", 1)[1]
    (OUT / sec / "index.md").write_text(f"<!--@include: ./{first}.md-->\n")

print(json.dumps(report, indent=1))
