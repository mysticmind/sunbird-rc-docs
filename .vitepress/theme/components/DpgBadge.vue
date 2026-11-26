<script setup lang="ts">
// Digital Public Good badge, pinned to the bottom-right corner of every page.
// Badge image: digitalpublicgoods.net (shown unaltered, as the DPGA brand guide asks).
import { withBase } from 'vitepress'
</script>

<template>
  <a
    class="dpg-badge"
    href="https://www.digitalpublicgoods.net/r/sunbird-rc"
    target="_blank"
    rel="noopener"
    title="Sunbird RC is a recognised Digital Public Good"
  >
    <img :src="withBase('/images/dpg-badge.png')" alt="Digital Public Good: view Sunbird RC in the DPG Registry" width="88" height="42" />
  </a>
</template>

<style scoped>
.dpg-badge {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 30; /* above page content, below the nav bar and search dialog */
  display: block;
  line-height: 0;
  transition: transform 0.2s;
}
.dpg-badge:hover {
  transform: translateY(-2px);
}
.dpg-badge img {
  width: 88px;
  height: auto;
}
@media (max-width: 640px) {
  .dpg-badge { right: 12px; bottom: 12px; }
  .dpg-badge img { width: 72px; }
}
@media print {
  .dpg-badge { display: none; }
}
</style>
