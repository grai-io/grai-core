import {
  BarElement,
  CategoryScale,
  Chart,
  ChartOptions,
  LinearScale,
} from "chart.js"
import React from "react"
import { Bar } from "react-chartjs-2"
import theme from "theme"
import ChartDataLabels from "chartjs-plugin-datalabels"
import { lighten } from "@mui/material"

const BarChart: React.FC = () => {
  const data = [
    { category: "credit-card", count: 25 },
    { category: "cash", count: 15 },
    { category: "bnpl", count: 5 },
    { category: "other", count: 45 },
  ]

  Chart.register(CategoryScale, LinearScale, BarElement, ChartDataLabels)

  const options: ChartOptions<"bar"> = {
    scales: {
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: theme.palette.text.secondary,
          font: {
            size: 14,
          },
        },
      },
      y: {
        display: false,
      },
    },
  }

  return (
    <Bar
      data={{
        labels: data.map(row => row.category),
        datasets: [
          {
            data: data.map(row => row.count),
            backgroundColor: lighten(theme.palette.info.main, 0.75),
            borderRadius: 3,
            datalabels: {
              font: {
                size: 14,
              },
            },
          },
        ],
      }}
      options={options}
    />
  )
}

export default BarChart
