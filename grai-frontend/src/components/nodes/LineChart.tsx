import {
  Chart,
  ChartData,
  ChartOptions,
  LineElement,
  PointElement,
} from "chart.js"
import React from "react"
import { Scatter } from "react-chartjs-2"
import theme from "theme"
import { lighten } from "@mui/material"

type LineChartProps = {}

const LineChart: React.FC<LineChartProps> = ({}) => {
  Chart.register(PointElement, LineElement)

  const inputData = [
    {
      x: 0,
      y: 0,
    },
    {
      x: 1,
      y: 2,
    },
    {
      x: 2,
      y: 2,
    },
    {
      x: 3,
      y: 4,
    },
    {
      x: 4,
      y: 5,
    },
    {
      x: 5,
      y: 10,
    },
    {
      x: 6,
      y: 11,
    },
    {
      x: 7,
      y: 12,
    },
    {
      x: 8,
      y: 18,
    },
    {
      x: 9,
      y: 19,
    },
    {
      x: 10,
      y: 20,
    },
    {
      x: 20,
      y: 18,
    },
    {
      x: 30,
      y: 10,
    },
  ]

  const options: ChartOptions<"scatter"> = {
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        grid: {
          display: false,
        },
      },
    },
  }

  const data: ChartData<"scatter"> = {
    datasets: [
      {
        data: inputData,
        showLine: true,
        datalabels: { display: false },
        pointRadius: 0,
        borderColor: lighten(theme.palette.info.main, 0.75),
        borderWidth: 2,
      },
    ],
  }

  return <Scatter data={data} options={options} />
}

export default LineChart
