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
        <button class="menu-item" @click="navigate('/extruder3')">Extruder C</button>
      </div>

      <div class="menu-section">
        <div class="menu-title">WINDER</div>
        <button class="menu-item" @click="navigate('/winder1')">Winder 1</button>
        <button class="menu-item active">Winder 2</button>
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
          <h2>WINDER 2</h2>

          <div class="stats centered">
            <div class="kpi-outer">
              <div class="kpi-inner">
                <div class="kpi-title">TOTALIZER</div>
                <div class="kpi-value">
                  {{ totalizer }} <span class="kpi-unit">m</span>
                </div>
              </div>
            </div>
          </div>

          <div class="graph-section">
            <div class="graph-header">
              <span>ROLL LENGTH</span>
              <span class="badge">{{ rollLengthLatest }} m</span>
            </div>
            <div class="graph-card">
              <canvas ref="rollLengthChart"></canvas>
            </div>
          </div>

          <div class="graph-section">
            <div class="graph-header">
              <span>ROLL DIAMETER</span>
              <span class="badge">{{ rollDiaLatest }} mm</span>
            </div>
            <div class="graph-card">
              <canvas ref="rollDiaChart"></canvas>
            </div>
          </div>
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
import socket from "@/services/socket";
import {
  Chart,
  LineController,
  LineElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js";

Chart.register(
  LineController,
  LineElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

const MAX_POINTS = 30;
const CHART_INTERVAL = 3000;

export default {
  name: "Winder2",

  data() {
    return {
      totalizer: 0,
      rollLengthLatest: 0,
      rollDiaLatest: 0,
      currentDate: "",
      currentTime: "",
      lastChartUpdate: 0,
      graphSeeded: false,
      _telemetryHandler: null
    };
  },

  mounted() {
    this.updateClock();
    this._clockTimer = setInterval(this.updateClock, 1000);

    this._lengthLabels = [];
    this._lengthData = [];
    this._diaLabels = [];
    this._diaData = [];

    this.createCharts();

    this._telemetryHandler = this.onTelemetry;
    socket.on("telemetry_update", this._telemetryHandler);
  },

  beforeUnmount() {
    clearInterval(this._clockTimer);

    if (this._telemetryHandler) {
      socket.off("telemetry_update", this._telemetryHandler);
    }

    this.rollLengthChart?.destroy();
    this.rollDiaChart?.destroy();
  },

  methods: {
    navigate(path) {
      this.$router.push(path);
    },

    goBack() {
      this.$router.push("/dashboard");
    },

    updateClock() {
      const d = new Date();
      this.currentDate = d.toLocaleDateString("en-GB");
      this.currentTime = d.toLocaleTimeString("en-GB");
    },

    onTelemetry(payload) {
      const w = payload?.winder_data?.winder2;
      const t = payload?.winder_trends?.winder2;
      if (!w || !t) return;

      this.totalizer = w.totalizer ?? this.totalizer;

      const latestLength = t.roll_length?.at(-1);
      const latestDia = t.roll_dia?.at(-1);
      if (latestLength == null || latestDia == null) return;

      this.rollLengthLatest = latestLength;
      this.rollDiaLatest = latestDia;

      // ===== INITIAL SEED =====
      if (!this.graphSeeded) {
        const lenSeries = t.roll_length.slice(-MAX_POINTS);
        const diaSeries = t.roll_dia.slice(-MAX_POINTS);

        const now = Date.now();

        this._lengthLabels = lenSeries.map((_, i) =>
          new Date(now - (lenSeries.length - i) * 1000)
            .toLocaleTimeString("en-GB")
        );

        this._lengthData = [...lenSeries];
        this._diaLabels = [...this._lengthLabels];
        this._diaData = [...diaSeries];

        this.rollLengthChart.data.labels = this._lengthLabels;
        this.rollLengthChart.data.datasets[0].data = this._lengthData;

        this.rollDiaChart.data.labels = this._diaLabels;
        this.rollDiaChart.data.datasets[0].data = this._diaData;

        this.rollLengthChart.update("none");
        this.rollDiaChart.update("none");

        this.graphSeeded = true;
        return;
      }

      // ===== THROTTLED UPDATE =====
      const now = Date.now();
      if (now - this.lastChartUpdate < CHART_INTERVAL) return;
      this.lastChartUpdate = now;

      const time = new Date().toLocaleTimeString("en-GB");

      this._lengthLabels.push(time);
      this._lengthData.push(latestLength);
      this._diaLabels.push(time);
      this._diaData.push(latestDia);

      if (this._lengthLabels.length > MAX_POINTS) {
        this._lengthLabels.shift();
        this._lengthData.shift();
        this._diaLabels.shift();
        this._diaData.shift();
      }

      this.rollLengthChart.data.labels = this._lengthLabels;
      this.rollLengthChart.data.datasets[0].data = this._lengthData;
      this.rollLengthChart.update("none");

      this.rollDiaChart.data.labels = this._diaLabels;
      this.rollDiaChart.data.datasets[0].data = this._diaData;
      this.rollDiaChart.update("none");
    },

    createCharts() {
      // ===== ROLL LENGTH =====
      this.rollLengthChart = new Chart(this.$refs.rollLengthChart, {
        type: "line",
        data: {
          labels: [],
          datasets: [{
            label: "Roll Length",
            data: [],
            stepped: true,
            borderColor: "#7fdcff",
            backgroundColor: "#7fdcff33",
            fill: true,
            pointRadius: 0,
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          plugins: {
            legend: { labels: { color: "#e6f7fb" } }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Time",
                color: "#e6f7fb"
              },
              ticks: { color: "#cfefff" },
              grid: { color: "rgba(255,255,255,0.08)" }
            },
            y: {
              title: {
                display: true,
                text: "Length (m)",
                color: "#e6f7fb"
              },
              ticks: { color: "#cfefff" },
              grid: { color: "rgba(255,255,255,0.08)" }
            }
          }
        }
      });

      // ===== ROLL DIAMETER =====
      this.rollDiaChart = new Chart(this.$refs.rollDiaChart, {
        type: "line",
        data: {
          labels: [],
          datasets: [{
            label: "Roll Diameter",
            data: [],
            stepped: true,
            borderColor: "#4dd0e1",
            backgroundColor: "#4dd0e133",
            fill: true,
            pointRadius: 0,
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          plugins: {
            legend: { labels: { color: "#e6f7fb" } }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Time",
                color: "#e6f7fb"
              },
              ticks: { color: "#cfefff" },
              grid: { color: "rgba(255,255,255,0.08)" }
            },
            y: {
              title: {
                display: true,
                text: "Diameter (mm)",
                color: "#e6f7fb"
              },
              ticks: { color: "#cfefff" },
              grid: { color: "rgba(255,255,255,0.08)" }
            }
          }
        }
      });
    }
  }
};
</script>


<style scoped>
/* ================= HEADER / TITLE ROW ================= */

.top-left,
.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-heading {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 0.6px;
  color: #e6f7fb;
}

/* ================= BACK BUTTON (UNIFIED) ================= */

.back-icon {
  width: 38px;
  height: 38px;
  cursor: pointer;
  border-radius: 50%;
  padding: 6px;

  /* glass effect */
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
    inset 0 0 0 1px rgba(255, 255, 255, 0.35);
}

.back-icon:active {
  transform: scale(0.96);
}

/* ================= KPI ================= */

.stats.centered {
  display: flex;
  justify-content: center;
}

.kpi-outer {
  padding: 8px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.15);
}

.kpi-inner {
  padding: 18px 28px;
  border-radius: 14px;
  background: linear-gradient(180deg, #4a5f6b, #3a4d57);
  text-align: center;
}

.kpi-title {
  font-size: 13px;
  opacity: 0.8;
}

.kpi-value {
  font-size: 36px;
  font-weight: 900;
  color: #7fffd4;
}

.kpi-unit {
  font-size: 16px;
  margin-left: 6px;
}

/* ================= GRAPHS ================= */

.graph-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 18px;
}

.graph-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 10px;
  border-radius: 10px;
}

.graph-card {
  height: 240px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 12px;
}

.graph-card canvas {
  width: 100% !important;
  height: 100% !important;
}
</style> 



