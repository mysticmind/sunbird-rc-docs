<script setup lang="ts">
// COSS and Digital Public Good badges in the bottom-right corner of every page.
// Desktop: fixed to the corner of the screen, so at the end of a page they rest in the footer's corner
// with no jump. Phones: a centred row at the bottom of the page, since the footer text is full width.
// COSS logo: the full coss.org.in logo (mark and name), on a white card so the name reads in dark mode.
// DPG badge: digitalpublicgoods.net, shown unaltered as the DPGA brand guide asks.
import { withBase } from 'vitepress'
</script>

<template>
  <div class="corner-badges">
    <a
      class="badge dpg"
      href="https://www.digitalpublicgoods.net/r/sunbird-rc"
      target="_blank"
      rel="noopener"
      title="Sunbird RC is a recognised Digital Public Good"
    >
      <img :src="withBase('/images/dpg-badge.png')" alt="Digital Public Good: view Sunbird RC in the DPG Registry" width="88" height="42" />
    </a>
    <a
      class="badge coss"
      href="https://www.coss.org.in/"
      target="_blank"
      rel="noopener"
      title="Sunbird RC is developed by the Centre for Open Societal Systems (COSS)"
    >
      <img :src="withBase('/images/coss-logo.svg')" alt="Centre for Open Societal Systems (COSS)" width="72" height="87" />
    </a>
  </div>
</template>

<style scoped>
.corner-badges {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 30; /* above page content, below the nav bar and search dialog */
  display: flex;
  flex-direction: column;
  align-items: center; /* DPG badge on top, COSS mark centred below it */
  gap: 8px;
}
.badge {
  display: block;
  line-height: 0;
  transition: transform 0.2s;
}
.badge:hover {
  transform: translateY(-2px);
}
.coss img {
  width: 72px;
  height: auto;
  padding: 5px;
  box-sizing: content-box;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
}
.dpg img {
  width: 88px;
  height: auto;
}
@media (max-width: 640px) {
  .corner-badges { right: 12px; bottom: 12px; gap: 8px; }
  .coss img { width: 60px; }
  .dpg img { width: 72px; }
}
/* Narrow screens: the footer text is full width, so show a centred row at the bottom of the page instead */
@media (max-width: 767px) {
  .corner-badges {
    position: static;
    flex-direction: row;
    justify-content: center;
    padding: 0 0 24px;
  }
}
@media print {
  .corner-badges { display: none; }
}
</style>
