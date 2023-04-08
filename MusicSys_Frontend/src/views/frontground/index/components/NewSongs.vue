<script setup lang="ts">
import request from "@/api/request";

const dataList = ref([]) as any;

const initDataList = async () => {
  await request({
    url: "newSongs/",
  }).then((res) => {
    if (res.data.meta["status"] === 200) {
      dataList.value = res.data.data;
    }
  });
};
initDataList();
</script>

<template>
  <div class="new-songs">
    <h1>New Songs</h1>
    <div class="new-songs-list">
      <div class="new-song-card" v-for="item in dataList">
        <div class="new-song-cover">
          <router-link :to="'/detail/' + item.id"
            ><el-image :src="item.picUrl"
          /></router-link>
        </div>
        <h5 class="new-song-title">
          <router-link :to="'/detail/' + item.id">{{
            item.songName
          }}</router-link>
        </h5>
        <div class="new-song-author">
          <a>{{ item.singer }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.new-songs-list {
  display: flex;
  flex-wrap: wrap;
}

.new-song-card {
  margin-right: 20px;
  margin-bottom: 20px;
}

h5 {
  margin: 0;
}

.el-image {
  width: 150px;
  height: 150px;
}

.new-song-author a {
  color: #999;
  font-size: 10px;
}
</style>
