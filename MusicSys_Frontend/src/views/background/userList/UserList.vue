<script setup lang="ts">
import request from "@/api/request";
import { ElMessage, ElMessageBox } from "element-plus";
import Dialog from "./component/Dialog.vue";
import { isNull } from "@/utils/filter";

const dialogVisible = ref(false);
const dialogTitle = ref("");
const dialogTableValue = ref({});

const dataList = ref([]);
const total = ref(0);
const queryForm = ref({
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
    url: "user/",
    params: queryForm.value,
  }).then((res) => {
    dataList.value = res.data.data["user"];
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

// 添加编辑
const handleDialog = (row?: any) => {
  dialogTitle.value = "新增用户";
  dialogTableValue.value = {};
  dialogVisible.value = true;
};

// 重置密码(单条数据)
const handleResetPwd = (row: any) => {
  ElMessageBox.confirm("确认重置密码", "Warning", {
    confirmButtonText: "确认",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await request({
        url: "userPwd/",
        method: "put",
        data: row,
      });
      ElMessage({
        type: "success",
        message: "密码重置成功",
      });
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "取消重置密码",
      });
    });
};

// 重置密码(多条数据)
const handleResetPwds = () => {
  ElMessageBox.confirm("确认重置密码", "Warning", {
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
        url: "userPwd/",
        method: "put",
        data: ids,
      });
      ElMessage({
        type: "success",
        message: "密码重置成功",
      });
    })
    .catch(() => {
      ElMessage({
        type: "info",
        message: "取消重置密码",
      });
    });
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
        url: "user/",
        method: "delete",
        data: row,
      });
      ElMessage({
        type: "success",
        message: "删除成功",
      });
      initDataList();
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
        url: "user/",
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
      <span>用户列表</span>
    </template>
    <div class="search">
      <el-input
        v-model="queryForm.songName"
        placeholder="搜索用户名"
        style="width: 150px"
        size="default"
      >
        <template #prefix>
          <el-icon><i-ep-Search /></el-icon>
        </template>
      </el-input>
      <el-input
        v-model="queryForm.singer"
        placeholder="搜索昵称"
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
    <div class="operate">
      <el-button type="success" @click="handleDialog()"
        ><i-ep-Plus />新增</el-button
      >
      <el-button type="warning" @click="handleResetPwds"
        ><i-ep-Refresh />重置密码</el-button
      >
      <el-button type="danger" @click="handleDeletes"
        ><i-ep-Delete />批量删除</el-button
      >
    </div>
    <el-table
      :data="dataList"
      border
      style="width: 100%"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="username" label="用户名" width="150" />
      <el-table-column prop="nickname" label="昵称" width="150" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="addTime" label="创建时间" width="180" />
      <el-table-column prop="loginTime" label="登录时间" width="180" />
      <el-table-column fixed="right" label="操作" width="150">
        <template #default="{ row }" style="display: flex">
          <div class="operate-row">
            <el-icon @click="handleDelete(row)"><i-ep-Delete /></el-icon>
            <el-icon @click="handleResetPwd(row)"><i-ep-Refresh /></el-icon>
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
  <Dialog
    v-model:dialog-visible="dialogVisible"
    v-if="dialogVisible"
    :dialog-title="dialogTitle"
    :dialog-table-value="dialogTableValue"
    @initDataList="initDataList"
  />
</template>

<style scoped lang="less">
.search * + * {
  margin-left: 10px;
}

.operate {
  margin-top: 10px;
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
