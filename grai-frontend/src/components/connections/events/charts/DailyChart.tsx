import React from "react"
import { lighten } from "@mui/material"
import {
  Chart,
  registerables,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  ChartOptions,
  ChartData,
} from "chart.js"
import { MatrixController, MatrixElement } from "chartjs-chart-matrix"
import { DateTime, Interval } from "luxon"
import theme from "theme"
import notEmpty from "helpers/notEmpty"
import { Matrix } from "components/charts/Matrix"
import "chartjs-adapter-luxon"

type ChartDataPoint = {
  x: string
  y: number
  d: string
  v: number
}

interface Event {
  day: string
  value: number
}

type DailyChartProps = {
  events: Event[]
  responsive?: boolean
}

const DailyChart: React.FC<DailyChartProps> = ({ events, responsive }) => {
  Chart.register(
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend,
    ...registerables,
    MatrixController,
    MatrixElement
  )

  const scales = {
    y: {
      type: "linear" as const,
      offset: true,
      grid: {
        display: false,
      },
      border: {
        display: false,
      },
      ticks: {
        display: false,
      },
    },
    x: {
      type: "time" as const,
      position: "top" as const,
      offset: true,
      time: {
        unit: "month" as const,
        round: "week" as const,
        isoWeekday: 1,
        displayFormats: {
          month: "MMM",
        },
      },
      ticks: {
        maxRotation: 0,
        padding: 10,
        labelOffset: 50,
        font: {
          size: 11,
        },
      },
      grid: {
        display: false,
      },
      border: {
        display: false,
      },
    },
  }

  const options: ChartOptions<"matrix"> = {
    responsive,
    aspectRatio: 6,
    plugins: {
      legend: { display: false },
      tooltip: {
        displayColors: false,
        callbacks: {
          title: () => "",
          label: context => [
            "d: " + (context.raw as ChartDataPoint).d,
            "v: " + (context.raw as ChartDataPoint).v.toFixed(2),
          ],
        },
        filter: context => (context.raw as ChartDataPoint).v !== 0,
      },
    },
    scales,
    layout: {
      padding: {
        top: 10,
      },
    },
  }

  const start = DateTime.now().startOf("year")
  const end = DateTime.now().endOf("year")

  const dates: DateTime[] = Interval.fromDateTimes(start, end)
    .splitBy({ days: 1 })
    .map(d => d.start)
    .filter(notEmpty)

  const data2: ChartDataPoint[] = dates.map(date => ({
    x: date.toFormat("yyyy-MM-dd"),
    y: date.weekday,
    d: date.toFormat("yyyy-MM-dd"),
    v:
      events.find(event => event.day === date.toFormat("yyyy-MM-dd"))?.value ||
      0,
  }))

  const data: ChartData<"matrix", ChartDataPoint[]> = {
    datasets: [
      {
        label: "My Matrix",
        data: data2,
        backgroundColor(c) {
          const value = (c.raw as ChartDataPoint).v

          switch (value) {
            case 1:
              return lighten(theme.palette.error.main, 0.25)
            case 2:
              return "orange"
            case 3:
              return lighten(theme.palette.success.main, 0.25)

            default:
              return "#eeeeee"
          }
        },
        borderColor: "white",
        borderWidth: 1,
        width(c) {
          const a = c.chart.chartArea || {}
          return (a.right - a.left) / 53 - 1
        },
        height(c) {
          const a = c.chart.chartArea || {}
          return (a.bottom - a.top) / 7 - 1
        },
      },
    ],
  }

  return <Matrix data={data} options={options} />
}

export default DailyChart
