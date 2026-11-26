import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import { enhanceAppWithTabs } from 'vitepress-plugin-tabs/client'
import ApiOperation from './components/ApiOperation.vue'
import RcBanner from './components/RcBanner.vue'
import Mermaid from './components/Mermaid.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    enhanceAppWithTabs(app)
    app.component('ApiOperation', ApiOperation)
    app.component('RcBanner', RcBanner)
    app.component('Mermaid', Mermaid)
  },
} satisfies Theme
