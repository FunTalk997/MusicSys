<script setup lang="ts">
import request from "@/api/request";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";
import { useRouter } from "vue-router";
import Cookies from "js-cookie";

const router = useRouter();

const loginFormRef = ref<FormInstance>();
const loginForm = ref({
  username: "admin",
  password: "123456",
});
const textType = ref("password");

const loginRules = reactive<FormRules>({
  username: [
    {
      required: true,
      message: "请输入用户名",
      trigger: "blur",
    },
  ],
  password: [
    {
      required: true,
      message: "请输入密码",
      trigger: "blur",
    },
  ],
});

const submitLoginForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      await request({
        url: "adminLogin/",
        method: "post",
        data: loginForm.value,
      }).then((response) => {
        if (response.data.meta.status === 201) {
          const adminToken = response.data.data["token"];
          Cookies.set("adminToken", adminToken);
          router.replace("/admin");
        } else {
          ElMessage({
            type: "error",
            message: response.data.meta.msg,
          });
        }
      });
    } else {
      console.log("error submit!", fields);
    }
  });
};
</script>

<template>
  <div class="main-wrap">
    <div class="login-wrap">
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        status-icon
      >
        <div class="logo-wrap">
          <h1>音乐后台管理系统</h1>
        </div>
        <div class="form-wrap">
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="用户名">
              <template #prefix>
                <el-icon><i-ep-User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              placeholder="密码"
              :type="textType"
            >
              <template #prefix>
                <el-icon><i-ep-Lock /></el-icon>
              </template>
              <template #suffix>
                <el-icon
                  v-if="textType == 'password'"
                  @click="textType = 'text'"
                  ><i-ep-View
                /></el-icon>
                <el-icon
                  v-else="textType == 'text'"
                  @click="textType = 'password'"
                  ><i-ep-Hide
                /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitLoginForm(loginFormRef)"
              >登录</el-button
            >
          </el-form-item>
        </div>
      </el-form>
    </div>
  </div>
</template>

<style scoped lang="less">
.main-wrap {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: url("@/assets/background.jpg");
  background-size: 100% 100%;

  .el-form > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}

.form-wrap {
  .el-form-item {
    padding-bottom: 10px;
  }
  .el-input {
    width: 350px;

    /deep/.el-input__wrapper {
      //   background-color: transparent;

      .el-input__inner {
        color: black;
      }
    }
  }

  .el-button {
    width: 350px;
    margin-bottom: 20px;
  }
}
</style>
