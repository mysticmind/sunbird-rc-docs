<script setup lang="ts">
// COSS and Digital Public Good badges, pinned to the bottom-right corner of every page.
// COSS mark: coss.org.in logo, cropped to the square (the name under it is unreadable at this size).
// DPG badge: digitalpublicgoods.net, shown unaltered as the DPGA brand guide asks.
import { withBase } from 'vitepress'
</script>

<template>
  <div class="corner-badges">
    <a
      class="badge coss"
      href="https://www.coss.org.in/"
      target="_blank"
      rel="noopener"
      title="Sunbird RC is developed by the Centre for Open Societal Systems (COSS)"
    >
      <img :src="withBase('/images/coss-mark.svg')" alt="Centre for Open Societal Systems (COSS)" width="44" height="44" />
    </a>
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
  display: flex;
  flex-direction: column;
  align-items: flex-end;
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
  width: 44px;
  height: 44px;
  border-radius: 4px;
}
.dpg img {
  width: 88px;
  height: auto;
}
@media (max-width: 640px) {
  .corner-badges { right: 12px; bottom: 12px; gap: 6px; }
  .coss img { width: 36px; height: 36px; }
  .dpg img { width: 72px; }
}
@media print {
  .corner-badges { display: none; }
}
</style>
