
<template>
  <n-layout position="absolute" style="top: 0px; bottom: 0px; left: 0px; right: 0px">
    <n-layout-header style="height: 64px; padding: 24px" bordered>
      追番小助手
    </n-layout-header>
    <n-layout position="absolute" style="top: 64px; bottom: 64px" has-sider>
      <Menu />
      <n-layout content-style="padding: 24px;" :native-scrollbar="false">
        <router-view />
      </n-layout>
    </n-layout>
    <n-layout-footer position="absolute" style="height: 64px; padding: 24px" bordered>
      城府路
    </n-layout-footer>
  </n-layout>
</template>

<script setup>
import { NLayout, NLayoutHeader, NLayoutFooter } from 'naive-ui'
import Menu from "./components/Menu.vue"
</script>

<style scoped></style>
