---
title: "~Custom QR Code design~"
---

# \~Custom QR Code design\~

::: danger
**Removed — directory doesn't exist.** This page describes configuring a custom QR-styling canvas via a `certificate-api` service, `ENABLE_CUSTOM_QR_CODE_CANVAS`, and a `qr_code_config.json` file. None of this exists in the current `sunbird-rc-core` codebase — there's no `certificate-api` service, no such env flag, and no styling config anywhere in the repo. QR generation today happens inside `credentials-service` (`rendering.utils.service.ts`), using the plain `qrcode` npm package with no styling hook. This page needs new content once/if custom QR styling is reintroduced — not a link fix.
:::

