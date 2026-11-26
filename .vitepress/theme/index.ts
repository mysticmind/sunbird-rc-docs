import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import { enhanceAppWithTabs } from 'vitepress-plugin-tabs/client'
import ApiOperation from './components/ApiOperation.vue'
import RcBanner from './components/RcBanner.vue'
import Mermaid from './components/Mermaid.vue'
import DpgBadge from './components/DpgBadge.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  // Digital Public Good badge in the bottom-right corner of every page
  Layout: () => h(DefaultTheme.Layout, null, { 'layout-bottom': () => h(DpgBadge) }),
  enhanceApp({ app }) {
    enhanceAppWithTabs(app)
    app.component('ApiOperation', ApiOperation)
    app.component('RcBanner', RcBanner)
    app.component('Mermaid', Mermaid)
  },
} satisfies Theme
