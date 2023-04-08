<script setup lang="ts">
import request from "@/api/request";
import { ElMessage, type FormInstance, type FormRules } from "element-plus";

const props = defineProps<{
  dialogVisible: boolean;
}>();

const emits = defineEmits(["update:dialogVisible"]);
const handleClose = () => {
  emits("update:dialogVisible", false);
};

const formRef = ref<FormInstance>();

const form = ref({
  username: "admin",
  oldPassword: "",
  newPassword: "",
  checkPassword: "",
});

const checkOldPw = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("请输入旧密码"));
  }
  request({
    url: "editPwd/",
    params: form.value,
  }).then((response) => {
    if (response.data.meta.status === 200) {
      callback();
    } else {
      callback(new Error(response.data.meta.msg));
    }
  });
};

const checkNewPw = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error("请再次输入密码"));
  }
  if (form.value.newPassword !== value) {
    callback(new Error("密码不一致"));
  } else {
    callback();
  }
};

const rules = reactive<FormRules>({
  oldPassword: [
    {
      required: true,
      validator: checkOldPw,
      trigger: "blur",
    },
  ],
  newPassword: [
    {
      required: true,
      message: "请输入新密码",
      trigger: "blur",
    },
  ],
  checkPassword: [
    {
      required: true,
      validator: checkNewPw,
      trigger: "blur",
    },
  ],
});

const handleConfirm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      await request({
        url: "editPwd/",
        method: "put",
        data: form.value,
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      }).then(() => {
        ElMessage({
          message: "修改成功",
          type: "success",
        });
        handleClose();
      });
    } else {
      console.log("error submit!", fields);
    }
  });
};
</script>

<template>
  <el-dialog
    :model-value="dialogVisible"
    title="修改密码"
    width="40%"
    :before-close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      label-width="20%"
      :rules="rules"
      status-icon
    >
      <div class="content">
        <el-form-item label="旧密码：" prop="oldPassword">
          <el-input
            class="con"
            type="password"
            v-model="form.oldPassword"
          ></el-input>
        </el-form-item>
        <el-form-item label="新密码：" prop="newPassword">
          <el-input
            class="con"
            type="password"
            v-model="form.newPassword"
          ></el-input>
        </el-form-item>
        <el-form-item label="旧密码：" prop="checkPassword">
          <el-input
            class="con"
            type="password"
            v-model="form.checkPassword"
          ></el-input>
        </el-form-item>
      </div>
    </el-form>
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
.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>
