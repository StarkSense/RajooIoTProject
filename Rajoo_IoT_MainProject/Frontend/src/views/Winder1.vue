<template>
  <section class="panel full-panel">
    <h2>WINDER 1</h2>

    <!-- ================= KPI ROW ================= -->
    <div class="kpi-row">
      <div class="kpi-tile">
        <div class="kpi-title">TOTALIZER</div>
        <div class="kpi-value">{{ winder.totalizer }}</div>
        <div class="kpi-unit">m</div>
      </div>

      <div class="kpi-tile">
        <div class="kpi-title">ROLL LENGTH</div>
        <div class="kpi-value">{{ latestRollLength }}</div>
        <div class="kpi-unit">m</div>
      </div>

      <div class="kpi-tile">
        <div class="kpi-title">ROLL DIAMETER</div>
        <div class="kpi-value">{{ latestRollDia }}</div>
        <div class="kpi-unit">mm</div>
      </div>
    </div>

    <!-- ================= ROLL LENGTH ================= -->
    <div class="chart-card">
      <div class="chart-header">
        <span>ROLL LENGTH</span>
        <span class="badge">{{ latestRollLength }} m</span>
      </div>
      <canvas ref="rollLengthChart"></canvas>
    </div>

    <!-- ================= ROLL DIAMETER ================= -->
    <div class="chart-card">
      <div class="chart-header">
        <span>ROLL DIAMETER</span>
        <span class="badge">{{ latestRollDia }} mm</span>
      </div>
      <canvas ref="rollDiaChart"></canvas>
    </div>
  </section>
</template>

<script>
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from "chart.js";

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
);

export default {
  name: "Winder1",

  data() {
    return {
      winder: {
        totalizer: 0,
        rollLength: [],
        rollDia: []
      },
      rollLengthChart: null,
      rollDiaChart: null
    };
  },

  computed: {
    latestRollLength() {
      return this.winder.rollLength.at(-1) || 0;
    },
    latestRollDia() {
      return this.winder.rollDia.at(-1) || 0;
    }
  },

  mounted() {
    this.initCharts();

    this.$socket.on("telemetry_update", (payload) => {
      const w = payload?.winder_data?.winder1;
      const t = payload?.winder_trends?.winder1;

      if (w) this.winder.totalizer = w.totalizer;
      if (t) {
        this.winder.rollLength = t.roll_length || [];
        this.winder.rollDia = t.roll_dia || [];
        this.updateCharts();
      }
    });
  },

  methods: {
    initCharts() {
      this.rollLengthChart = this.createChart(
        this.$refs.rollLengthChart,
        "Roll Length (m)",
        "#5eead4"
      );

      this.rollDiaChart = this.createChart(
        this.$refs.rollDiaChart,
        "Roll Diameter (mm)",
        "#60a5fa"
      );
    },

    createChart(canvas, label, color) {
      return new Chart(canvas, {
        type: "line",
        data: {
          labels: [],
          datasets: [
            {
              label,
              data: [],
              borderColor: color,
              tension: 0.35,
              pointRadius: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: "#cbd5e1" } }
          },
          scales: {
            x: {
              ticks: { color: "#94a3b8" },
              grid: { color: "rgba(255,255,255,0.05)" }
            },
            y: {
              ticks: { color: "#94a3b8" },
              grid: { color: "rgba(255,255,255,0.05)" }
            }
          }
        }
      });
    },

    updateCharts() {
      this.rollLengthChart.data.labels =
        this.winder.rollLength.map((_, i) => i + 1);
      this.rollLengthChart.data.datasets[0].data =
        this.winder.rollLength;
      this.rollLengthChart.update();

      this.rollDiaChart.data.labels =
        this.winder.rollDia.map((_, i) => i + 1);
      this.rollDiaChart.data.datasets[0].data =
        this.winder.rollDia;
      this.rollDiaChart.update();
    }
  }
};
</script>

<style scoped>
.kpi-row {
  display: flex;
  gap: 20px;
  margin: 20px 0 28px;
}

.kpi-tile {
  background: linear-gradient(180deg, #4a5f6b, #3a4d57);
  border-radius: 16px;
  padding: 18px 26px;
  min-width: 220px;
  text-align: center;
}

.kpi-title {
  font-size: 13px;
  opacity: 0.8;
}

.kpi-value {
  font-size: 30px;
  font-weight: 700;
  color: #7fffd4;
}

.kpi-unit {
  font-size: 12px;
  opacity: 0.7;
}

.chart-card {
  background: #445862;
  border-radius: 16px;
  padding: 14px 18px 18px;
  margin-bottom: 22px;
  height: 260px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.badge {
  background: #2b6f85;
  padding: 4px 10px;
  border-radius: 12px;
}
</style>
