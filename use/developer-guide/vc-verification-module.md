---
title: "VC Verification Module"
---

# VC Verification Module

A common library for VC verification, usable across Sunbird RC frontends. Scans QR codes inside Angular apps.

<a href="https://github.com/Sunbird-RC/vc-verification" class="button primary" data-icon="github">View the source on GitHub</a>

::::: steps
::: step
### Install the library

```bash
npm i vc-verification
```
:::

::: step
### Install the scanner

The deprecated `ngx-scanner` integration was removed starting from `vc-verification@0.0.13`. Install `@zxing/ngx-scanner` separately, matching your Angular version:

```bash
npm i @zxing/ngx-scanner@vx.x.x
```

| Angular Version                   | ngx-scanner version |
| --------------------------------- | ------------------- |
| 9.0.0 – <10                       | 3.0.0, 3.0.1        |
| 10.1.5                            | 3.1.0 – 3.1.3       |
| 11.2.11 \|\| ^12.0.4              | 3.2.0, 3.3.0        |
| 11.2.11 \|\| ^12.0.4 \|\| ^13.0.0 | 3.4.2, 3.5.0        |

For anything beyond this table, check compatibility directly against the [`ngx-scanner` README](https://github.com/zxing-js/ngx-scanner#readme).
:::

:::: step
### Add the zbar-wasm script

```html [index.html]
<script src="https://cdn.jsdelivr.net/npm/@undecaf/zbar-wasm@0.9.12/dist/index.js"></script>
```
::::

:::: step
### Wire up the module

```typescript [app.module.ts]
import { VerifyModule } from 'vc-verification';
import { ZXingScannerModule } from '@zxing/ngx-scanner'; // not required >=0.0.13
import * as configData from '../assets/config.json';

@NgModule({
  imports: [
    VerifyModule.forChild(configData),
    ZXingScannerModule, // not required >=0.0.13
  ],
})
export class AppModule {}
```
::::
:::::

## Using the module

:::: tabs
== Default scan template

Drop `<sb-vc-verification></sb-vc-verification>` into `app.component.html`.

To customize labels/messages, pass an `item` input (`showResult` array of `{title, path}` entries, plus copy strings like `scanNote`, `certificateTitle`, etc.).

From v10, `showResult` entries also support a `type: 'date'` formatter and a `removeStr` value-stripping option.

== Service directly

For a fully custom UI, import `VerifyService` from `'verify-module'` and call `scanSuccessHandler(event)`.

Available methods:

* `enableScanner()` — toggle scanner visibility
* `scanSuccessHandler($event)` — verify scanned data
::::

## Scanners

| Scanner        | Default in    | Notes                                        |
| -------------- | ------------- | -------------------------------------------- |
| `ZXING_QRCODE` | pre-0.0.13    | Deprecated; struggles with large-payload QRs |
| `ZBAR_QRCODE`  | 0.0.13 onward | Handles large payloads better                |

Set via the `scanner_type` property. Override `.vc-btnPrimary` in your stylesheet to change the button color.
