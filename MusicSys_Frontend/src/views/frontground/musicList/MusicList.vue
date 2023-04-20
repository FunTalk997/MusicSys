<script setup lang="ts">
import request from "@/api/request";
import eventBus from "@/views/frontground/components/event-bus";
import { ElMessage } from "element-plus";
import Cookies from "js-cookie";

const userInfo = ref(null) as any;
const getUserInfo = async () => {
  const userToken = Cookies.get("userToken");
  if (userToken) {
    await request({
      url: "userInfo/",
      params: { token: userToken },
    }).then((res) => {
      if (res.data.meta.status === 200) {
        userInfo.value = res.data.data;
      }
    });
  }
};
getUserInfo();

const dataList = ref([]);
const total = ref(0);
const queryForm = ref({
  songName: "",
  singer: "",
  album: "",
  pageNum: 1,
  pageSize: 20,
});

const initDataList = async () => {
  await request({
    url: "music/",
    params: queryForm.value,
  }).then((res) => {
    dataList.value = res.data.data["songs"];
    total.value = res.data.data["total"];
  });
};
initDataList();

// 搜索
const handleSearch = () => {
  initDataList();
};

// 重置
const handleReset = () => {
  queryForm.value.songName = "";
  queryForm.value.singer = "";
  queryForm.value.album = "";
  initDataList();
};

// 播放音乐
const handlePlayList = (row: any) => {
  eventBus.emit("playList", { dataList, row });
};

// 添加音乐到播放列表
const handleAddPlayList = (row: any) => {
  eventBus.emit("addPlayList", row);
};

// 添加音乐到收藏列表
const handleCollect = async (row: any) => {
  await request({
    url: "collect/",
    method: "post",
    data: {
      user_id: userInfo.value.id,
      music_id: row.id,
    },
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

// 分页
const handleCurrentChange = (pageNum: number) => {
  queryForm.value.pageNum = pageNum;
  initDataList();
};
</script>

<template>
  <el-card>
    <template #header>
      <span>歌曲列表</span>
    </template>
    <div class="search">
      <el-input
        v-model="queryForm.songName"
        placeholder="搜索歌曲名"
        style="width: 150px"
        size="default"
      >
        <template #prefix>
          <el-icon><i-ep-Search /></el-icon>
        </template>
      </el-input>
      <el-input
        v-model="queryForm.singer"
        placeholder="搜索歌手"
        style="width: 150px"
        size="default"
      >
        <template #prefix>
          <el-icon><i-ep-Search /></el-icon>
        </template>
      </el-input>
      <el-input
        v-model="queryForm.album"
        placeholder="搜索专辑"
        style="width: 150px"
        size="default"
      >
        <template #prefix>
          <el-icon><i-ep-Search /></el-icon>
        </template>
      </el-input>
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button @click="handleReset">重置</el-button>
    </div>
    <el-table :data="dataList" border style="width: 100%">
      <el-table-column prop="songName" label="歌曲名称" />
      <el-table-column prop="singer" label="歌手" />
      <el-table-column prop="album" label="专辑" />
      <el-table-column prop="songTime" label="歌曲时长" width="100" />
      <el-table-column prop="lyricist" label="作词" />
      <el-table-column prop="addTime" label="添加时间" width="180" />
      <el-table-column fixed="right" label="操作" width="150">
        <template #default="{ row }" style="display: flex">
          <div class="operate">
            <el-icon @click="handlePlayList(row)"><i-ep-VideoPlay /></el-icon>
            <el-icon @click="handleAddPlayList(row)"
              ><i-ep-CirclePlus
            /></el-icon>
            <el-icon @click="handleCollect(row)"><i-ep-Star /></el-icon>
            <router-link :to="'/detail/' + row.id"
              ><el-icon><i-ep-View /></el-icon
            ></router-link>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="queryForm.pageNum"
      :page-size="queryForm.pageSize"
      layout="total, prev, pager, next, jumper"
      :total="total"
      @current-change="handleCurrentChange"
    />
  </el-card>
</template>

<style scoped lang="less">
.search * + * {
  margin-left: 10px;
}

.el-table {
  margin-top: 10px;
}

.operate {
  display: flex;
  justify-content: center;

  .el-icon {
    cursor: pointer;
  }

  * + * {
    margin-left: 10px;
  }
}
</style>
