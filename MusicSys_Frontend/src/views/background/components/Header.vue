<script setup lang="ts">
import Password from "@/views/background/components/Password.vue";
import Cookies from "js-cookie";
import { useRouter } from "vue-router";

const router = useRouter();
const dialogVisible = ref(false);

const editPwd = () => {
  dialogVisible.value = true;
};

const logout = () => {
  Cookies.remove("adminToken");
  router.replace("/admin/login");
};
</script>

<template>
  <div class="item-wrap">
    <div class="user-wrap">
      <el-icon><i-ep-UserFilled /></el-icon>
      <el-dropdown>
        <span class="el-dropdown-link">
          admin<el-icon><i-ep-ArrowDown></i-ep-ArrowDown></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="editPwd">修改密码</el-dropdown-item>
            <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
  <Password v-model:dialog-visible="dialogVisible" v-if="dialogVisible" />
</template>

<style scoped lang="less">
.item-wrap {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  height: 100%;
}
</style>
