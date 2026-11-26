<script setup lang="ts">
// Renders a ```mermaid code block as a diagram in the browser, following the light/dark theme.
// Mermaid is loaded only on pages that have a diagram.
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useData } from 'vitepress'

const props = defineProps<{ code: string }>()
const source = decodeURIComponent(props.code)
const svg = ref('')
const failed = ref(false)
const { isDark } = useData()
let count = 0

// Diagram colours that match the site theme: orange outlines, soft fill, muted lines
const LIGHT = {
  fontSize: '14px',
  primaryColor: '#fff4ec',
  primaryBorderColor: '#e06a00',
  primaryTextColor: '#3c3c43',
  secondaryColor: '#f6f6f7',
  tertiaryColor: '#ffffff',
  lineColor: '#8e8e93',
  textColor: '#3c3c43',
  clusterBkg: '#fafafa',
  clusterBorder: '#e2e2e3',
  edgeLabelBackground: '#ffffff',
}
const DARK = {
  fontSize: '14px',
  darkMode: true,
  background: '#1b1b1f',
  primaryColor: '#2a1f17',
  primaryBorderColor: '#ff8a24',
  primaryTextColor: '#dfdfd6',
  secondaryColor: '#202127',
  tertiaryColor: '#1b1b1f',
  lineColor: '#8e8e93',
  textColor: '#dfdfd6',
  clusterBkg: '#202127',
  clusterBorder: '#3c3f44',
  edgeLabelBackground: '#1b1b1f',
}

async function draw() {
  try {
    const mermaid = (await import('mermaid')).default
    await document.fonts?.ready // measure labels with the site font, or multi-line labels get clipped
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      look: 'classic', // no hand-drawn or glow effects
      theme: 'base',
      fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
      themeVariables: isDark.value ? DARK : LIGHT,
      flowchart: { curve: 'basis', padding: 14, nodeSpacing: 40, rankSpacing: 56, wrappingWidth: 240 },
    })
    const id = `mermaid-${Math.random().toString(36).slice(2)}-${count++}`
    const out = (await mermaid.render(id, source)).svg
    // Mermaid sizes diagrams to 100% of the column, which shrinks wide ones until the text is unreadable.
    // Use the diagram's natural width instead; wide diagrams then scroll sideways.
    const vb = out.match(/viewBox="[-\d.]+ [-\d.]+ ([\d.]+) [\d.]+"/)
    svg.value = vb ? out.replace('width="100%"', `width="${Math.ceil(+vb[1])}"`) : out
    failed.value = false
  } catch (e) {
    console.error('Mermaid diagram failed to render', e)
    failed.value = true
  }
}

onMounted(draw)
watch(isDark, draw)

// Click a diagram to see it full size; Esc or a click closes it
const zoomed = ref(false)
const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') zoomed.value = false }
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <template v-if="svg && !failed">
    <button type="button" class="mermaid-diagram" title="Click to view full size" @click="zoomed = true" v-html="svg" />
    <Teleport to="body">
      <div v-if="zoomed" class="mermaid-zoom" role="dialog" aria-label="Diagram, full size" @click="zoomed = false">
        <div class="mermaid-zoom-inner" v-html="svg" />
        <span class="mermaid-zoom-hint">Press Esc or click to close</span>
      </div>
    </Teleport>
  </template>
  <!-- Shown before the diagram renders, without JavaScript, and if rendering fails -->
  <div v-else class="language-mermaid"><pre><code>{{ source }}</code></pre></div>
</template>

<style scoped>
/* In the page: fit the column so nothing is cut off */
.mermaid-diagram {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 16px 0;
  padding: 0;
  border: 0;
  background: none;
  cursor: zoom-in;
}
.mermaid-diagram :deep(svg) {
  max-width: 100% !important;
  height: auto;
}
/* Full size: the diagram's natural width, scrollable if larger than the screen */
.mermaid-zoom {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: flex;
  flex-direction: column;
  align-items: safe center;
  justify-content: safe center;
  gap: 12px;
  padding: 32px;
  overflow: auto;
  background: rgba(0, 0, 0, 0.75);
  cursor: zoom-out;
}
.mermaid-zoom-inner {
  padding: 24px;
  border-radius: 12px;
  background: var(--vp-c-bg);
}
.mermaid-zoom-inner :deep(svg) {
  max-width: none !important;
  height: auto;
}
.mermaid-zoom-hint {
  color: #fff;
  font-size: 13px;
  opacity: 0.8;
}
/* VitePress gives every <p> in a page a margin and 28px line height; Mermaid labels are <p>s, so reset them */
.mermaid-diagram :deep(foreignObject p),
.mermaid-diagram :deep(foreignObject div),
.mermaid-diagram :deep(foreignObject span),
.mermaid-zoom :deep(foreignObject p),
.mermaid-zoom :deep(foreignObject div),
.mermaid-zoom :deep(foreignObject span) {
  margin: 0;
  line-height: 1.5;
}
.language-mermaid pre {
  padding: 16px 20px;
  background: var(--vp-code-block-bg);
  border-radius: 8px;
  overflow-x: auto;
  font-size: 14px;
}
</style>
