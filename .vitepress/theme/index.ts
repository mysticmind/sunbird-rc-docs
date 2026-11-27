import { h, nextTick, onMounted, watch } from 'vue'
import DefaultTheme from 'vitepress/theme'
import { useRoute, type Theme } from 'vitepress'
import { enhanceAppWithTabs } from 'vitepress-plugin-tabs/client'
import ApiOperation from './components/ApiOperation.vue'
import Mermaid from './components/Mermaid.vue'
import CornerBadges from './components/CornerBadges.vue'
import CopyOrDownloadAsMarkdownButtons from 'vitepress-plugin-llms/vitepress-components/CopyOrDownloadAsMarkdownButtons.vue'
import './custom.css'

// Demo screen recordings play like GIFs. For visitors who ask for reduced motion,
// keep them paused on the first frame and show controls so they can play them on demand.
function respectReducedMotion() {
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  document.querySelectorAll<HTMLVideoElement>('video.gif-video').forEach((v) => {
    v.autoplay = false
    v.pause()
    v.controls = true
  })
}

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
  setup() {
    const route = useRoute()
    onMounted(respectReducedMotion)
    watch(() => route.path, () => nextTick(respectReducedMotion))
  },
} satisfies Theme
