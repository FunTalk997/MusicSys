<script setup lang="ts">
import Header from "@/views/background/components/Header.vue";
import Menu from "@/views/background/components/Menu.vue";
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
</template>

<style scoped lang="less">
.el-container {
  height: 100%;
}

.el-main {
  background-color: #f0f0f0;
}
</style>
