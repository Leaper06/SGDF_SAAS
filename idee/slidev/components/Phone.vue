<script setup>
// Capture d'écran affichée dans un cadre de téléphone
defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: '' },
  height: { type: String, default: '24rem' }
})
</script>

<template>
  <figure class="phone-figure">
    <div class="phone" :style="{ height }">
      <img :src="src" :alt="alt" />
    </div>
  </figure>
</template>

<style scoped>
.phone-figure {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0;
}
.phone {
  aspect-ratio: 390 / 844;
  border: 6px solid #1f2937;
  border-radius: 1.6rem;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.22);
}
.phone img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top;
  display: block;
}
</style>
