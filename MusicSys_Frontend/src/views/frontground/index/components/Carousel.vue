<script setup lang="ts">
import request from "@/api/request";

const dataList = ref([]) as any;

const initDataList = async () => {
  await request({
    url: "carousel/",
  }).then((res) => {
    if (res.data.meta["status"] == 200) {
      dataList.value = res.data.data;
    }
  });
};
initDataList();
</script>

<template>
  <el-carousel height="400px">
    <el-carousel-item v-for="item in dataList">
      <router-link :to="'/detail/' + item.id"
        ><el-image :src="item.picUrl" style="width: 100%; height: 100%"
      /></router-link>
    </el-carousel-item>
  </el-carousel>
</template>

<style scoped lang="less">
.el-carousel {
  margin: 0 20px;
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
