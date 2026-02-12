<template>
  <div class="app">
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>
        <button
          class="menu-item"
          :class="{ active: isActive('/layer1') }"
          @click="navigate('/layer1')"
        >Layer 1</button>

        <button
          class="menu-item"
          :class="{ active: isActive('/layer2') }"
          @click="navigate('/layer2')"
        >Layer 2</button>

        <button
          class="menu-item"
          :class="{ active: isActive('/layer3') }"
          @click="navigate('/layer3')"
        >Layer 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>
        <button class="menu-item" @click="navigate('/extruder1')">Extruder A</button>
        <button class="menu-item" @click="navigate('/extruder2')">Extruder B</button>
        <button class="menu-item" @click="navigate('/extruder3')">Extruder C</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">WINDER</div>
        <button class="menu-item" @click="navigate('/winder1')">Winder 1</button>
        <button class="menu-item" @click="navigate('/winder2')">Winder 2</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">UTILITIES</div>
        <button class="menu-item" @click="navigate('/reports')">Reports</button>
        <button class="menu-item" @click="navigate('/material-utilization')">
          Material Utilization
        </button>
      </div>
    </aside>

    <main class="main">
      <header class="topbar">
        <div class="top-left">
          <img src="/back-arrow.png" class="back-icon" @click="goBack" />
          <h1>THREE LAYER BLOWN FILM LINE</h1>
        </div>

        <div class="top-right">
          <span class="pill dark">
            {{ currentDate }}<br />{{ currentTime }}
          </span>
          <img src="/notification.png" class="notification-icon" />
          <img src="/power-button.png" class="power-icon" />
        </div>
      </header>

      <div class="content">
        <section class="panel left-panel">
          <h2>MATERIAL UTILIZATION</h2>
        </section>

        <section class="panel right-panel">
          <h2>OVERALL EQUIPMENT EFFICIENCY</h2>
          <div class="oee-grid">
            <div class="oee-box">OEE <span>72%</span></div>
            <div class="oee-box">Availability <span>87%</span></div>
            <div class="oee-box">Performance <span>81%</span></div>
            <div class="oee-box">Quality <span>94%</span></div>
          </div>
        </section>
      </div>

      <footer class="footer">MODEL : RFC-2550-40-1800</footer>
    </main>
  </div>
</template>

<script>
export default {
  name: "MaterialUtilization",
  data() {
    return { currentDate: "", currentTime: "" };
  },
  mounted() {
    this.updateClock();
    setInterval(this.updateClock, 1000);
  },
  methods: {
    // CENTRALIZED NAVIGATION
    navigate(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },

    // ALWAYS GO BACK TO DASHBOARD
    goBack() {
      this.$router.push("/dashboard");
    },

    isActive(path) {
      return this.$route.path === path;
    },

    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-US");
    }
  }
};
</script>


<style scoped>
.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.back-icon {
  width: 34px;
  cursor: pointer;
}

/* BACK BUTTON ICON */
.back-icon {
  width: 38px;
  height: 38px;
  cursor: pointer;

  /* smooth rounded edge */
  border-radius: 50%;
  padding: 6px;

  /* glass / smooth look */
  background: rgba(0, 255, 160, 0.12);
  backdrop-filter: blur(6px);

  /* animation */
  transition:
    transform 0.2s ease,
    box-shadow 0.25s ease,
    background-color 0.25s ease;
}

.back-icon:hover {
  transform: scale(1.08);
  background: rgba(0, 255, 160, 0.22);
  box-shadow:
    0 0 14px rgba(0, 255, 160, 0.45),
    inset 0 0 0 1px rgba(255,255,255,0.35);
}

.back-icon:active {
  transform: scale(0.96);
}

</style>


<style scoped>
.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.back-icon {
  width: 34px;
  cursor: pointer;
}

/* BACK BUTTON ICON */
.back-icon {
  width: 38px;
  height: 38px;
  cursor: pointer;

  /* smooth rounded edge */
  border-radius: 50%;
  padding: 6px;

  /* glass / smooth look */
  background: rgba(0, 255, 160, 0.12);
  backdrop-filter: blur(6px);

  /* animation */
  transition:
    transform 0.2s ease,
    box-shadow 0.25s ease,
    background-color 0.25s ease;
}

.back-icon:hover {
  transform: scale(1.08);
  background: rgba(0, 255, 160, 0.22);
  box-shadow:
    0 0 14px rgba(0, 255, 160, 0.45),
    inset 0 0 0 1px rgba(255,255,255,0.35);
}

.back-icon:active {
  transform: scale(0.96);
}

</style>
