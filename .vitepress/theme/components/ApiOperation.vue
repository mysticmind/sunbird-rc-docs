<script setup lang="ts">
// Renders one operation from an OpenAPI spec in /openapi, replacing GitBook's {% openapi %} block.
// Usage in Markdown: <ApiOperation spec="issue-api" path="/credentials/issue" method="post" />
import { computed } from 'vue'
import yaml from 'js-yaml'

const props = defineProps<{ spec: string; path: string; method: string }>()

const raw = import.meta.glob('../../../openapi/*.yaml', { query: '?raw', import: 'default', eager: true }) as Record<string, string>
const specs: Record<string, any> = {}
for (const [file, text] of Object.entries(raw)) {
  specs[file.split('/').pop()!.replace(/\.yaml$/, '')] = yaml.load(text)
}

function resolve(node: any, doc: any, seen = new Set<string>()): any {
  if (!node || typeof node !== 'object') return node
  if (node.$ref) {
    if (seen.has(node.$ref)) return { type: 'object', description: `(recursive ${node.$ref})` }
    const target = node.$ref.replace(/^#\//, '').split('/').reduce((o: any, k: string) => o?.[k], doc)
    return resolve(target, doc, new Set([...seen, node.$ref]))
  }
  if (Array.isArray(node)) return node.map((n) => resolve(n, doc, seen))
  return Object.fromEntries(Object.entries(node).map(([k, v]) => [k, resolve(v, doc, seen)]))
}

const doc = computed(() => specs[props.spec])
const op = computed(() => {
  const d = doc.value
  const o = d?.paths?.[props.path]?.[props.method.toLowerCase()]
  return o ? resolve(o, d) : null
})
const server = computed(() => doc.value?.servers?.[0]?.url ?? '')

type Row = { name: string; type: string; required: boolean; description: string; depth: number }
function flatten(schema: any, depth = 0, prefix = ''): Row[] {
  if (!schema || depth > 4) return []
  const s = schema.type === 'array' ? schema.items ?? {} : schema
  const req = new Set<string>(s.required ?? [])
  return Object.entries(s.properties ?? {}).flatMap(([name, p]: [string, any]) => [
    {
      name: prefix + name,
      type: p.type === 'array' ? `array of ${p.items?.type ?? 'object'}` : p.type ?? (p.properties ? 'object' : ''),
      required: req.has(name),
      description: p.description ?? (p.enum ? `One of: ${p.enum.join(', ')}` : ''),
      depth,
    },
    ...flatten(p, depth + 1, prefix + name + (p.type === 'array' ? '[].' : '.')),
  ])
}

function example(schema: any, depth = 0): any {
  if (!schema || depth > 6) return null
  if (schema.example !== undefined) return schema.example
  if (schema.type === 'array') return [example(schema.items, depth + 1)]
  if (schema.type === 'object' || schema.properties)
    return Object.fromEntries(Object.entries(schema.properties ?? {}).map(([k, v]) => [k, example(v, depth + 1)]))
  return { string: 'string', integer: 0, number: 0, boolean: true }[schema.type as string] ?? null
}

const body = computed(() => {
  const content = op.value?.requestBody?.content ?? {}
  const [type, media] = Object.entries(content)[0] ?? []
  return media ? { type, schema: (media as any).schema, required: op.value.requestBody.required } : null
})
const responses = computed(() =>
  Object.entries(op.value?.responses ?? {}).map(([code, r]: [string, any]) => {
    const media: any = Object.values(r.content ?? {})[0]
    return { code, description: r.description ?? '', schema: media?.schema, example: media?.example ?? example(media?.schema) }
  })
)
const pretty = (v: any) => JSON.stringify(v, null, 2)
</script>

<template>
  <div class="api-op">
    <div v-if="!op" class="api-missing">
      Operation <code>{{ method.toUpperCase() }} {{ path }}</code> not found in <code>openapi/{{ spec }}.yaml</code>.
    </div>
    <template v-else>
      <div class="api-head">
        <span class="api-method" :class="method.toLowerCase()">{{ method.toUpperCase() }}</span>
        <code class="api-path">{{ path }}</code>
      </div>
      <p v-if="op.summary" class="api-summary">{{ op.summary }}</p>
      <p v-if="op.description" class="api-desc">{{ op.description }}</p>
      <p v-if="server" class="api-server">Server: <code>{{ server }}</code></p>

      <template v-if="op.parameters?.length">
        <h4>Parameters</h4>
        <table>
          <thead><tr><th>Name</th><th>In</th><th>Type</th><th>Description</th></tr></thead>
          <tbody>
            <tr v-for="p in op.parameters" :key="p.in + p.name">
              <td><code>{{ p.name }}</code><span v-if="p.required" class="api-req">*</span></td>
              <td>{{ p.in }}</td>
              <td>{{ p.schema?.type ?? p.type ?? '' }}</td>
              <td>{{ p.description ?? '' }}</td>
            </tr>
          </tbody>
        </table>
      </template>

      <template v-if="body">
        <h4>Request body <span class="api-ctype">{{ body.type }}</span></h4>
        <table v-if="flatten(body.schema).length">
          <thead><tr><th>Field</th><th>Type</th><th>Description</th></tr></thead>
          <tbody>
            <tr v-for="r in flatten(body.schema)" :key="r.name">
              <td><code>{{ r.name }}</code><span v-if="r.required" class="api-req">*</span></td>
              <td>{{ r.type }}</td>
              <td>{{ r.description }}</td>
            </tr>
          </tbody>
        </table>
        <details class="api-example">
          <summary>Example request</summary>
          <div class="language-json"><pre><code>{{ pretty(example(body.schema)) }}</code></pre></div>
        </details>
      </template>

      <h4>Responses</h4>
      <details v-for="r in responses" :key="r.code" class="api-response">
        <summary>
          <span class="api-code" :class="'c' + r.code[0]">{{ r.code }}</span> {{ r.description }}
        </summary>
        <div v-if="r.example" class="language-json"><pre><code>{{ pretty(r.example) }}</code></pre></div>
        <p v-else class="api-desc">No response body.</p>
      </details>
    </template>
  </div>
</template>

<style scoped>
.api-op { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 16px 20px; margin: 24px 0; }
.api-head { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.api-method { font-weight: 700; font-size: 13px; padding: 2px 8px; border-radius: 4px; color: #fff; background: #6b7280; }
.api-method.get { background: #2563eb; }
.api-method.post { background: #16a34a; }
.api-method.put, .api-method.patch { background: #d97706; }
.api-method.delete { background: #dc2626; }
.api-path { font-size: 15px; }
.api-summary { font-weight: 600; margin: 12px 0 4px; }
.api-desc, .api-server { color: var(--vp-c-text-2); margin: 4px 0; }
.api-req { color: #dc2626; margin-left: 2px; }
.api-ctype { font-weight: 400; font-size: 13px; color: var(--vp-c-text-2); margin-left: 6px; }
.api-response, .api-example { margin: 8px 0; }
.api-response summary, .api-example summary { cursor: pointer; }
.api-code { font-weight: 700; font-family: var(--vp-font-family-mono); }
.api-code.c2 { color: #16a34a; }
.api-code.c4 { color: #d97706; }
.api-code.c5 { color: #dc2626; }
.api-op pre { overflow-x: auto; padding: 12px 16px; background: var(--vp-code-block-bg); border-radius: 6px; font-size: 13px; }
.api-missing { color: #dc2626; }
h4 { margin: 20px 0 8px; }
</style>
