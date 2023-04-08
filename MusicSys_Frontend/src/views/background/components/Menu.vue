<script setup lang="ts">
import { useRoute } from "vue-router";

const route = useRoute();

const activeIndex = ref(route.path.replace("/admin/", ""));
</script>

<template>
  <div class="item-wrap">
    <div class="logo-wrap">
      <img src="@/assets/logo.jpg" alt="" />
      <span>音乐后台管理系统</span>
    </div>
    <div class="menu-wrap">
      <el-scrollbar>
        <el-menu :default-active="activeIndex" router>
          <el-menu-item index="index" @click="activeIndex = 'index'">
            <el-icon><i-ep-House /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="musicList" @click="activeIndex = 'musicList'">
            <el-icon><i-ep-Mic /></el-icon>
            <span>歌曲列表</span>
          </el-menu-item>
          <el-menu-item index="collect" @click="activeIndex = 'collect'">
            <el-icon><i-ep-Star /></el-icon>
            <span>收藏列表</span>
          </el-menu-item>
          <el-menu-item index="comment" @click="activeIndex = 'comment'">
            <el-icon><i-ep-Comment /></el-icon>
            <span>评论列表</span>
          </el-menu-item>
          <el-menu-item index="userList" @click="activeIndex = 'userList'">
            <el-icon><i-ep-User /></el-icon>
            <span>用户列表</span>
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
    </div>
  </div>
</template>

<style scoped lang="less">
.logo-wrap {
  display: flex;
  align-items: center;
  padding-top: 10px;
  padding-bottom: 20px;

  > img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-left: 6px;
  }

  > span {
    margin-left: 10px;
  }
}
</style>
