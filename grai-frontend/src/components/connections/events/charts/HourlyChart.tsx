import React from "react"
import {
  Chart,
  LinearScale,
  TimeScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  ChartData,
  ChartOptions,
} from "chart.js"
import { DateTime } from "luxon"
import { Scatter } from "react-chartjs-2"
import theme from "theme"
import "chartjs-adapter-luxon"

interface Event {
  status: string
  date: string
}

type HourlyChartProps = {
  events: Event[]
  responsive?: boolean
}

const HourlyChart: React.FC<HourlyChartProps> = ({ events, responsive }) => {
  Chart.register(
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend
  )

  const options: ChartOptions<"scatter"> = {
    responsive,
    scales: {
      x: {
        type: "time" as const,
        time: {
          unit: "hour" as const,
          tooltipFormat: "H:MM",
          displayFormats: {
            hour: "H:mm",
          },
        },
        grid: {
          display: false,
        },
        border: {
          display: false,
        },
        ticks: {
          stepSize: 2,
          padding: 30,
        },
        position: "top",
      },
      y: {
        type: "time" as const,
        time: {
          unit: "day" as const,
          tooltipFormat: "DDD",
        },
        grid: {
          display: false,
        },
        border: {
          display: false,
        },
        ticks: {
          padding: 30,
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  }

  const data: ChartData<
    "scatter",
    {
      x: string
      y: Date
    }[],
    unknown
  > = {
    datasets: [
      {
        label: "A dataset",
        data: events.map(event => ({
          x: DateTime.fromISO(event.date).toFormat("HH:mm:ss"),
          y: DateTime.fromISO(event.date).startOf("day").toJSDate(),
        })),
        pointBackgroundColor: events.map(event =>
          event.status === "success"
            ? theme.palette.success.main
            : theme.palette.error.main
        ),
        borderWidth: 0,
        pointRadius: 5,
      },
    ],
  }

  return <Scatter options={options} data={data} />
}

export default HourlyChart
