<script setup lang="ts">
import request from "@/api/request";
import { trigger } from "@vue/reactivity";
import {
  ElMessage,
  type FormInstance,
  type FormRules,
  type UploadProps,
} from "element-plus";

const props = defineProps<{
  dialogVisible: boolean;
  dialogTitle: string;
  dialogTableValue: object;
}>();

const emits = defineEmits(["update:dialogVisible", "initDataList"]);
const handleClose = () => {
  emits("update:dialogVisible", false);
};

const formRef = ref<FormInstance>();

const form = ref({
  id: "",
  username: "",
  password: "",
  nickname: "",
  email: "",
  iconUrl: "",
});

const rules = reactive<FormRules>({
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
      message: "请输密码",
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
  iconUrl: [
    {
      required: true,
      message: "请上传图像",
      trigger: "blur",
    },
  ],
});

// 图片上传
const imgFile = ref(new FormData());
const handleImgChange: UploadProps["onChange"] = (file, fileList: any[]) => {
  const isLt2M = file.raw!.size / 1024 / 1024 > 2;
  if (isLt2M) {
    ElMessage({
      type: "warning",
      message: "图片大小不能超过2M",
    });
  } else {
    form.value.iconUrl = URL.createObjectURL(file.raw!);
    imgFile.value.append("imgFile", file.raw!);
  }

  if (fileList.length > 1) {
    fileList.splice(0, 1);
  }
};

const handleConfirm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      await request({ url: "user/", method: "post", data: form.value });
      ElMessage({
        message: "添加成功",
        type: "success",
      });
      emits("initDataList");
      handleClose();
    } else {
      console.log("error submit!", fields);
    }
  });
};

watch(
  () => props.dialogTableValue,
  () => {
    form.value = props.dialogTableValue as any;
  },
  { deep: true, immediate: true }
);
</script>

<template>
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="40%"
    :before-close="handleClose"
  >
    <el-scrollbar>
      <el-form
        ref="formRef"
        :model="form"
        label-width="100px"
        :rules="rules"
        status-icon
      >
        <el-form-item label="头像" prop="iconUrl">
          <el-upload
            class="img-uploader"
            action="#"
            accept=".jpg, .jpeg"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="handleImgChange"
          >
            <img
              v-if="form.iconUrl"
              :src="form.iconUrl"
              class="img"
              style="width: 150px; height: 180px"
            />
            <el-icon v-else class="img-uploader-icon"><i-ep-Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="form.nickname"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email"></el-input>
        </el-form-item>
      </el-form>
    </el-scrollbar>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleConfirm(formRef)"
          >确认</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>

<style scoped lang="less">
.img-uploader {
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

.img-uploader:hover {
  border-color: var(--el-color-primary);
}

.el-icon.img-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  text-align: center;
}
</style>
