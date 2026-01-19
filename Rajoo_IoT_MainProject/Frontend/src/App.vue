<!-- <template>
  <router-view v-slot="{ Component }">
    <transition :name="transitionName" mode="out-in">
      <component :is="Component" :key="$route.fullPath" />
    </transition>
  </router-view>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const transitionName = ref("fade");
    const router = useRouter();

    router.beforeEach((to, from, next) => {
      if (from.path.startsWith("/layer") && to.path === "/dashboard") {
        transitionName.value = "slide-back";
      } else {
        transitionName.value = "fade";
      }
      next();
    });

    return { transitionName };
  }
};
</script> -->


<template>
  <router-view v-slot="{ Component }">
    <transition :name="transitionName" mode="out-in">
      <component :is="Component" :key="$route.fullPath" />
    </transition>
  </router-view>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";

// 🔥 FIXED PATH (IMPORTANT)
import socket from "./services/socket";

export default {
  setup() {
    const transitionName = ref("fade");
    const router = useRouter();

    // ------------------------------
    // Route transition logic 
    // ------------------------------
    router.beforeEach((to, from, next) => {
      if (from.path.startsWith("/layer") && to.path === "/dashboard") {
        transitionName.value = "slide-back";
      } else {
        transitionName.value = "fade";
      }
      next();
    });

    // ------------------------------
    // Telemetry listener
    // ------------------------------
    const onTelemetry = (data) => {
      console.log("📡 LIVE TELEMETRY RECEIVED:", data);
    };

    onMounted(() => {
      console.log("📦 App mounted → attaching telemetry listener");
      socket.on("telemetry_update", onTelemetry);
    });

    onBeforeUnmount(() => {
      socket.off("telemetry_update", onTelemetry);
    });

    return { transitionName };
  }
};
</script>

