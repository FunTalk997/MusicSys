<script setup lang="ts">
import request from "@/api/request";
import { useRoute } from "vue-router";
import eventBus from "@/views/frontground/components/event-bus";
import { ElMessage } from "element-plus";
import Cookies from "js-cookie";

const route = useRoute();

const music_id = route.params.id;
const unfold = ref(false);
const songInfo = ref({}) as any;
const lyric = ref([]);
const collectForm = ref({
  user_id: "",
  music_id: "",
});

const initSongInfo = async () => {
  await request({
    url: "music/detail/",
    params: { id: music_id },
  }).then((res) => {
    if (res.data.meta["status"] === 200) {
      songInfo.value = res.data.data;
      collectForm.value.music_id = res.data.data["id"];
      lyric.value = songInfo.value.lyric.split("\n");
    }
  });
};
initSongInfo();

const getUser_ID = async () => {
  const userToken = Cookies.get("userToken");
  if (userToken) {
    await request({
      url: "userInfo/",
      params: { token: userToken },
    }).then((res) => {
      if (res.data.meta.status === 200) {
        collectForm.value.user_id = res.data.data["id"];
      }
    });
  }
};
getUser_ID();

// 播放音乐
const handlePlay = () => {
  eventBus.emit("play", songInfo);
};

// 添加音乐到播放列表
const handleAddPlayList = () => {
  eventBus.emit("addPlayList", songInfo.value);
};

// 添加音乐到收藏列表
const handleCollect = async () => {
  await request({
    url: "collect/",
    method: "post",
    data: collectForm.value,
  }).then((res) => {
    if (res.data.meta["status"] === 201) {
      ElMessage({
        type: "success",
        message: "收藏成功",
      });
    } else {
      ElMessage({
        type: "error",
        message: res.data.meta["msg"],
      });
    }
  });
};
</script>

<template>
  <div class="main-wrap">
    <div class="info-wrap">
      <el-image class="pic" :src="songInfo.picUrl" />
      <div class="content">
        <h1>{{ songInfo.songName }}</h1>
        <p>
          歌手：<span
            ><RouterLink to="">{{ songInfo.singer }}</RouterLink></span
          >
        </p>
        <p>
          所属专辑：<span
            ><RouterLink to="">{{ songInfo.album }}</RouterLink></span
          >
        </p>
        <div class="operate">
          <el-button-group>
            <el-button size="small" type="primary" @click="handlePlay"
              ><i-ep-VideoPlay />播放</el-button
            >
            <el-button size="small" type="primary" @click="handleAddPlayList"
              ><i-ep-Plus
            /></el-button>
          </el-button-group>
          <el-button
            size="small"
            style="margin-left: 12px"
            @click="handleCollect"
            ><i-ep-Star />收藏</el-button
          >
        </div>
        <div class="lyric-wrap">
          <div class="lyric" v-for="item in lyric ? lyric.slice(0, 12) : ''">
            {{ item }}
            <br />
          </div>
          <div
            style="color: #0c73c2; cursor: pointer"
            v-if="!unfold"
            @click="unfold = !unfold"
          >
            展开<i-ep-ArrowDown />
          </div>

          <div
            :hidden="!unfold"
            class="lyric more"
            v-for="item in lyric ? lyric.slice(13) : ''"
          >
            {{ item }}
            <br />
          </div>
          <div
            style="color: #0c73c2; cursor: pointer"
            v-if="unfold"
            @click="unfold = !unfold"
          >
            收起<i-ep-ArrowUp />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.main-wrap {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}

.info-wrap {
  display: flex;
  width: 50%;
  height: 100%;
}

.pic {
  width: 200px;
  height: 200px;
  margin-right: 50px;
}

.content {
  p {
    margin: 2px 0;
    font-size: 12px;
  }
  a {
    color: #ee30a7;
  }
}

.operate {
  margin-top: 10px;
}

.lyric-wrap {
  margin-top: 10px;

  > div {
    font-size: 14px;
  }
}
</style>
