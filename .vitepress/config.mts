import { mkdirSync, writeFileSync, existsSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { defineConfig } from 'vitepress'
import container from 'markdown-it-container'
import { tabsMarkdownPlugin } from 'vitepress-plugin-tabs'
import llmstxt, { copyOrDownloadAsMarkdownButtons } from 'vitepress-plugin-llms'
import sidebar from './sidebar.json'
import redirects from './redirects.json'

// Showcase repo for review; change to the Sunbird-RC organisation repo when it moves there.
const REPO = 'https://github.com/mysticmind/sunbird-rc-docs'
const BRANCH = 'main'

// Where the site is served. Defaults are for rc.sunbird.org; the deploy workflow overrides them when the
// site is published as a project page under a sub-path (for example a personal github.io demo).
const BASE = process.env.DOCS_BASE || '/'
const SITE = process.env.DOCS_SITE || 'https://rc.sunbird.org'

// Simple wrappers for the GitBook blocks that VitePress has no equivalent for.
const wrappers: Record<string, string> = {
  steps: 'rc-steps',
  step: 'rc-step',
  columns: 'rc-columns',
  column: 'rc-column',
  card: 'rc-card',
}

export default defineConfig({
  title: 'Sunbird RC',
  description: 'Build live, reusable and trustworthy registries and verifiable credentials, with configuration, not code.',
  lang: 'en-US',
  base: BASE,
  cleanUrls: true,
  lastUpdated: true,
  srcExclude: ['README.md', 'CONTRIBUTING.md'],
  ignoreDeadLinks: 'localhostLinks',
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: `${BASE}favicon.svg` }],
    ['link', { rel: 'icon', type: 'image/png', sizes: '32x32', href: `${BASE}favicon-32.png` }],
    ['link', { rel: 'apple-touch-icon', sizes: '180x180', href: `${BASE}apple-touch-icon.png` }],
  ],

  markdown: {
    config(md) {
      // ```mermaid blocks become diagrams, rendered in the browser by the Mermaid component
      const fence = md.renderer.rules.fence!
      md.renderer.rules.fence = (tokens, idx, options, env, self) => {
        const token = tokens[idx]
        if (token.info.trim() === 'mermaid') {
          return `<Mermaid code="${encodeURIComponent(token.content)}" />`
        }
        return fence(tokens, idx, options, env, self)
      }
      // VitePress adds the base path to Markdown links but not to links written as raw HTML in the content
      // (tables, buttons). Prefix those too, so the site also works when served under a sub-path.
      // (Images and video src are left alone: Vite resolves those and adds the base itself.)
      if (BASE !== '/') {
        const prefix = (html: string) =>
          html.replace(/\bhref="\/(?!\/)/g, (m, offset, str) =>
            str.startsWith(BASE, offset + 6) ? m : `href="${BASE}`)
        md.core.ruler.push('rc-base-in-html', (state) => {
          for (const t of state.tokens) {
            if (t.type === 'html_block') t.content = prefix(t.content)
            for (const c of t.children ?? []) if (c.type === 'html_inline') c.content = prefix(c.content)
          }
        })
      }
      md.use(tabsMarkdownPlugin)
      // "Copy page" button and dropdown (view / download as Markdown, open in an AI assistant) under each page title
      md.use(copyOrDownloadAsMarkdownButtons)
      for (const [name, cls] of Object.entries(wrappers)) {
        md.use(container, name, {
          render: (tokens: any[], idx: number) =>
            tokens[idx].nesting === 1 ? `<div class="${cls}">\n` : '</div>\n',
        })
      }
    },
  },

  vite: {
    plugins: [llmstxt({ domain: SITE })],
  },

  // Previous/next links come from the sidebar order; keep them within one top-level section so a page
  // never points across, say, from Registry release notes to the Credentials architecture page.
  transformPageData(pageData) {
    const order: { link: string; section: string }[] = []
    const walk = (items: any[], section: string) => {
      for (const item of items) {
        if (item.link) order.push({ link: item.link, section })
        if (item.items) walk(item.items, section)
      }
    }
    for (const group of sidebar as any[]) walk(group.items ?? [], group.text)
    const link = '/' + pageData.relativePath.replace(/(index)?\.md$/, '')
    const i = order.findIndex((o) => o.link === link)
    if (i < 0) return
    if (i === 0 || order[i - 1].section !== order[i].section) pageData.frontmatter.prev ??= false
    if (i === order.length - 1 || order[i + 1].section !== order[i].section) pageData.frontmatter.next ??= false
  },

  // Old GitBook URLs -> new pages (list written by scripts/migrate-from-gitbook.py). GitHub Pages has no
  // server-side redirects, so write a small page for each old URL that forwards to the new one.
  buildEnd({ outDir }) {
    for (const [from, to] of Object.entries(redirects as Record<string, string>)) {
      const target = `${BASE}${to}`
      const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sunbird RC</title>`
        + `<meta http-equiv="refresh" content="0; url=${target}"><link rel="canonical" href="${SITE}/${to}">`
        + `</head><body><p>This page moved to <a href="${target}">${target}</a>.</p></body></html>\n`
      // /old is served from old.html; old/index.html also covers /old/ (with a trailing slash)
      for (const file of [join(outDir, `${from}.html`), join(outDir, from, 'index.html')]) {
        if (existsSync(file)) continue // never overwrite a real page
        mkdirSync(dirname(file), { recursive: true })
        writeFileSync(file, html)
      }
    }
  },

  themeConfig: {
    logo: { src: '/logo-rc.svg', alt: 'Sunbird RC' },
    siteTitle: false,
    nav: [
      { text: 'Introduction', link: '/learn/overview', activeMatch: '^/(learn|use|community|help)/' },
      { text: 'Registry', link: '/registry/architecture/high-level-architecture', activeMatch: '^/registry/' },
      { text: 'Credentials', link: '/credentials/architecture/high-level-architecture', activeMatch: '^/credentials/' },
      {
        text: 'Releases',
        items: [
          { text: 'Registry releases', link: '/registry/releases' },
          { text: 'Credentialing releases', link: '/credentials/releases' },
        ],
      },
      // Index of every page for AI agents and LLM tools (generated by vitepress-plugin-llms)
      { text: 'LLM Friendly Docs', link: `${BASE}llms.txt`, target: '_blank' },
      // The wider Sunbird family of Digital Public Goods
      { text: 'sunbird.org', link: 'https://www.sunbird.org/' },
    ],
    sidebar,
    socialLinks: [{ icon: 'github', link: 'https://github.com/Sunbird-RC/sunbird-rc-core' }],
    search: { provider: 'local' },
    outline: { level: [2, 3] },
    editLink: {
      pattern: `${REPO}/edit/${BRANCH}/:path`,
      text: 'Edit this page on GitHub',
    },
    footer: {
      message: 'Released under the <a href="https://github.com/Sunbird-RC/sunbird-rc-core/blob/main/LICENSE" target="_blank" rel="noopener">MIT License</a>.',
      // Copyright on two balanced lines: who holds it, then on whose behalf
      copyright:
        `Copyright © ${new Date().getFullYear()} `
        + '<a href="https://www.iiitb.ac.in/" target="_blank" rel="noopener">International Institute of Information Technology, Bangalore&nbsp;(IIITB)</a>'
        + '<br>on behalf of the <a href="https://www.coss.org.in/" target="_blank" rel="noopener">Centre for Open Societal Systems&nbsp;(COSS)</a>',
    },
  },
})
