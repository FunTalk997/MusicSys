<script setup lang="ts">
// const windowHeight = ref(0);

// const updateWindowHeight = () => {
//   windowHeight.value = window.innerHeight;
// };

// window.addEventListener("resize", updateWindowHeight);

// onMounted(() => {
//   windowHeight.value = window.innerHeight;
// });
</script>

<template>
  <el-card>
    <template #header>
      <span>首页</span>
    </template>
    <div class="hello">
      <h2>欢迎使用 音乐后台管理系统</h2>
      <div class="img">
        <img class="pic" src="@/assets/pic1.jpg" />
        <img class="pic" src="@/assets/pic2.jpg" />
      </div>
    </div>
  </el-card>
</template>

<style scoped lang="less">
.hello {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.img {
  display: flex;
}

.pic {
  width: 50%;
  height: 100%;
}
</style>
