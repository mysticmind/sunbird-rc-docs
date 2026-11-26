"""One-off migration of the live rc.sunbird.org GitBook site into this VitePress repo.

Usage: python3 scripts/migrate-from-gitbook.py <work_dir> <repo_root> [--fetch]
  --fetch  download llms.txt, every page's Markdown export and the OpenAPI specs into <work_dir> first
  work_dir then holds llms_.txt, raw/<page>.md and openapi/*.yaml

Rerun it only while GitBook is still being edited; after the switch, edit the Markdown here.
"""
import hashlib, html, json, re, shutil, sys, time, urllib.parse, urllib.request
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
print(len(pages), "pages")


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


PAGE_COVERS = {"learn/welcome-aboard": "<RcBanner />"}

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


# ---------------------------------------------------------------- write pages
for p in pages:
    raw = (LIVE / "raw" / (p["path"] + ".md")).read_text()
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
sidebar = {"/": build(kb, 0), "/registry/": build(reg, 1), "/credentials/": build(cred, 1)}
(OUT / ".vitepress").mkdir(exist_ok=True)
(OUT / ".vitepress" / "sidebar.json").write_text(json.dumps(sidebar, indent=2, ensure_ascii=False) + "\n")

# section landing pages keep the live /registry and /credentials URLs working
for sec, items in (("registry", reg), ("credentials", cred)):
    first = items[0]["path"].split("/", 1)[1]
    (OUT / sec / "index.md").write_text(f"<!--@include: ./{first}.md-->\n")

print(json.dumps(report, indent=1))
