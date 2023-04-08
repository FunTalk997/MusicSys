<script setup lang="ts">
import request from "@/api/request";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";
import { useRouter } from "vue-router";
import Cookies from "js-cookie";

const router = useRouter();

const isLogin = ref(true);
const loginFormRef = ref<FormInstance>();
const registerFormRef = ref<FormInstance>();
const loginForm = ref({
  username: "user01",
  password: "123456",
});
const registerForm = ref({
  username: "",
  password: "",
  nickname: "",
  email: "",
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

const registerRules = reactive<FormRules>({
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
  nickname: [
    {
      required: true,
      message: "请输入昵称",
      trigger: "blur",
    },
  ],
  email: [
    {
      required: true,
      message: "请输入邮箱",
      trigger: "blur, change",
    },
    {
      type: "email",
      message: "请输入正确的邮箱地址",
      trigger: ["blur", "change"],
    },
  ],
});

const submitLoginForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      await request({
        url: "userLogin/",
        method: "post",
        data: loginForm.value,
      }).then((response) => {
        if (response.data.meta.status === 201) {
          const userToken = response.data.data["token"];
          Cookies.set("userToken", userToken);
          router.replace("/");
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

const submitRegisterForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      await request({
        url: "user/",
        method: "post",
        data: registerForm.value,
      }).then((response) => {
        if (response.data.meta.status === 201) {
          isLogin.value = !isLogin.value;
          ElMessage({
            type: "success",
            message: "注册成功",
          });
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

const toggle = () => {
  isLogin.value = !isLogin.value;
};
</script>

<template>
  <div class="main-wrap">
    <div class="login-wrap" v-if="isLogin">
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        status-icon
      >
        <div class="logo-wrap">
          <h1>音乐管理系统</h1>
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
          <span
            >没有账号？<a
              style="color: #ff9933; cursor: pointer"
              @click="toggle"
              >立即注册</a
            ></span
          >
        </div>
      </el-form>
    </div>

    <div class="register-wrap" v-else>
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        status-icon
      >
        <div class="logo-wrap">
          <h1>音乐管理系统</h1>
        </div>
        <div class="form-wrap">
          <el-form-item prop="username">
            <el-input v-model="registerForm.username" placeholder="用户名">
              <template #prefix>
                <el-icon><i-ep-User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="nickname">
            <el-input v-model="registerForm.nickname" placeholder="昵称">
              <template #prefix>
                <el-icon><i-ep-Avatar /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
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

          <el-form-item prop="email">
            <el-input v-model="registerForm.email" placeholder="邮箱">
              <template #prefix>
                <el-icon><i-ep-Postcard /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              @click="submitRegisterForm(registerFormRef)"
              >注册</el-button
            >
          </el-form-item>
          <span
            >已有账号？<a
              style="color: #ff9933; cursor: pointer"
              @click="toggle"
              >立即登录</a
            ></span
          >
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
