<template>
  <div v-if="active" class="sort-indicator">
    <div class="sort-arrows">
      <span class="arrow up" :class="{ active: order === 'asc' }">▲</span>
      <span class="arrow down" :class="{ active: order === 'desc' }">▼</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  active: Boolean,
  order: String
})
</script>

<style scoped>
.sort-indicator {
  display: inline-block;
  margin-left: 4px;
  vertical-align: middle;
}

.sort-arrows {
  display: flex;
  flex-direction: column;
  align-items: center;
  line-height: 0.5;
}

.arrow {
  font-size: 0.7em;
  color: rgba(255, 255, 255, 0.5);
  transition: color 0.2s ease;
}

.arrow.active {
  color: white;
}
</style>