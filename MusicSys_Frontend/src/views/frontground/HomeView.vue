<script setup lang="ts">
import Menu from "@/views/frontground/components/Menu.vue";
import Header from "@/views/frontground/components/Header.vue";
import Audio from "@/views/frontground/components/Audio.vue";
</script>

<template>
  <el-container>
    <el-aside width="250px">
      <Menu />
    </el-aside>
    <el-container>
      <el-header>
        <Header />
      </el-header>
      <el-main>
        <!-- 路由占位符 -->
        <router-view />
      </el-main>
    </el-container>
  </el-container>
  <Audio />
</template>

<style scoped lang="less">
.el-container {
  height: 100%;
}

.el-main {
  background-color: #f0f0f0;
}
</style>
