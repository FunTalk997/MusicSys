<script setup lang="ts">
import Carousel from "@/views/frontground/index/components/Carousel.vue";
import NewSongs from "@/views/frontground/index/components/NewSongs.vue";
import TopSongs from "@/views/frontground/index/components/TopSongs.vue";
</script>

<template>
  <div class="item-wrap">
    <div class="carousel-wrap">
      <Carousel />
    </div>
    <div class="list-wrap">
      <NewSongs style="width: 65%" />
      <TopSongs style="width: 35%" />
    </div>
  </div>
</template>

<style scoped lang="less">
.list-wrap {
  display: flex;
}
</style>
