<script setup lang="ts">
import request from "@/api/request";
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
  songName: "",
  singer: "",
  album: "",
  songTime: "",
  lyric: "",
  lyricist: "",
  picUrl: "",
  songUrl: "",
});

const rules = reactive<FormRules>({
  songName: [
    {
      required: true,
      message: "请输入歌曲名称",
      trigger: "blur",
    },
  ],
  picUrl: [
    {
      required: true,
      message: "请输专辑封面",
      trigger: "blur",
    },
  ],
  songUrl: [
    {
      required: true,
      message: "请输入音频文件",
      trigger: "blur",
    },
  ],
  singer: [
    {
      required: true,
      message: "请输入歌手",
      trigger: "blur",
    },
  ],
  album: [
    {
      required: true,
      message: "请输入歌曲专辑",
      trigger: "blur",
    },
  ],
  songTime: [
    {
      required: true,
      message: "请输入歌曲时长",
      trigger: "blur",
    },
  ],
});

// 图片上传
const picFile = ref(new FormData());
const handlePicChange: UploadProps["onChange"] = (file, fileList: any[]) => {
  const isLt2M = file.raw!.size / 1024 / 1024 > 2;
  if (isLt2M) {
    ElMessage({
      type: "warning",
      message: "图片大小不能超过2M",
    });
  } else {
    form.value.picUrl = URL.createObjectURL(file.raw!);

    if (picFile.value.has("picFile")) {
      picFile.value.set("picFile", file.raw!);
    } else {
      picFile.value.append("picFile", file.raw!);
    }
  }

  if (fileList.length > 0) {
    fileList.splice(0);
  }
};

// 音频上传
const audioFile = ref(new FormData());
const handleAudioChange: UploadProps["onChange"] = (file, fileList: any[]) => {
  const isLt2M = file.raw!.size / 1024 / 1024 > 20;
  if (isLt2M) {
    ElMessage({
      type: "warning",
      message: "音频大小不能超过20M",
    });
  } else {
    form.value.songUrl = URL.createObjectURL(file.raw!);

    if (audioFile.value.has("audioFile")) {
      audioFile.value.set("audioFile", file.raw!);
    } else {
      audioFile.value.append("audioFile", file.raw!);
    }
  }

  if (fileList.length > 1) {
    fileList.splice(0, 1);
  }
};

// 提交表单
const handleConfirm = async (formEl: FormInstance | undefined) => {
  if (form.value.picUrl) {
    await request({
      url: "upload/",
      method: "post",
      headers: { "Content-Type": "multipart/form-data" },
      data: picFile.value,
    }).then((res: any) => {
      if (res.data.meta["status"] === 201) {
        form.value.picUrl = res.data.data["picUrl"];
      } else {
        ElMessage({
          type: "error",
          message: res.data.meta["msg"],
        });
        return;
      }
    });
  } else {
    ElMessage({
      type: "warning",
      message: "请上传图片！",
    });
    return;
  }

  if (form.value.songUrl) {
    await request({
      url: "upload/",
      method: "post",
      headers: { "Content-Type": "multipart/form-data" },
      data: audioFile.value,
    }).then((res: any) => {
      if (res.data.meta["status"] === 201) {
        form.value.songUrl = res.data.data["songUrl"];
      } else {
        ElMessage({
          type: "error",
          message: res.data.meta["msg"],
        });
        return;
      }
    });
  } else {
    ElMessage({
      type: "warning",
      message: "请上传音频",
    });
    return;
  }

  if (!formEl) return;
  await formEl.validate(async (valid, fields) => {
    if (valid) {
      props.dialogTitle === "新增歌曲"
        ? await request({
            url: "music/",
            method: "post",
            data: form.value,
          })
        : await request({
            url: "music/",
            method: "put",
            data: form.value,
          });
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
        <el-form-item label="歌曲名称" prop="songName">
          <el-input v-model="form.songName"></el-input>
        </el-form-item>
        <el-form-item label="专辑封面" prop="picUrl">
          <el-upload
            class="pic-upload"
            action="#"
            accept=".jpg, .jpeg"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="handlePicChange"
          >
            <img
              v-if="form.picUrl"
              :src="form.picUrl"
              class="img"
              style="width: 150px; height: 180px"
            />
            <el-icon v-else class="pic"><i-ep-Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="音频文件" prop="songUrl">
          <el-upload
            class="audio-upload"
            action="#"
            accept=".mp3"
            :auto-upload="false"
            :on-change="handleAudioChange"
          >
            <el-button type="primary"
              ><el-icon><i-ep-UploadFilled /></el-icon>选择音频</el-button
            >
            <!-- <a :href="form.songUrl" hidden></a> -->
          </el-upload>
        </el-form-item>
        <el-form-item label="歌手" prop="singer">
          <el-input v-model="form.singer"></el-input>
        </el-form-item>
        <el-form-item label="歌曲专辑" prop="album">
          <el-input v-model="form.album"></el-input>
        </el-form-item>
        <el-form-item label="作词" prop="lyricist">
          <el-input v-model="form.lyricist"></el-input>
        </el-form-item>
        <el-form-item label="歌曲时长" prop="songTime">
          <el-input v-model="form.songTime"></el-input>
        </el-form-item>
        <el-form-item label="歌词" prop="lyric">
          <el-input type="textarea" v-model="form.lyric"></el-input>
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
.pic-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
  width: 150px;
  height: 150px;
}

.pic-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.pic {
  font-size: 28px;
  color: #8c939d;
  width: 150px;
  height: 150px;
  text-align: center;
}

.audio-upload {
  display: flex;
}
</style>
