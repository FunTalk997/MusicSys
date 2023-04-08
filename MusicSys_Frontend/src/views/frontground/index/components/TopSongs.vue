<script setup lang="ts">
import request from "@/api/request";

const dataList = ref([]) as any;

const initDataList = async () => {
  await request({
    url: "topSongs/",
  }).then((res) => {
    if (res.data.meta["status"] === 200) {
      dataList.value = res.data.data;
    }
  });
};
initDataList();
</script>

<template>
  <div class="top-songs">
    <h1>Top Songs</h1>
    <div class="top-songs-list">
      <div class="top-song-card" v-for="(item, index) of dataList">
        <div class="top-song-item">
          <router-link :to="'/detail/' + item.id"
            ><el-image :src="item.picUrl"
          /></router-link>

          <div class="top-song-content">
            <h4 class="top-song-title">
              <router-link :to="'/detail/' + item.id">{{
                item.songName
              }}</router-link>
            </h4>
            <a>{{ item.singer }}</a>
          </div>
        </div>
        <div class="top-song-rank">
          <span>{{ index + 1 }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.top-song-card {
  background-color: #ffffff;
  border: 1px solid #d3d3d3;
  display: flex;
  justify-content: space-between;
  height: 80px;
}

.top-song-item {
  display: flex;
  align-items: center;
}

.el-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-left: 10px;
}

.top-song-content {
  margin-left: 20px;

  h4 {
    margin: 0;
  }

  > a {
    color: #999;
    font-size: 12px;
  }
}

.top-song-rank {
  margin-right: 10px;
  display: flex;
  align-items: center;
  > span {
    font-size: 30px;
  }
}
</style>
