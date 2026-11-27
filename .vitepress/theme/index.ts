import { h, nextTick, onMounted, watch } from 'vue'
import DefaultTheme from 'vitepress/theme'
import { useRoute, withBase, type Theme } from 'vitepress'
import mediumZoom from 'medium-zoom'
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

// VitePress does not scroll the sidebar to the current page. After each navigation, if the active
// entry is outside the visible part of the sidebar, scroll the sidebar (only) so it sits near the top third.
function revealActiveSidebarItem(behavior: ScrollBehavior = 'smooth') {
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const sidebar = document.querySelector<HTMLElement>('.VPSidebar')
    const item = sidebar?.querySelector<HTMLElement>('.VPSidebarItem.is-active > .item')
    if (!sidebar || !item) return
    const box = sidebar.getBoundingClientRect()
    const top = parseFloat(getComputedStyle(sidebar).paddingTop) || 0
    const r = item.getBoundingClientRect()
    if (r.top < box.top + top || r.bottom > box.bottom) {
      sidebar.scrollTo({ top: sidebar.scrollTop + (r.top - box.top) - box.height / 3, behavior })
    }
  }))
}

// Click any image in the docs to view it full screen (logos, icons and badges are outside .vp-doc)
let zoom: ReturnType<typeof mediumZoom> | undefined
function enableImageZoom() {
  zoom?.detach()
  zoom = mediumZoom('.vp-doc img:not(a img)', { margin: 24, background: 'rgba(0, 0, 0, 0.8)' })
}

export default {
  extends: DefaultTheme,
  // COSS and Digital Public Good badges in the bottom-right corner of every page
  // The home page hero logo links to the Overview, like the main call to action
  Layout: () => h(DefaultTheme.Layout, null, {
    'layout-bottom': () => h(CornerBadges),
    'home-hero-image': () => h('a', { class: 'rc-hero-link', href: withBase('/learn/overview'), 'aria-label': 'Sunbird RC overview' },
      [h('img', { class: 'VPImage image-src', src: withBase('/logo-rc.svg'), alt: 'Sunbird RC' })]),
  }),
  enhanceApp({ app }) {
    enhanceAppWithTabs(app)
    app.component('ApiOperation', ApiOperation)
    app.component('Mermaid', Mermaid)
    app.component('CopyOrDownloadAsMarkdownButtons', CopyOrDownloadAsMarkdownButtons)
  },
  setup() {
    const route = useRoute()
    onMounted(() => { respectReducedMotion(); revealActiveSidebarItem('instant'); enableImageZoom() })
    watch(() => route.path, () => nextTick(() => { respectReducedMotion(); revealActiveSidebarItem(); enableImageZoom() }))
  },
} satisfies Theme
