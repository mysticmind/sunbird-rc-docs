// Refresh the vendored OpenAPI specs from sunbird-rc-core.
// Usage: npm run sync-openapi [-- <branch>]   (default branch: main)
import { writeFile } from 'node:fs/promises'

const branch = process.argv[2] ?? 'main'
const specs = ['issue-api', 'identity-api', 'schema-api']
const base = `https://raw.githubusercontent.com/Sunbird-RC/sunbird-rc-core/${branch}/api-documentation`

for (const name of specs) {
  const res = await fetch(`${base}/${name}.yaml`)
  if (!res.ok) throw new Error(`${name}.yaml: HTTP ${res.status}`)
  await writeFile(new URL(`../openapi/${name}.yaml`, import.meta.url), await res.text())
  console.log(`updated openapi/${name}.yaml from ${branch}`)
}
