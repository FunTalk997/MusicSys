<script setup lang="ts">
import Password from "@/views/frontground/components/Password.vue";
import { useRouter } from "vue-router";
import eventBus from "./event-bus";
import Cookies from "js-cookie";
import request from "@/api/request";

const router = useRouter();
const dialogVisible = ref(false);
const userInfo = ref({}) as any;

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

const goToIndex = (index: string) => {
  router.push(index);
};

const editPwd = () => {
  dialogVisible.value = true;
};

const logout = () => {
  eventBus.emit("logout");
  Cookies.remove("userToken");
  router.replace("/login");
};
</script>

<template>
  <div class="item-wrap">
    <div class="user-wrap">
      <el-image :src="userInfo.iconUrl" />
      <el-dropdown>
        <span class="username-wrap">
          {{ userInfo.username
          }}<el-icon><i-ep-ArrowDown></i-ep-ArrowDown></el-icon>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="goToIndex('/profile')"
              >个人信息</el-dropdown-item
            >
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

.user-wrap {
  display: flex;
  align-items: center;

  .username-wrap {
    margin-left: 10px;
  }
}

.el-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
</style>
