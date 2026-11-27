<script setup lang="ts">
// Digital Public Good badge in the bottom-right corner of every page (COSS is credited in the footer).
// Desktop: fixed to the corner of the screen, so at the end of a page it rests in the footer's corner
// with no jump. Phones: centred at the bottom of the page, since the footer text is full width.
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
  </div>
</template>

<style scoped>
.corner-badges {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 30; /* above page content, below the nav bar and search dialog */
}
.badge {
  display: block;
  line-height: 0;
  transition: transform 0.2s;
}
.badge:hover {
  transform: translateY(-2px);
}
.dpg img {
  width: 88px;
  height: auto;
}
@media (max-width: 640px) {
  .corner-badges { right: 12px; bottom: 12px; }
  .dpg img { width: 72px; }
}
/* Narrow screens: the footer text is full width, so centre the badge at the bottom of the page instead */
@media (max-width: 767px) {
  .corner-badges {
    position: static;
    display: flex;
    justify-content: center;
    padding: 0 0 24px;
  }
}
@media print {
  .corner-badges { display: none; }
}
</style>
