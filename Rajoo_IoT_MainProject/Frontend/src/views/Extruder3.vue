<template>
  <div class="app">

    <!-- ================= SIDEBAR ================= -->
    <aside class="sidebar">
      <div class="avatar">
        <img src="/user-icon.png" />
      </div>

      <div class="menu-section">
        <div class="menu-title">LAYERS</div>
        <button class="menu-item" @click="navigate('/layer1')">Layer 1</button>
        <button class="menu-item" @click="navigate('/layer2')">Layer 2</button>
        <button class="menu-item" @click="navigate('/layer3')">Layer 3</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">EXTRUDER</div>
        <button class="menu-item" @click="navigate('/extruder1')">Extruder A</button>
        <button class="menu-item" @click="navigate('/extruder2')">Extruder B</button>
        <button class="menu-item active">Extruder C</button>
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

    <!-- ================= MAIN ================= -->
    <main class="main">

      <header class="topbar">
        <div class="top-left">
          <img src="/back-arrow.png" class="back-icon" @click="goBack" />
          <span class="page-title">THREE LAYER BLOWN FILM LINE</span>
        </div>

        <div class="top-right">
          <span class="pill dark">
            {{ currentDate }}<br />{{ currentTime }}
          </span>

          <!-- 🔔 Notification -->
          <img src="/notification.png" class="notification-icon" />

          <!-- ⏻ Logout / Power -->
          <img src="/power-button.png" class="power-icon" />
        </div>
      </header>

      <div class="content">

        <section class="panel left-panel extruder-panel">
          <h2>EXTRUDER C</h2>

          <div class="material-visuals">

            <div class="visual-card">
              <div class="card-title">ACTUAL COMPOSITION (%)</div>
              <div class="bar-chart-wrapper">
                <canvas ref="compositionChart"></canvas>
              </div>
            </div>

            <div class="visual-card">
              <div class="card-title">SET vs ACTUAL (KG)</div>
              <div class="bar-chart-wrapper">
                <canvas ref="setActualGroupedChart"></canvas>
              </div>
            </div>

            <div class="visual-card">
              <div class="card-title">TOTAL KG (ACTUAL)</div>
              <div class="bar-chart-wrapper">
                <canvas ref="totalKgChart"></canvas>
              </div>
            </div>

            <div class="visual-card">
              <div class="card-title">EXTRUDER TEMPERATURE COMPARISON</div>
              <div class="temp-chart-wrapper">
                <canvas ref="tempBarChart"></canvas>
              </div>
            </div>

          </div>
        </section>
        <!-- RIGHT PANEL -->
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
import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";
import socket from "@/services/socket";

Chart.register(ChartDataLabels);

export default {
  name: "Extruder3",

  data() {
    return {
      currentDate: "",
      currentTime: "",
      compositionChart: null,
      setActualGroupedChart: null,
      totalKgChart: null,
      tempBarChart: null,
      materials: [],
      tempZones: []
    };
  },

  mounted() {
    this.updateClock();
    setInterval(this.updateClock, 1000);
    socket.on("telemetry_update", this.onTelemetryUpdate);
  },

  beforeUnmount() {
    socket.off("telemetry_update", this.onTelemetryUpdate);
    this.destroyCharts();
  },

  methods: {

    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-US");
    },

    onTelemetryUpdate(payload) {
      // 🔥 USING EXTRUDER C
      const extruder = payload?.extruders?.C;
      if (!extruder) return;

      this.materials = Object.entries(extruder.materials).map(([name, m]) => ({
        name,
        set: m.set,
        act: m.act,
        setKg: m.setKg,
        actKg: m.actKg,
        density: m.density,
        color: m.color
      }));

      this.tempZones = extruder.temperature || [];
      this.redrawCharts();
    },

    redrawCharts() {
      setTimeout(() => {
        this.destroyCharts();
        this.drawCompositionChart();
        this.drawSetActualGroupedChart();
        this.drawTotalKgChart();
        this.drawTempBarChart();
      }, 0);
    },

    destroyCharts() {
      this.compositionChart?.destroy();
      this.setActualGroupedChart?.destroy();
      this.totalKgChart?.destroy();
      this.tempBarChart?.destroy();
    },

    drawCompositionChart() {
      this.compositionChart = new Chart(this.$refs.compositionChart, {
        type: "bar",
        data: {
          labels: ["Blend"],
          datasets: this.materials.map(m => ({
            label: m.name,
            data: [Number(m.act) || 0],
            backgroundColor: m.color
          }))
        },
        options: {
          indexAxis: "y",
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "bottom", labels: { color: "#cfe9ff" }},
            datalabels: {
              color: "#fff",
              formatter: v => v > 0 ? v.toFixed(1) + "%" : ""
            }
          },
          scales: {
            x: { stacked: true, min: 0, max: 100, ticks: { color: "#9ecfff" }},
            y: { stacked: true, ticks: { color: "#9ecfff" }}
          }
        }
      });
    },

    drawSetActualGroupedChart() {
      this.setActualGroupedChart = new Chart(this.$refs.setActualGroupedChart, {
        type: "bar",
        data: {
          labels: this.materials.map(m => m.name),
          datasets: [
            { label: "Set (KG)", data: this.materials.map(m => m.setKg), backgroundColor: "#00e5ff" },
            { label: "Actual (KG)", data: this.materials.map(m => m.actKg), backgroundColor: "#ffb300" }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "top", labels: { color: "#cfe9ff" }},
            datalabels: {
              anchor: "end",
              align: "top",
              color: "#fff",
              formatter: v => v > 0 ? v.toFixed(2) : ""
            }
          },
          scales: {
            x: { ticks: { color: "#9ecfff" }},
            y: { ticks: { color: "#9ecfff" }}
          }
        }
      });
    },

    drawTotalKgChart() {
      this.totalKgChart = new Chart(this.$refs.totalKgChart, {
        type: "bar",
        data: {
          labels: this.materials.map(m => m.name),
          datasets: [{
            label: "Actual KG",
            data: this.materials.map(m => m.actKg),
            backgroundColor: this.materials.map(m => m.color)
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            datalabels: {
              anchor: "end",
              align: "top",
              color: "#fff",
              formatter: v => v > 0 ? v.toFixed(2) : ""
            }
          },
          scales: {
            x: { ticks: { color: "#9ecfff" }},
            y: { ticks: { color: "#9ecfff" }}
          }
        }
      });
    },

    drawTempBarChart() {
      this.tempBarChart = new Chart(this.$refs.tempBarChart, {
        type: "bar",
        data: {
          labels: this.tempZones.map(z => z.zone),
          datasets: [
            { label: "Set (°C)", data: this.tempZones.map(z => z.set), backgroundColor: "#00e5ff" },
            { label: "Actual (°C)", data: this.tempZones.map(z => z.act), backgroundColor: "#ffb300" }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "top", labels: { color: "#cfe9ff" }},
            datalabels: {
              anchor: "end",
              align: "top",
              color: "#fff",
              formatter: v => v.toFixed(0) + "°C"
            }
          },
          scales: {
            x: { ticks: { color: "#9ecfff" }},
            y: { ticks: { color: "#9ecfff" }}
          }
        }
      });
    },

    navigate(path) {
      this.$router.push(path);
    },

    goBack() {
      this.$router.push("/dashboard");
    }
  }
};
</script>

<style scoped>

/* ================= BACK BUTTON ================= */
.back-icon {
  width: 38px;
  height: 38px;
  cursor: pointer;
  border-radius: 50%;
  padding: 6px;
  background: rgba(0, 255, 160, 0.12);
  transition: 0.25s;
}
.back-icon:hover {
  background: rgba(0, 255, 160, 0.22);
  transform: scale(1.08);
}

/* ================= TOP BAR ================= */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #9ecfff;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

/* ================= EXTRUDER PANEL ================= */
.extruder-panel {
  display: flex;
  flex-direction: column;
  gap: 18px;   /* slightly reduced */
}

/* ================= GRID LAYOUT ================= */
.material-visuals {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;              /* reduced from 24px */
  align-items: stretch;
}

/* ================= VISUAL CARDS ================= */
.visual-card {
  background: #081c2f;
  padding: 10px 14px;     /* tighter padding */
  border-radius: 16px;
  height: 38vh;           /* 🔥 optimized responsive height */
  display: flex;
  flex-direction: column;
  min-height: 0;          /* 🔥 prevents flex overflow */
}

.card-title {
  font-size: 13px;        /* slightly reduced */
  font-weight: 600;
  color: #cfe9ff;
  margin-bottom: 6px;     /* tighter spacing */
  text-align: center;
}

/* ================= CHART WRAPPERS ================= */
.bar-chart-wrapper,
.temp-chart-wrapper {
  flex: 1;
  position: relative;
  min-height: 0;          /* 🔥 critical for Chart.js inside flex */
}

/* Make canvas fill wrapper properly */
.visual-card canvas {
  width: 100% !important;
  height: 100% !important;
}

/* ================= MATERIAL LEGEND ================= */
.material-legend {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px 16px;         /* reduced spacing */
  margin-top: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.25);
}

.legend-text {
  font-size: 11px;        /* slightly smaller */
  font-weight: 600;
  color: #cfe9ff;
}

</style>

