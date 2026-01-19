<template>
  <div class="app">
    <!-- LEFT SIDEBAR -->
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>
        <button class="menu-item" :class="{ active: isActive('/layer1') }" @click="goToLayer('/layer1')">Layer 1</button>
        <button class="menu-item" :class="{ active: isActive('/layer2') }" @click="goToLayer('/layer2')">Layer 2</button>
        <button class="menu-item" :class="{ active: isActive('/layer3') }" @click="goToLayer('/layer3')">Layer 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>
        <button class="menu-item" :class="{ active: isActive('/extruder1') }" @click="goTo('/extruder1')">Extruder 1</button>
        <button class="menu-item" :class="{ active: isActive('/extruder2') }" @click="goTo('/extruder2')">Extruder 2</button>
        <button class="menu-item" :class="{ active: isActive('/extruder3') }" @click="goTo('/extruder3')">Extruder 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">WINDER</div>
        <button class="menu-item" :class="{ active: isActive('/winder1') }" @click="goTo('/winder1')">Winder 1</button>
        <button class="menu-item" :class="{ active: isActive('/winder2') }" @click="goTo('/winder2')">Winder 2</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">UTILITIES</div>
        <button class="menu-item" :class="{ active: isActive('/reports') }" @click="goTo('/reports')">Reports</button>
        <button class="menu-item" :class="{ active: isActive('/material-utilization') }" @click="goTo('/material-utilization')">Material Utilization</button>
      </div>
    </aside>

    <!-- MAIN -->
    <main class="main">
      <!-- TOP BAR -->
      <header class="topbar">
        <h1>THREE LAYER BLOWN FILM LINE</h1>
        <div class="top-right">
          <span class="pill dark">{{ currentDate }}<br />{{ currentTime }}</span>
          <img src="/notification.png" class="notification-icon" />
          <img src="/power-button.png" class="power-icon" @click="handleLogout" />
        </div>
      </header>

      <!-- CONTENT -->
      <div class="content">
        <!-- MACHINE OVERVIEW -->
        <section class="panel left-panel">
          <h2>MACHINE OVERVIEW PANEL</h2>

          <div class="stats">
            <div class="stat">Total Set Output<span>{{ total_set_output.toFixed(2) }} kg/hr</span></div>
            <div class="stat">Total Actual Output<span>{{ total_actual_output.toFixed(2) }} kg/hr</span></div>
            <div class="stat">Density<span>{{ density.toFixed(2) }} g/cm³</span></div>
            <div class="stat">GSM<span>{{ gsm.toFixed(2) }}</span></div>
            <div class="stat">Lay Flat<span>{{ lay_flat.toFixed(2) }} mm</span></div>
          </div>

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

          <!-- DIE TEMP -->
          <div class="row die-zone-card">
            <div class="row-title">DIE TEMPERATURE ZONE WISE</div>
            <div class="die-zone-grid">
              <div v-for="zone in die_temp_zones" :key="zone.zone" class="die-zone" :class="zoneStatus(zone)">
                <div class="zone-name">{{ zone.zone }}</div>
                <div class="zone-values">
                  <div>SET {{ zone.set.toFixed(1) }}°C</div>
                  <div>ACT {{ zone.actual.toFixed(1) }}°C</div>
                  <div class="delta">Δ {{ (zone.actual - zone.set).toFixed(1) }}°C</div>
                </div>
              </div>
            </div>
          </div>

          <!-- THICKNESS -->
          <div class="row thickness-card-full">
            <div class="row-title">THICKNESS</div>
            <div class="thickness-content-full">
              <div class="thickness-graph-full">
                <Line :data="thicknessChartData" :options="thicknessChartOptions" />
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

/* ================= GLOBAL CHART SAFETY ================= */
ChartJS.defaults.responsive = true;
ChartJS.defaults.maintainAspectRatio = false;

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

      /* ================= KPIs ================= */
      total_set_output: 0,
      total_actual_output: 0,
      density: 0,
      gsm: 0,
      lay_flat: 0,

      /* ================= RAW DATA ================= */
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
      /* ================= KPIs ================= */
      if (data.machine_overview) {
        const m = data.machine_overview;
        this.total_set_output = Number(m.total_set_output || 0);
        this.total_actual_output = Number(m.total_actual_output || 0);
        this.density = Number(m.density || 0);
        this.gsm = Number(m.gsm || 0);
        this.lay_flat = Number(m.lay_flat || 0);
      }

      /* ================= PROFILES ================= */
      this.lip_profile = data.lip_profile ?? [];
      this.map_profile = data.map_profile ?? [];

      /* ================= TIME-SERIES ================= */
      this.ibc_temp_in = this.toXYWithTime(data.ibc_temp?.in ?? []);
      this.ibc_temp_out = this.toXYWithTime(data.ibc_temp?.out ?? []);
      this.speed_set = this.toXYWithTime(data.speed_trend?.set ?? []);
      this.speed_actual = this.toXYWithTime(data.speed_trend?.actual ?? []);

      /* ================= DIE TEMP ================= */
      this.die_temp_zones = data.die_temp_zones ?? [];

      /* ================= THICKNESS ================= */
      if (data.thickness) {
        this.thickness_trend = this.toXYWithTime(data.thickness.trend ?? []);
        this.thickness_stats = {
          ...this.thickness_stats,
          ...data.thickness.stats
        };
      }
    });
  },

  methods: {
    /* ===== Convert values → timestamps ===== */
    toXYWithTime(series) {
      const now = new Date();
      return series.map((v, i) => {
        const t = new Date(now.getTime() - (series.length - i - 1) * 10000);
        return {
          x: t.toLocaleTimeString("en-GB"),
          y: v
        };
      });
    },

    /* ===== Navigation ===== */
    goToLayer(path) {
      if (this.$route.path !== path) this.$router.push(path);
    },
    goTo(path) {
      if (this.$route.path !== path) this.$router.push(path);
    },
    isActive(path) {
      return this.$route.path === path;
    },

    /* ===== Clock ===== */
    updateClock() {
      const now = new Date();
      this.currentDate = now.toLocaleDateString("en-GB");
      this.currentTime = now.toLocaleTimeString("en-GB");
    },

    zoneStatus(zone) {
      const diff = Math.abs(zone.actual - zone.set);
      if (diff <= 2) return "ok";
      if (diff <= 5) return "warn";
      return "alert";
    },

    handleLogout() {
      if (this.socket) this.socket.disconnect();
      localStorage.removeItem("token");
      this.$router.replace("/");
    },

    /* ================= CHART OPTIONS ================= */
    commonOptions(xLabel, yLabel, legend = false) {
      return {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        resizeDelay: 150,

        plugins: {
          legend: legend
            ? {
                labels: {
                  color: "#e6f7fb",
                  font: { size: 14, weight: "600" }
                }
              }
            : { display: false },

          tooltip: {
            backgroundColor: "rgba(10,25,35,0.95)",
            titleColor: "#ffffff",
            bodyColor: "#e6f7fb",
            borderColor: "#7fdcff",
            borderWidth: 1
          }
        },

        scales: {
          x: {
            title: {
              display: true,
              text: xLabel,
              color: "#ffffff",
              font: { size: 14, weight: "600" }
            },
            ticks: {
              color: "#dff6ff",
              font: { size: 12 }
            },
            grid: {
              color: "rgba(255,255,255,0.12)"
            }
          },
          y: {
            title: {
              display: true,
              text: yLabel,
              color: "#ffffff",
              font: { size: 14, weight: "600" }
            },
            ticks: {
              color: "#dff6ff",
              font: { size: 12 }
            },
            grid: {
              color: "rgba(255,255,255,0.12)"
            }
          }
        }
      };
    }
  },

  computed: {
    /* ================= DATASETS ================= */
    lipChartData() {
      return {
        labels: this.lip_profile.map(p => p.x),
        datasets: [{
          data: this.lip_profile.map(p => p.y),
          borderColor: "#7fdcff",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 3
        }]
      };
    },

    mapChartData() {
      return {
        labels: this.map_profile.map(p => p.x),
        datasets: [{
          data: this.map_profile.map(p => p.y),
          borderColor: "#81c784",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 3
        }]
      };
    },

    ibcChartData() {
      return {
        labels: this.ibc_temp_in.map(p => p.x),
        datasets: [
          { label: "IBC IN", data: this.ibc_temp_in.map(p => p.y) },
          { label: "IBC OUT", data: this.ibc_temp_out.map(p => p.y) }
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
            borderWidth: 3,
            tension: 0.35
          },
          {
            label: "Set Thickness",
            data: labels.map(() => this.thickness_stats.set),
            borderColor: "#4dd0e1",
            borderDash: [6, 4]
          }
        ]
      };
    },

    /* ================= OPTIONS ================= */
    lipChartOptions() {
      return this.commonOptions("Die Width", "Thickness (µm)");
    },
    mapChartOptions() {
      return this.commonOptions("Die Width", "Thickness (µm)");
    },
    ibcChartOptions() {
      return this.commonOptions("Time (HH:MM:SS)", "Temperature (°C)", true);
    },
    speedChartOptions() {
      return this.commonOptions("Time (HH:MM:SS)", "Speed", true);
    },
    thicknessChartOptions() {
      return this.commonOptions("Time (HH:MM:SS)", "Thickness (µm)");
    }
  }
};
</script>


<!-- <script>
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

/* ================= GLOBAL CHART SAFETY ================= */
ChartJS.defaults.responsive = true;
ChartJS.defaults.maintainAspectRatio = false;

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

      /* ================= KPIs ================= */
      total_set_output: 0,
      total_actual_output: 0,
      density: 0,
      gsm: 0,
      lay_flat: 0,

      /* ================= TELEMETRY ================= */
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
      /* ================= MACHINE OVERVIEW ================= */
      if (data.machine_overview) {
        const m = data.machine_overview;
        this.total_set_output = Number(m.total_set_output || 0);
        this.total_actual_output = Number(m.total_actual_output || 0);
        this.density = Number(m.density || 0);
        this.gsm = Number(m.gsm || 0);
        this.lay_flat = Number(m.lay_flat || 0);
      }

      /* ================= PROFILES ================= */
      this.lip_profile = data.lip_profile ?? [];
      this.map_profile = data.map_profile ?? [];

      /* ================= TIME SERIES ================= */
      this.ibc_temp_in = this.toXY(data.ibc_temp?.in ?? []);
      this.ibc_temp_out = this.toXY(data.ibc_temp?.out ?? []);
      this.speed_set = this.toXY(data.speed_trend?.set ?? []);
      this.speed_actual = this.toXY(data.speed_trend?.actual ?? []);

      /* ================= DIE TEMPERATURE ================= */
      this.die_temp_zones = data.die_temp_zones ?? [];

      /* ================= THICKNESS ================= */
      if (data.thickness) {
        this.thickness_trend = this.toXY(data.thickness.trend ?? []);
        this.thickness_stats = {
          ...this.thickness_stats,
          ...data.thickness.stats
        };
      }
    });
  },

  methods: {
    /* ================= HELPERS ================= */
    toXY(series) {
      return series.map((v, i) => ({ x: i + 1, y: v }));
    },

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

    handleLogout() {
      if (this.socket) this.socket.disconnect();
      localStorage.removeItem("token");
      this.$router.replace("/");
    },

    /* ================= NAVIGATION ================= */
    goToLayer(path) {
      if (this.$route.path !== path) this.$router.push(path);
    },
    goTo(path) {
      if (this.$route.path !== path) this.$router.push(path);
    },
    isActive(path) {
      return this.$route.path === path;
    },

    /* ================= CHART OPTIONS (READABLE) ================= */
    commonOptions(xLabel, yLabel, showLegend = false) {
      return {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        resizeDelay: 150,

        plugins: {
          legend: showLegend
            ? {
                labels: {
                  color: "#e6f7fb",
                  font: { size: 14, weight: "600" },
                  boxWidth: 18,
                  padding: 16
                }
              }
            : { display: false },

          tooltip: {
            backgroundColor: "rgba(15,35,50,0.95)",
            titleColor: "#ffffff",
            bodyColor: "#e6f7fb",
            borderColor: "#7fdcff",
            borderWidth: 1,
            titleFont: { size: 14, weight: "600" },
            bodyFont: { size: 13 }
          }
        },

        scales: {
          x: {
            title: {
              display: true,
              text: xLabel,
              color: "#ffffff",
              font: { size: 14, weight: "600" }
            },
            ticks: {
              color: "#dff6ff",
              font: { size: 12, weight: "500" },
              padding: 6
            },
            grid: {
              color: "rgba(255,255,255,0.12)"
            }
          },
          y: {
            title: {
              display: true,
              text: yLabel,
              color: "#ffffff",
              font: { size: 14, weight: "600" }
            },
            ticks: {
              color: "#dff6ff",
              font: { size: 12, weight: "500" },
              padding: 6
            },
            grid: {
              color: "rgba(255,255,255,0.12)"
            }
          }
        }
      };
    }
  },

  computed: {
    /* ================= DATASETS ================= */
    lipChartData() {
      return {
        labels: this.lip_profile.map(p => p.x),
        datasets: [{
          data: this.lip_profile.map(p => p.y),
          borderColor: "#7fdcff",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 3,
          pointBackgroundColor: "#ffffff"
        }]
      };
    },

    mapChartData() {
      return {
        labels: this.map_profile.map(p => p.x),
        datasets: [{
          data: this.map_profile.map(p => p.y),
          borderColor: "#81c784",
          borderWidth: 2.5,
          tension: 0.35,
          pointRadius: 3,
          pointBackgroundColor: "#ffffff"
        }]
      };
    },

    ibcChartData() {
      return {
        labels: this.ibc_temp_in.map(p => p.x),
        datasets: [
          {
            label: "IBC IN",
            data: this.ibc_temp_in.map(p => p.y),
            backgroundColor: "rgba(77,208,225,0.7)"
          },
          {
            label: "IBC OUT",
            data: this.ibc_temp_out.map(p => p.y),
            backgroundColor: "rgba(255,183,77,0.7)"
          }
        ]
      };
    },

    speedChartData() {
      return {
        labels: this.speed_set.map(p => p.x),
        datasets: [
          {
            label: "SET",
            data: this.speed_set.map(p => p.y),
            borderColor: "#4dd0e1",
            borderWidth: 2.5,
            tension: 0.3
          },
          {
            label: "ACT",
            data: this.speed_actual.map(p => p.y),
            borderColor: "#ff7043",
            borderWidth: 2.5,
            tension: 0.3
          }
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
            backgroundColor: "rgba(255,112,67,0.15)",
            borderWidth: 3,
            tension: 0.35,
            pointRadius: 3
          },
          {
            label: "Set Thickness",
            data: labels.map(() => this.thickness_stats.set),
            borderColor: "#4dd0e1",
            borderDash: [6, 4],
            borderWidth: 2,
            pointRadius: 0
          }
        ]
      };
    },

    /* ================= OPTIONS ================= */
    lipChartOptions() { return this.commonOptions("Die Width", "Thickness"); },
    mapChartOptions() { return this.commonOptions("Die Width", "Thickness"); },
    ibcChartOptions() { return this.commonOptions("Time", "Temperature", true); },
    speedChartOptions() { return this.commonOptions("Time", "Speed", true); },
    thicknessChartOptions() { return this.commonOptions("Time", "Thickness"); }
  }
};
</script> -->



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



/* ========================================= */
/* 🔒 CHART FULLSCREEN / OVERFLOW FIX        */
/* ========================================= */

.graph-row,
.thickness-graph-full {
  position: relative;
  overflow: hidden;
}

/* Lock canvas inside its container */
.graph-row canvas,
.thickness-graph-full canvas {
  position: relative !important;
  width: 100% !important;
  height: 100% !important;
  max-width: 100% !important;
  max-height: 100% !important;
  display: block;
}

/* Prevent Chart.js from escaping flex parents */
.row,
.graph-row,
.dual-graph-row,
.thickness-card-full {
  contain: layout paint size;
}


/* ===== DIE ZONE FIX (VISIBLE Z1–Z7) ===== */
.die-zone-card {
  min-height: 140px;
  overflow: visible;
}

.die-zone-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 14px;
  width: 100%;
}

.die-zone {
  min-height: 92px;
  border-radius: 14px;
  padding: 12px 8px;
  text-align: center;
  font-size: 12px;
  font-weight: 700;

  background: linear-gradient(
    180deg,
    rgba(255,255,255,0.18),
    rgba(255,255,255,0.08)
  );

  border: 1px solid rgba(127,220,255,0.3);
  backdrop-filter: blur(6px);
}

/* Zone states */
.die-zone.ok {
  border-color: rgba(110,231,183,0.6);
}

.die-zone.warn {
  border-color: rgba(255,183,77,0.7);
}

.die-zone.alert {
  border-color: rgba(255,112,67,0.8);
}

/* Text clarity */
.zone-name {
  font-size: 15px;
  margin-bottom: 6px;
}

.zone-values div {
  font-size: 13px;
}

.delta {
  font-size: 14px;
}




/* Make chart containers slightly darker */
.graph-row,
.thickness-graph-full {
  background: rgba(0, 0, 0, 0.18);
  border-radius: 12px;
  padding: 6px;
}

/* Improve canvas text contrast */
canvas {
  filter: contrast(1.08) brightness(1.05);
}

/* Axis label clarity on high DPI screens */
.chartjs-render-monitor {
  image-rendering: crisp-edges;
}


</style>