<script setup lang="ts">
import request from "@/api/request";
import eventBus from "@/views/frontground/components/event-bus";
import { ElMessage, ElMessageBox } from "element-plus";

const dataList = ref([]);
const total = ref(0);
const queryForm = ref({
  username: "user01",
  pageNum: 1,
  pageSize: 20,
});

const initDataList = async () => {
  await request({
    url: "collect/",
    params: queryForm.value,
  }).then((res) => {
    dataList.value = res.data.data["collect"];
    total.value = res.data.data["total"];
  });
};
initDataList();

// 播放音乐
const handlePlayList = (row: any) => {
  console.log(row);
  eventBus.emit("playList", { dataList, row });
};

// 添加音乐到播放列表
const handleAddPlayList = (row: any) => {
  eventBus.emit("addPlayList", row);
};

//
const handleDelete = async (row: any) => {
  ElMessageBox.confirm("确认删除", "Warning", {
    confirmButtonText: "确认",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await request({
        url: "collect/",
        method: "delete",
        data: row,
      }).then((res) => {
        if (res.data.meta["status"] === 201) {
          ElMessage({
            type: "success",
            message: "取消收藏成功",
          });
        } else {
          ElMessage({
            type: "error",
            message: res.data.meta["msg"],
          });
        }
      });
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "取消删除",
      });
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
      <span>我的收藏</span>
    </template>
    <el-table :data="dataList" border style="width: 100%">
      <el-table-column prop="songName" label="歌曲名称" />
      <el-table-column prop="singer" label="歌手" />
      <el-table-column prop="album" label="专辑" />
      <el-table-column prop="songTime" label="歌曲时长" width="100" />
      <el-table-column prop="addTime" label="收藏时间" width="180" />
      <el-table-column fixed="right" label="操作" width="150">
        <template #default="{ row }" style="display: flex">
          <div class="options">
            <el-icon @click="handlePlayList(row)"><i-ep-VideoPlay /></el-icon>
            <el-icon @click="handleAddPlayList(row)"
              ><i-ep-CirclePlus
            /></el-icon>
            <el-icon @click="handleDelete(row)"><i-ep-Delete /></el-icon>
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
.el-table {
  margin-top: 10px;
}

.options {
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
