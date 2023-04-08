<script setup lang="ts">
const windowHeight = ref(0);

const updateWindowHeight = () => {
  windowHeight.value = window.innerHeight;
};

window.addEventListener("resize", updateWindowHeight);

onMounted(() => {
  windowHeight.value = window.innerHeight;
});
</script>

<template>
  <el-card>
    <template #header>
      <span>首页</span>
    </template>
    <div class="hello" :style="`height: ${windowHeight - 200}px`">
      <h2>欢迎使用用 音乐后台管理系统</h2>
    </div>
  </el-card>
</template>

<style scoped lang="less">
.hello {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
