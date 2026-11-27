import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import { enhanceAppWithTabs } from 'vitepress-plugin-tabs/client'
import ApiOperation from './components/ApiOperation.vue'
import Mermaid from './components/Mermaid.vue'
import CornerBadges from './components/CornerBadges.vue'
import CopyOrDownloadAsMarkdownButtons from 'vitepress-plugin-llms/vitepress-components/CopyOrDownloadAsMarkdownButtons.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  // COSS and Digital Public Good badges in the bottom-right corner of every page
  Layout: () => h(DefaultTheme.Layout, null, { 'layout-bottom': () => h(CornerBadges) }),
  enhanceApp({ app }) {
    enhanceAppWithTabs(app)
    app.component('ApiOperation', ApiOperation)
    app.component('Mermaid', Mermaid)
    app.component('CopyOrDownloadAsMarkdownButtons', CopyOrDownloadAsMarkdownButtons)
  },
} satisfies Theme
