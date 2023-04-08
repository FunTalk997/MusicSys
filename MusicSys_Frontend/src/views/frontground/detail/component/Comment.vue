<script setup lang="ts">
import request from "@/api/request";
import { ElMessage } from "element-plus";
import Cookies from "js-cookie";
import { useRoute } from "vue-router";

const route = useRoute();

const userInfo = ref({}) as any;
const music_id = route.params.id;
const dataList = ref([]) as any;
const total = ref();
const form = ref({
  user_id: "",
  music_id: music_id,
  comment: "",
});

const getUser_ID = async () => {
  const userToken = Cookies.get("userToken");
  if (userToken) {
    await request({
      url: "userInfo/",
      params: { token: userToken },
    }).then((res) => {
      if (res.data.meta.status === 200) {
        userInfo.value = res.data.data;
        form.value.user_id = res.data.data["id"];
      }
    });
  }
};
getUser_ID();

const initDataList = async () => {
  await request({
    url: "music/comment/",
    params: { music_id: music_id },
  }).then((res) => {
    if (res.data.meta["status"] === 200) {
      dataList.value = res.data.data["comment"];
      total.value = res.data.data["total"];
    }
  });
};
initDataList();

const handleSubmit = async () => {
  await request({
    url: "comment/",
    method: "post",
    data: form.value,
  }).then((res) => {
    if (res.data.meta["status"] === 201) {
      ElMessage({
        type: "success",
        message: "评论成功",
      });
      initDataList();
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
    <div class="comment-wrap">
      <h1>评论</h1>
      <hr />
      <div class="comment-input">
        <el-image :src="userInfo.iconUrl" />
        <el-input type="textarea" v-model="form.comment"></el-input>
        <el-button type="primary" @click="handleSubmit">评论</el-button>
      </div>
      <h5 style="margin: 50px 0 0 0">最新评论</h5>
      <hr />
      <div class="comments">
        <div class="cmt-wrap" v-for="item in dataList">
          <el-image :src="item.iconUrl" />
          <div class="cmt">
            <span>{{ item.username }}</span>
            <span>{{ item.comment }}</span>
            <span>{{ item.addTime }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="less">
.main-wrap {
  margin-top: 50px;
  display: flex;
  justify-content: center;
}

.comment-wrap {
  width: 80%;
}

.el-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.comment-input {
  margin-top: 20px;
  display: flex;

  > * + * {
    margin-left: 10px;
  }
}

.cmt-wrap {
  display: flex;
  align-items: center;
  margin-top: 10px;

  .cmt {
    display: flex;
    flex-direction: column;
    margin-left: 10px;

    > * + * {
      margin-top: 10px;
    }
  }
}
</style>
