<script setup lang="ts">
// "Digital Public Good" banner, rebuilt from the GitBook page cover so it stays sharp and readable.
import { withBase } from 'vitepress'

defineProps<{ compact?: boolean }>()
</script>

<template>
  <section class="rc-banner" :class="{ 'rc-banner--compact': compact }" aria-label="About Sunbird RC">
    <img class="rc-banner-logo" :src="withBase('/logo.png')" alt="Sunbird" />
    <div class="rc-banner-text">
      <h2 class="rc-banner-title">
        <span class="rc-label rc-label-tilt">Digital Public Good for</span>
        <span class="rc-label">Registry and Verifiable Credentialing</span>
      </h2>
      <p class="rc-banner-desc">
        Open source Registry and Credentialing infrastructure for quickly deploying configurable Registries and for
        issuing, verifying and managing digital credentials.
      </p>
    </div>
  </section>
</template>

<style scoped>
.rc-banner {
  display: grid;
  grid-template-columns: minmax(160px, 30%) 1fr;
  align-items: center;
  gap: 32px;
  padding: 40px 48px;
  border-radius: 28px;
  background: linear-gradient(135deg, #e8b37c 0%, #e2a76f 100%);
  box-shadow: 0 10px 30px rgba(165, 82, 54, 0.18);
}
.rc-banner-logo {
  width: 100%;
  max-width: 300px;
  justify-self: center;
}
.rc-banner-text {
  min-width: 0;
  text-align: center;
}
.rc-banner-title {
  margin: 0 0 16px;
  padding: 0;
  border: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: clamp(18px, 2.4vw, 28px);
  font-weight: 800;
  line-height: 1.25;
  letter-spacing: 0.01em;
}
.rc-label {
  display: inline-block;
  max-width: 100%;
  box-sizing: border-box;
  padding: 4px 18px;
  background: #fb7600;
  color: #fff;
}
.rc-label-tilt {
  transform: rotate(-1.2deg);
}
/* The original cover used white text here; dark brown keeps it readable on the peach background. */
.rc-banner-desc {
  margin: 0 auto;
  max-width: 640px;
  color: #4a2414;
  font-size: clamp(15px, 1.5vw, 18px);
  line-height: 1.6;
}
.rc-banner--compact {
  grid-template-columns: 1fr;
  gap: 20px;
  padding: 36px 32px;
}
.rc-banner--compact .rc-banner-logo {
  max-width: 230px;
}
.rc-banner--compact .rc-banner-title {
  font-size: clamp(18px, 1.9vw, 23px);
}
.rc-banner--compact .rc-banner-desc {
  font-size: 16px;
}
@media (max-width: 720px) {
  .rc-banner {
    grid-template-columns: 1fr;
    padding: 28px 20px;
    gap: 20px;
  }
  .rc-banner-logo {
    max-width: 200px;
  }
}
</style>
