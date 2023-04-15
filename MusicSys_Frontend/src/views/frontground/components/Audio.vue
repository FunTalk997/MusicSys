<script setup lang="ts">
import APlayer from "aplayer";
import "aplayer/dist/APlayer.min.css";
import eventBus from "./event-bus";

const aplayerRef = ref(null);
const aplayer = ref(null) as any;

eventBus.on("logout", () => {
  aplayer.value.destroy();
});

eventBus.on("playList", (args: any) => {
  aplayer.value.list.clear();
  aplayer.value.list.add(
    args["dataList"].value.map(function (item: any) {
      return {
        name: item.songName,
        artist: item.singer,
        url: item.songUrl,
        cover: item.picUrl,
        lrc: item.lyric,
      };
    })
  );
  const index = args["dataList"].value.findIndex(
    (item: any) => item.id === args["row"].id
  );
  aplayer.value.list.switch(index);
  aplayer.value.play();
});

eventBus.on("play", (song: any) => {
  aplayer.value.list.clear();
  aplayer.value.list.add({
    name: song.value.songName,
    artist: song.value.singer,
    url: song.value.songUrl,
    cover: song.value.picUrl,
    lrc: song.value.lyric,
  });
  aplayer.value.play();
});

eventBus.on("addPlayList", (song: any) => {
  const playList = aplayer.value.list.audios;
  if (playList.some((item: any) => item.name === song.songName)) {
    return;
  } else {
    aplayer.value.list.add({
      name: song.songName,
      artist: song.singer,
      url: song.songUrl,
      cover: song.picUrl,
      lrc: song.lyric,
    });
  }
});

onMounted(() => {
  aplayer.value = new APlayer({
    container: aplayerRef.value,
    fixed: true,
    autoplay: true,
    theme: "#FADFA3",
    loop: "all",
    order: "random",
    preload: "auto",
    volume: 0.7,
    mutex: true,
    listMaxHeight: 90,
    lrcType: 1,
    audio: [
      {
        name: "玛卡巴卡",
        artist: "mahalin",
        url: "http://43.139.166.206/upload/music/musicUrl/1680620660536.mp3",
        cover: "http://43.139.166.206/upload/music/picUrl/1680620363929.jpg",
        lrc: "[00:00.00-1] 作曲 : 马哈林\n",
      },
      {
        name: "从前有个魔仙堡",
        artist: "挽萤",
        url: "http://43.139.166.206/upload/music/picUrl/1680779628172.jpg",
        cover: "http://43.139.166.206/upload/music/musicUrl/1680779628328.mp3",
        lrc: "[00:03.02]作曲：黎允文\n[00:05.02]作词：徐少荣\n[00:07.02]原唱：大小Ann\n[00:09.02]翻唱/后期：挽萤\n[00:17.02]传说有个魔仙堡\n[00:20.29]有个女王不得了\n[00:23.47]每个魔仙得她指导\n[00:26.87]都盼望世界更美好\n[00:30.10]变大变小真奇妙\n[00:32.98]一个咒语一个符号\n[00:36.39]一不小心就会一团糟\n[00:41.17]\n[00:42.80]我有个好提议\n[00:44.62]就约定在一起\n[00:46.19]去寻找魔法的秘密\n[00:49.29]一看到巧克力\n[00:51.11]特别是草莓的\n[00:52.71]我知道我无能为力\n[00:56.87]\n[00:57.58]巴啦啦小魔仙\n[00:59.28]咒语一呼喊\n[01:00.99]就展开正义的一战\n[01:03.79]巴啦啦小魔仙\n[01:05.64]咒语一呼喊\n[01:07.33]会实现最美的梦想\n[01:10.43]有了友爱力量\n[01:12.48]我的法力变强\n[01:14.10]战胜灰暗忧伤\n[01:15.58]我们才能够成长\n[01:18.91]\n[01:29.52]就算魔法多神奇\n[01:33.15]夺到魔法的彩石\n[01:36.27]比不上我得到友谊\n[01:39.67]有了爱世界才美丽\n[01:42.45]一次探险一起游历\n[01:45.83]一种鼓励一点勇气\n[01:49.19]为这世界送上了奇迹\n[01:54.39]\n[01:55.35]我有个好建议\n[01:57.45]就约定在一起\n[01:59.04]去寻找魔法的秘密\n[02:01.94]一看到巧克力\n[02:03.88]特别是草莓的\n[02:05.43]我知道我无能为力\n[02:09.51]\n[02:10.53]巴啦啦小魔仙\n[02:12.07]咒语一呼喊\n[02:13.58]就展开正义的一战\n[02:16.60]巴啦啦小魔仙\n[02:18.40]咒语一呼喊\n[02:19.96]会实现最美的梦想\n[02:23.18]巴啦啦小魔仙\n[02:24.97]咒语一呼喊\n[02:26.37]会将来不断快成长\n[02:29.46]巴啦啦小魔仙\n[02:31.49]咒语一呼喊\n[02:32.90]这世界马上不一样\n[02:36.15]有了友爱力量\n[02:38.01]我的法力变强\n[02:39.69]战胜灰暗忧伤\n[02:41.26]我们才能够成长\n[02:44.23]小魔仙 来到人间\n[02:45.82]一整天 帮助别人不空闲\n[02:49.36]小魔仙 不怕危险\n[02:52.43]守一天 明天就会好一点\n[02:55.96]小魔仙 友爱永远[02:58.81]小魔仙 正义的心不改变\n[03:04.67]\n",
      },
    ],
  });
});
</script>

<template>
  <div id="aplayer" ref="aplayerRef"></div>
</template>

<style scoped lang="less"></style>
