import { defineConfig } from 'vitepress'
import container from 'markdown-it-container'
import { tabsMarkdownPlugin } from 'vitepress-plugin-tabs'
import llmstxt from 'vitepress-plugin-llms'
import sidebar from './sidebar.json'

// Placeholder until the docs repo exists on GitHub.
const REPO = 'https://github.com/Sunbird-RC/docs'
const BRANCH = 'main'

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
  cleanUrls: true,
  lastUpdated: true,
  srcExclude: ['README.md', 'CONTRIBUTING.md'],
  ignoreDeadLinks: 'localhostLinks',
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    ['link', { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32.png' }],
    ['link', { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' }],
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
      md.use(tabsMarkdownPlugin)
      for (const [name, cls] of Object.entries(wrappers)) {
        md.use(container, name, {
          render: (tokens: any[], idx: number) =>
            tokens[idx].nesting === 1 ? `<div class="${cls}">\n` : '</div>\n',
        })
      }
    },
  },

  vite: {
    plugins: [llmstxt({ domain: 'https://rc.sunbird.org' })],
  },

  themeConfig: {
    logo: { src: '/logo-rc.svg', alt: 'Sunbird RC' },
    siteTitle: false,
    nav: [
      { text: 'Knowledge Base', link: '/learn/welcome-aboard', activeMatch: '^/(learn|use|engage|help)/' },
      { text: 'Registry', link: '/registry/', activeMatch: '^/registry/' },
      { text: 'Credentials', link: '/credentials/', activeMatch: '^/credentials/' },
      {
        text: 'Releases',
        items: [
          { text: 'Registry releases', link: '/use/releases/registry' },
          { text: 'Credentialing releases', link: '/use/releases/credentialing' },
        ],
      },
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
      message: 'Released under the MIT License. For AI agents: <a href="/llms.txt">llms.txt</a>',
      copyright:
        'Copyright (c) 2023 International Institute of Information Technology, Bangalore (IIITB), on behalf of the Centre for Open Societal Systems (COSS)',
    },
  },
})
