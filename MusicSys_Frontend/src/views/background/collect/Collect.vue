<script setup lang="ts">
import request from "@/api/request";
import { ElMessage, ElMessageBox } from "element-plus";

const dataList = ref([]);
const total = ref(0);
const queryForm = ref({
  username: "",
  songName: "",
  singer: "",
  album: "",
  pageNum: 1,
  pageSize: 20,
});

// 表格行选择框
const multipleSelection = ref([]);
const handleSelectionChange = (val: any) => {
  multipleSelection.value = val;
};

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

// 删除（单条数据）
const handleDelete = (row: any) => {
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

// 删除（多条数据）
const handleDeletes = async () => {
  ElMessageBox.confirm("确认删除", "Warning", {
    confirmButtonText: "确认",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      const ids = {
        id: [],
      };
      for (const item of multipleSelection.value) {
        (ids.id as any).push((item as any).id);
      }
      await request({
        url: "collect/",
        method: "delete",
        data: ids,
      });
      initDataList();
      ElMessage({
        type: "success",
        message: "删除成功",
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
      <span>收藏列表</span>
    </template>
    <div class="search">
      <el-input
        v-model="queryForm.username"
        placeholder="搜索用户名"
        style="width: 150px"
        size="default"
      >
        <template #prefix>
          <el-icon><i-ep-Search /></el-icon>
        </template>
      </el-input>
      <el-input
        v-model="queryForm.songName"
        placeholder="搜索歌曲名称"
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
    <el-table
      :data="dataList"
      border
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="username" label="用户名" width="150" />
      <el-table-column prop="songName" label="歌曲名称" />
      <el-table-column prop="singer" label="歌手" />
      <el-table-column prop="album" label="专辑" />
      <el-table-column prop="songTime" label="歌曲时长" />
      <el-table-column prop="addTime" label="添加时间" width="180" />
      <el-table-column fixed="right" label="操作" width="150">
        <template #default="{ row }" style="display: flex">
          <div class="operate-row">
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
.search * + * {
  margin-left: 10px;
}

.el-table {
  margin-top: 10px;
}

.operate-row {
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
