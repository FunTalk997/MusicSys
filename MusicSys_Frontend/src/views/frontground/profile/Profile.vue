<script setup lang="ts">
import request from "@/api/request";
import {
  ElMessage,
  type FormInstance,
  type FormRules,
  type UploadProps,
} from "element-plus";
import Cookies from "js-cookie";

const formRef = ref<FormInstance>();
const form = ref({}) as any;
var iconUrl = "";

const getUserInfo = async () => {
  const userToken = Cookies.get("userToken");
  if (userToken) {
    await request({
      url: "userInfo/",
      params: { token: userToken },
    }).then((res) => {
      if (res.data.meta.status === 200) {
        form.value = res.data.data;
        iconUrl = res.data.data["iconUrl"];
      }
    });
  }
};
getUserInfo();

const rules = reactive<FormRules>({
  icon_url: [
    {
      required: true,
      message: "请选择头像",
      trigger: "blur",
    },
  ],
  nickname: [
    {
      required: true,
      message: "请输入手机号码",
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

// 图片上传
const iconFile = ref(new FormData());
const handleImgChange: UploadProps["onChange"] = (file, fileList: any[]) => {
  const isLt2M = file.raw!.size / 1024 / 1024 > 2;
  if (isLt2M) {
    ElMessage({
      type: "warning",
      message: "图片大小不能超过2M",
    });
  } else {
    form.value.iconUrl = URL.createObjectURL(file.raw!);
    iconFile.value.append("iconFile", file.raw!);
  }

  if (fileList.length > 1) {
    fileList.splice(0, 1);
  }
};

// 保存信息
const handleConfirm = async (formEl: FormInstance | undefined) => {
  if (form.value.iconUrl && form.value.iconUrl !== iconUrl) {
    await request({
      url: "upload/",
      method: "post",
      headers: { "Content-Type": "multipart/form-data" },
      data: iconFile.value,
    }).then((response: any) => {
      form.value.iconUrl = response.iconUrl;
    });
  } else if (form.value.iconUrl && form.value.iconUrl === iconUrl) {
  } else {
    ElMessage({
      type: "warning",
      message: "请上传图片！",
    });
    return;
  }

  if (!formEl) return;
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      request({
        url: "user/",
        method: "put",
        data: form.value,
      }).then(() => {
        ElMessage({
          message: "修改成功",
          type: "success",
        });
      });
    } else {
      console.log("error submit!", fields);
    }
  });
};
</script>

<template>
  <el-card>
    <template #header>
      <span>个人信息</span>
    </template>
    <el-form
      ref="formRef"
      :model="form"
      label-width="120px"
      :rules="rules"
      status-icon
    >
      <el-form-item label="头像：" prop="icon">
        <el-upload
          class="icon-uploader"
          action="#"
          accept=".jpg;.jpeg"
          :show-file-list="false"
          :auto-upload="false"
          :on-change="handleImgChange"
        >
          <el-image
            v-if="form.iconUrl"
            :src="form.iconUrl"
            style="width: 100px; height: 100px; border-radius: 50%"
          />
          <el-icon v-else class="icon-uploader-icon">
            <i-ep-Plus />
          </el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item label="用户名：" prop="username">
        <el-input disabled v-model="form.username"></el-input>
      </el-form-item>
      <el-form-item label="昵称：" prop="nickname">
        <el-input v-model="form.nickname"></el-input>
      </el-form-item>
      <el-form-item label="邮箱：" prop="email">
        <el-input v-model="form.email"></el-input>
      </el-form-item>
      <div class="handle">
        <el-button type="success" @click="handleConfirm(formRef)"
          >保存信息</el-button
        >
        <el-button @click="getUserInfo">取消修改</el-button>
      </div>
    </el-form>
  </el-card>
</template>

<style scoped lang="less">
.el-card {
  margin-top: 30px;
}

.el-input {
  width: 300px;
}

.handle {
  margin-left: 100px;
}

.icon-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.icon-uploader:hover {
  border-color: var(--el-color-primary);
}

.el-icon.icon-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
}
</style>
