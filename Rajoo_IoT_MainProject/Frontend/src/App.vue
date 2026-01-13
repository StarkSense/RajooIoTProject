<template>
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
</script>
