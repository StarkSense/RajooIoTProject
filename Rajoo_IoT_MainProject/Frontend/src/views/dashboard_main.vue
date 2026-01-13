<template>
  <div class="app">
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>

        <button
          class="menu-item"
          :class="{ active: isActive('/layer1') }"
          @click="goToLayer('/layer1')"
        >
          Layer 1
        </button>

        <button
          class="menu-item"
          :class="{ active: isActive('/layer2') }"
          @click="goToLayer('/layer2')"
        >
          Layer 2
        </button>

        <button
          class="menu-item"
          :class="{ active: isActive('/layer3') }"
          @click="goToLayer('/layer3')"
        >
          Layer 3
        </button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>

        <button
          class="menu-item"
          :class="{ active: isActive('/extruder1') }"
          @click="goTo('/extruder1')"
        >
          Extruder 1
        </button>

        <button
          class="menu-item"
          :class="{ active: isActive('/extruder2') }"
          @click="goTo('/extruder2')"
        >
          Extruder 2
        </button>

        <button
          class="menu-item"
          :class="{ active: isActive('/extruder3') }"
          @click="goTo('/extruder3')"
        >
          Extruder 3
        </button>
      </div>


      <div class="menu-section">
        <div class="menu-title">WINDER</div>

        <button
          class="menu-item"
          :class="{ active: isActive('/winder1') }"
          @click="goTo('/winder1')"
        >
          Winder 1
        </button>

        <button
          class="menu-item"
          :class="{ active: isActive('/winder2') }"
          @click="goTo('/winder2')"
        >
          Winder 2
        </button>
      </div>

      <div class="menu-section">
        <div class="menu-title">UTILITIES</div>

        <button
          class="menu-item"
          :class="{ active: isActive('/reports') }"
          @click="goTo('/reports')"
        >
          Reports
        </button>

        <button
          class="menu-item"
          :class="{ active: isActive('/material-utilization') }"
          @click="goTo('/material-utilization')"
        >
          Material Utilization
        </button>
      </div>

    </aside>

    <!-- MAIN -->
    <main class="main">
      <!-- TOP BAR -->
      <header class="topbar">
        <h1>THREE LAYER BLOWN FILM LINE</h1>
        <div class="top-right">
          <span class="pill dark">
            {{ currentDate }}<br />
            {{ currentTime }}
          </span>
          <img src="/notification.png" class="notification-icon" />
          <img
            src="/power-button.png"
            class="power-icon"
            @click="handleLogout"
          />
        </div>
      </header>

      <!-- CONTENT -->
      <div class="content">
        <!-- MACHINE OVERVIEW -->
        <section class="panel left-panel">
          <h2>MACHINE OVERVIEW PANEL</h2>

          <!-- STATS -->
          <div class="stats">
            <div class="stat">
              Total Set Output
              <span>{{ total_set_output.toFixed(2) }} kg/hr</span>
            </div>
            <div class="stat">
              Total Actual Output
              <span>{{ total_actual_output.toFixed(2) }} kg/hr</span>
            </div>
            <div class="stat">
              Density
              <span>{{ density.toFixed(2) }} g/cm³</span>
            </div>
            <div class="stat">
              GSM
              <span>{{ gsm.toFixed(2) }}</span>
            </div>
            <div class="stat">
              Lay Flat
              <span>{{ lay_flat.toFixed(2) }} mm</span>
            </div>
          </div>

          <!-- LIP + MAP -->
          <div class="dual-graph-row">
            <div class="row graph-row">
              <div class="row-title">LIP PROFILE</div>
              <Line :data="lipChartData" :options="lipChartOptions" />
            </div>
            <div class="row graph-row">
              <div class="row-title">MAP PROFILE</div>
              <Line :data="mapChartData" :options="mapChartOptions" />
            </div>
          </div>

          <!-- IBC + SPEED -->
          <div class="dual-graph-row">
            <div class="row graph-row">
              <div class="row-title">IBC TEMP IN / OUT</div>
              <Bar :data="ibcChartData" :options="ibcChartOptions" />
            </div>
            <div class="row graph-row">
              <div class="row-title">SET vs ACT SPEED</div>
              <Line :data="speedChartData" :options="speedChartOptions" />
            </div>
          </div>

          <!-- DIE TEMP ZONES -->
          <div class="row die-zone-card">
            <div class="row-title">DIE TEMPERATURE ZONE WISE</div>

            <div class="die-zone-grid">
              <div
                v-for="zone in die_temp_zones"
                :key="zone.zone"
                class="die-zone"
                :class="zoneStatus(zone)"
              >
                <div class="zone-name">{{ zone.zone }}</div>
                <div class="zone-values">
                  <div>SET <span>{{ zone.set.toFixed(1) }}°C</span></div>
                  <div>ACT <span>{{ zone.actual.toFixed(1) }}°C</span></div>
                  <div class="delta">
                    Δ {{ (zone.actual - zone.set).toFixed(1) }}°C
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- THICKNESS -->
          <div class="row thickness-card-full">
            <div class="row-title">THICKNESS</div>
            <div class="thickness-content-full">
              <div class="thickness-graph-full">
                <Line
                  :data="thicknessChartData"
                  :options="thicknessChartOptions"
                />
              </div>
              <div class="thickness-info-full">
                <div><b>Set Thickness</b> : {{ thickness_stats.set }}</div>
                <div><b>Average</b> : {{ thickness_stats.avg }}</div>
                <div><b>Nominal</b> : {{ thickness_stats.nominal }}</div>
                <div><b>Maximum</b> : {{ thickness_stats.max }}</div>
                <div><b>Minimum</b> : {{ thickness_stats.min }}</div>
                <div><b>GBR Position</b> : {{ thickness_stats.gbr }}</div>
              </div>
            </div>
          </div>
        </section>

        <!-- OEE -->
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
import { io } from "socket.io-client";
import { Line, Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

export default {
  name: "DashboardMain",
  components: { Line, Bar },

  data() {
    return {
      currentDate: "",
      currentTime: "",
      socket: null,

      total_set_output: 0,
      total_actual_output: 0,
      density: 0,
      gsm: 0,
      lay_flat: 0,

      lip_profile: [],
      map_profile: [],
      ibc_temp_in: [],
      ibc_temp_out: [],
      speed_set: [],
      speed_actual: [],
      die_temp_zones: [],
      thickness_trend: [],
      thickness_stats: {
        set: 0,
        avg: 0,
        nominal: 0,
        max: 0,
        min: 0,
        gbr: 0
      }
    };
  },

  mounted() {
    this.updateClock();
    setInterval(this.updateClock, 1000);

    this.socket = io("http://localhost:5000", {
      transports: ["websocket"]
    });

    this.socket.on("telemetry_update", (data) => {
      this.total_set_output =
        data.total_set_output ?? this.total_set_output;
      this.total_actual_output =
        data.total_actual_output ?? this.total_actual_output;
      this.density = data.density ?? this.density;
      this.gsm = data.gsm ?? this.gsm;
      this.lay_flat = data.lay_flat ?? this.lay_flat;

      this.lip_profile = data.lip_profile ?? [];
      this.map_profile = data.map_profile ?? [];
      this.ibc_temp_in = data.ibc_temp?.in ?? [];
      this.ibc_temp_out = data.ibc_temp?.out ?? [];
      this.speed_set = data.speed_trend?.set ?? [];
      this.speed_actual = data.speed_trend?.actual ?? [];
      this.die_temp_zones = data.die_temp_zones ?? [];

      if (data.thickness) {
        this.thickness_trend = data.thickness.trend ?? [];
        this.thickness_stats = {
          ...this.thickness_stats,
          ...data.thickness.stats
        };
      }
    });
  },

  methods: {
    /* ========== SIDEBAR NAVIGATION (ADDED) ========== */
    goToLayer(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },
    
    goTo(path) {
      if (this.$route.path !== path) {
        this.$router.push(path);
      }
    },

    isActive(path) {
      return this.$route.path === path;
    },

    /* ========== CLOCK ========== */
    updateClock() {
      const now = new Date();
      this.currentDate = now.toLocaleDateString("en-GB");
      this.currentTime = now.toLocaleTimeString("en-US");
    },

    zoneStatus(zone) {
      const diff = Math.abs(zone.actual - zone.set);
      if (diff <= 2) return "ok";
      if (diff <= 5) return "warn";
      return "alert";
    },

    /* ========== LOGOUT ========== */
    handleLogout() {
      try {
        if (this.socket) {
          this.socket.disconnect();
          this.socket = null;
        }

        localStorage.removeItem("token");
        this.$router.replace("/");
      } catch (err) {
        console.error("Logout failed:", err);
        window.location.href = "/";
      }
    },

    /* ========== COMMON CHART OPTIONS ========== */
    commonOptions(x, y, legend = false) {
      return {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        layout: { padding: { bottom: 20 } },
        plugins: {
          legend: legend
            ? { labels: { color: "#e6f7fb", font: { size: 11 } } }
            : { display: false }
        },
        scales: {
          x: {
            title: {
              display: !!x,
              text: x,
              color: "#e6f7fb",
              font: { size: 12, weight: "600" }
            },
            ticks: { color: "#cfefff", font: { size: 11 } }
          },
          y: {
            title: {
              display: !!y,
              text: y,
              color: "#e6f7fb",
              font: { size: 12, weight: "600" }
            },
            ticks: { color: "#cfefff", font: { size: 11 } }
          }
        }
      };
    }
  },

  computed: {
    lipChartData() {
      return {
        labels: this.lip_profile.map(p => p.x),
        datasets: [
          {
            data: this.lip_profile.map(p => p.y),
            borderColor: "#7fdcff",
            tension: 0.35,
            pointRadius: 2
          }
        ]
      };
    },

    mapChartData() {
      return {
        labels: this.map_profile.map(p => p.x),
        datasets: [
          {
            data: this.map_profile.map(p => p.y),
            borderColor: "#81c784",
            tension: 0.35,
            pointRadius: 2
          }
        ]
      };
    },

    ibcChartData() {
      return {
        labels: this.ibc_temp_in.map(p => p.x),
        datasets: [
          {
            label: "IBC IN",
            data: this.ibc_temp_in.map(p => p.y),
            backgroundColor: "rgba(77,208,225,0.75)"
          },
          {
            label: "IBC OUT",
            data: this.ibc_temp_out.map(p => p.y),
            backgroundColor: "rgba(255,183,77,0.75)"
          }
        ]
      };
    },

    speedChartData() {
      return {
        labels: this.speed_set.map(p => p.x),
        datasets: [
          { label: "SET", data: this.speed_set.map(p => p.y), borderColor: "#4dd0e1" },
          { label: "ACT", data: this.speed_actual.map(p => p.y), borderColor: "#ff7043" }
        ]
      };
    },

    thicknessChartData() {
      const labels = this.thickness_trend.map(p => p.x);
      return {
        labels,
        datasets: [
          {
            label: "Actual Thickness",
            data: this.thickness_trend.map(p => p.y),
            borderColor: "#ff7043",
            tension: 0.3,
            pointRadius: 2
          },
          {
            label: "Set Thickness",
            data: labels.map(() => this.thickness_stats.set),
            borderColor: "#4dd0e1",
            borderDash: [6, 4],
            pointRadius: 0
          }
        ]
      };
    },

    lipChartOptions() {
      return this.commonOptions("Die Width (mm)", "Thickness (µm)");
    },
    mapChartOptions() {
      return this.commonOptions("Die Width (mm)", "Thickness (µm)");
    },
    ibcChartOptions() {
      return this.commonOptions("Time", "Temperature (°C)", true);
    },
    speedChartOptions() {
      return this.commonOptions("Time", "Speed (m/min)", true);
    },
    thicknessChartOptions() {
      return this.commonOptions("Time", "Thickness (µm)");
    }
  }
};
</script>



<style>
  /* ================= BASE ================= */
* {
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  margin: 0;
  background: radial-gradient(circle at top, #0c2c3d, #061621);
  font-family: "Inter", sans-serif;
  color: #e6f7fb;
  overflow: hidden;
}

/* ================= APP LAYOUT ================= */
.app {
  display: flex;
  width: 100vw;
  height: 100vh;
}

/* ================= SIDEBAR ================= */
.sidebar {
  width: 190px;
  min-width: 190px;
  max-width: 190px;
  height: 100vh;
  padding: 14px;
  background: linear-gradient(180deg, #051c2a, #04121b);
  flex-shrink: 0;
}

/* ================= AVATAR ================= */
.avatar {
  width: 50px;
  height: 50px;
  margin-bottom: 18px;
  border-radius: 50%;
  background: radial-gradient(circle, #7fdcff, #3f51b5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar img {
  width: 32px;
}

/* ================= MENU ================= */
.menu-title {
  font-size: 10px;
  letter-spacing: 1.4px;
  color: #4dd0e1;
  margin: 10px 0 6px;
}

.menu-item {
  width: 100%;
  background: rgba(255,255,255,0.06);
  border: none;
  color: #e6f7fb;
  padding: 8px 10px;
  border-radius: 10px;
  margin-bottom: 6px;
  text-align: left;
  font-size: 13px;
}

.menu-item.active {
  background: rgba(127,220,255,0.25);
}

/* ================= MAIN ================= */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* ================= TOP BAR ================= */
.topbar {
  height: 60px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, #0e2f43, #081c28);
}

.topbar h1 {
  font-size: 21px;
  font-weight: 700;
  letter-spacing: 0.6px;
  margin: 0;
}

/* ================= CONTENT ================= */
.content {
  flex: 1;
  display: grid;
  grid-template-columns: 3fr 0.7fr;
  gap: 16px;
  padding: 16px 20px;
  overflow: hidden;
}

/* ================= PANELS ================= */
.panel {
  background: rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* ================= STATS ================= */
.stats {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.stat {
  background: rgba(255,255,255,0.14);
  border-radius: 14px;
  padding: 18px 14px;
  min-height: 82px;
  text-align: center;
  font-size: 18px;
}

.stat span {
  display: block;
  margin-top: 6px;
  font-size: 18px;
  font-weight: 700;
}

.stats .stat:nth-child(1) span { color: #7fdcff; }
.stats .stat:nth-child(2) span { color: #6ee7b7; }

/* ================= ROW ================= */
.row {
  background: rgba(255,255,255,0.1);
  border-radius: 14px;
  padding: 12px;
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.row-title {
  font-size: 11px;
  margin-bottom: 8px;
  letter-spacing: 0.6px;
}

/* ================= GRAPH (COMPACT) ================= */
.graph-row {
  min-height: 120px;
}

.dual-graph-row {
  min-height: 160px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* ================= DIE TEMP ================= */
.die-zone-card {
  flex: 0 0 auto;
}

.die-zone-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
}

.die-zone {
  background: rgba(255,255,255,0.12);
  border-radius: 12px;
  padding: 10px 6px;
  text-align: center;
  font-size: 12px;
  font-weight: 700;
}

.zone-name {
  font-size: 15px;
}

.zone-values div {
  font-size: 14px;
}

.delta {
  font-size: 15px;
}

/* ================= THICKNESS (FINAL FIX) ================= */

/* Slight increase in thickness placeholder height */
.thickness-card-full {
  height: calc(100% + 2px);
}

.thickness-content-full {
  display: flex;
  flex-direction: row;
  height: 100%;
  padding-top: 6px;          /* 👈 lifts graph + data together */
}

/* Graph slightly wider */
.thickness-graph-full {
  flex: 1 1 82%;          /* ⬅ wider than before */
  position: relative;
  min-height: 100%;
  margin-top: -6px;
}

/* Data panel pushed further right */
.thickness-info-full {
  flex: 0 0 18%;          /* ⬅ slightly narrower panel */
  font-size: 14px;
  line-height: 1.7;

  margin-left: 40px;     /* ⬅ main push to the right */
  padding-left: 16px;

  margin-top: -6px;
}



/* Make labels slightly stronger */
.thickness-info-full b {
  font-size: 15px;
  font-weight: 700;
}

/* Force canvas to fill graph box */
.thickness-graph-full canvas {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
}



/* ================= OEE ================= */
.oee-grid {
  display: grid;
  gap: 14px;
}

.oee-box {
  background: rgba(255,255,255,0.14);
  border-radius: 14px;
  padding: 14px;
  text-align: center;
}

/* ================= FOOTER ================= */
.footer {
  height: 51px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 1.6px;
  text-transform: uppercase;
  color: #eaf7fb;
  background: linear-gradient(180deg, #123a52, #081c28);
}



/* ========================================= */
/* HEADER TITLE – GRADIENT TEXT (PREMIUM)    */
/* ========================================= */

.topbar h1 {
  font-family: "Inter", "SF Pro Display", "Segoe UI Variable",
               -apple-system, BlinkMacSystemFont, system-ui, sans-serif;

  font-size: 26px;
  font-weight: 700;
  letter-spacing: 1.1px;
  text-transform: uppercase;

  /* Gradient text */
  background: linear-gradient(
    90deg,
    #e6f7fb 0%,
    #7fdcff 40%,
    #4dd0e1 70%,
    #e6f7fb 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;

  /* Clean, subtle depth */
  text-shadow:
    0 1px 1px rgba(255,255,255,0.03),
    0 2px 4px rgba(0,0,0,0.35);

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ========================================= */
/* HEADER RIGHT – CLEAN & ALIGNED             */
/* ========================================= */

.top-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

/* Clock pill layout fix */
.top-right .pill.dark {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  font-size: 12px;
  line-height: 1.4;
  padding: 8px 14px;
  min-width: 120px;
  height: 44px;

  text-align: center;
  border-radius: 14px;
}

/* ========================================= */
/* CLOCK PILL – BIGGER & BOLDER (CLEAN)      */
/* ========================================= */

.top-right .pill.dark {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  padding: 10px 16px;
  min-width: 130px;
  height: auto;

  font-size: 13.5px;        /* bigger */
  font-weight: 600;         /* slightly bold */
  line-height: 1.35;
  letter-spacing: 0.4px;

  text-align: center;
  white-space: normal;
  word-break: break-word;

  border-radius: 14px;
}


/* ========================================= */
/* HEADER ICONS – SLIGHTLY BIGGER             */
/* ========================================= */

.notification-icon,
.power-icon {
  width: 30px;          /* increased from 26px */
  height: 30px;
  flex-shrink: 0;
}

/* Ensure images render crisply */
.top-right img {
  max-width: 30px;
  max-height: 30px;
}


.notification-icon {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.left-panel > h2 {
  margin-top: -10px;   
}

/* ========================================= */
/* Increase graph placeholder height (+2px) */
/* EXCEPT thickness graph                   */
/* ========================================= */

/* Individual graph boxes */
.graph-row {
  min-height: calc(120px + 2px);   /* was 120px */
}

/* Dual graph rows (LIP, MAP, IBC, SPEED) */
.dual-graph-row {
  min-height: calc(160px + 2px);   /* was 160px */
}

/* Explicitly exclude thickness */
.thickness-card-full {
  min-height: unset;               /* untouched */
}


.row-title {
  font-size: 13.5px;        /* was ~11px */
  font-weight: 700;
  letter-spacing: 0.9px;
  text-transform: uppercase;
}

/* ========================================= */
/* GLOBAL HOVER EFFECTS – BOXES & CARDS       */
/* ========================================= */

/* Common transition for all interactive boxes */
.panel,
.row,
.stat,
.die-zone,
.oee-box,
.menu-item {
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    background-color 0.25s ease;
}

/* Main panels */
.panel:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(0,0,0,0.35);
}

/* Inner cards / rows */
.row:hover {
  background: rgba(255,255,255,0.14);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.30);
}

/* Top stats cards */
.stat:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 8px 22px rgba(0,0,0,0.35);
}

/* Die temperature zones */
.die-zone:hover {
  transform: scale(1.04);
  box-shadow: 0 6px 18px rgba(0,0,0,0.40);
}

/* OEE boxes */
.oee-box:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 8px 20px rgba(0,0,0,0.35);
}

/* Sidebar menu items */
.menu-item:hover {
  background: rgba(127,220,255,0.22);
  transform: translateX(4px);
  box-shadow: inset 0 0 0 1px rgba(127,220,255,0.35);
}

/* ========================================= */
/* DISABLE HOVER ON TOUCH SCREENS             */
/* ========================================= */
@media (hover: none) {
  .panel:hover,
  .row:hover,
  .stat:hover,
  .die-zone:hover,
  .oee-box:hover,
  .menu-item:hover {
    transform: none;
    box-shadow: none;
  }
}


/* ========================================= */
/* MODERN FONT SMOOTHING (SAFE ADDITION)      */
/* ========================================= */

html, body, #app {
  -webkit-font-smoothing: antialiased;   /* Chrome / Edge / Safari */
  -moz-osx-font-smoothing: grayscale;    /* macOS Firefox */
  text-rendering: optimizeLegibility;
}

/* Slightly improve readability for UI text */
body, button, input, select, textarea {
  font-feature-settings: "kern" 1, "liga" 1;
  letter-spacing: 0.15px;
}

/* Headings get cleaner spacing */
h1, h2, .row-title {
  letter-spacing: 0.9px;
}


/* ========================================= */
/* NOTIFICATION ICON – CLEAN & TRANSPARENT   */
/* ========================================= */

.notification-icon {
  background: transparent !important;   /* remove white bg */
  border-radius: 6px;                   /* smooth edges */
  transition: box-shadow 0.2s ease;
}

/* Optional subtle hover */
.notification-icon:hover {
  box-shadow: 0 0 8px rgba(127,220,255,0.25);
}

/* ========================================= */
/* UNIVERSAL PREMIUM INTERACTION SYSTEM      */
/* ========================================= */

/* Elements that should glow */
.panel,
.row,
.stat,
.die-zone,
.oee-box,
.menu-item,
.notification-icon,
.power-icon,
.pill.dark,
.back-icon {
  position: relative;
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    background-color 0.25s ease;
}

/* Hover glow */
.panel:hover,
.row:hover,
.stat:hover,
.die-zone:hover,
.oee-box:hover,
.menu-item:hover,
.notification-icon:hover,
.power-icon:hover,
.pill.dark:hover,
.back-icon:hover {
  transform: translateY(-2px) scale(1.02);

  box-shadow:
    0 0 0 1px rgba(127,220,255,0.25),
    0 10px 28px rgba(0,0,0,0.35),
    0 0 18px rgba(127,220,255,0.35);

  background-color: rgba(255,255,255,0.16);
}

/* Click feedback */
.panel:active,
.row:active,
.stat:active,
.die-zone:active,
.oee-box:active,
.menu-item:active,
.notification-icon:active,
.power-icon:active,
.pill.dark:active,
.back-icon:active {
  transform: scale(0.97);
}

/* Glassmorphism polish */
.panel,
.row,
.stat,
.die-zone,
.oee-box,
.pill.dark,
.back-icon {
  backdrop-filter: blur(6px);
}

</style>