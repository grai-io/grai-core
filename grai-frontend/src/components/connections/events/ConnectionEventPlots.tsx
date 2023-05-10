import React from "react"
import { Box, Divider, lighten } from "@mui/material"
import { ResponsiveCalendar } from "@nivo/calendar"
import {
  Chart as ChartJS,
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
import theme from "theme"
import "chartjs-adapter-luxon"
import { Scatter } from "react-chartjs-2"

interface Event {
  id: string
  date: string
  status: string
}

type ConnectionEventPlotsProps = {
  events: Event[]
}

const ConnectionEventPlots: React.FC<ConnectionEventPlotsProps> = ({
  events,
}) => {
  const transformedEvents = events.map(event => ({
    status: event.status,
    date: DateTime.fromISO(event.date).toFormat("yyyy-MM-dd"),
  }))

  type Dates = {
    [key: string]: {
      [key: string]: number
    }
  }

  const startDates: Dates = {}

  const dates = transformedEvents.reduce<Dates>((result, event) => {
    const date = event.date
    const status = event.status

    if (result[date]) {
      result[date] = {
        ...result[date],
        [status]: result[date][status] + 1,
      }
    } else {
      result[date] = {
        [status]: 1,
      }
    }
    return result
  }, startDates)

  const data = Object.entries(dates).map(([date, values]) => ({
    day: date,
    value: values.error ? (values.success ? 2 : 1) : 3,
  }))

  ChartJS.register(
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend
  )

  const options: ChartOptions<"scatter"> = {
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

  const datasets: ChartData<
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

  return (
    <>
      <Box sx={{ height: 400 }}>
        <ResponsiveCalendar
          data={data}
          from={DateTime.now().minus({ years: 1 }).toJSDate()}
          to={DateTime.now().toJSDate()}
          emptyColor="#eeeeee"
          colors={[
            "blue",
            lighten(theme.palette.error.main, 0.25),
            "orange",
            lighten(theme.palette.success.main, 0.25),
          ]}
          margin={{ top: 20, left: 10 }}
          yearSpacing={40}
          monthBorderColor="#ffffff"
          dayBorderWidth={2}
          dayBorderColor="#ffffff"
          legends={[
            {
              anchor: "bottom-right",
              direction: "row",
              translateY: 36,
              itemCount: 4,
              itemWidth: 42,
              itemHeight: 36,
              itemsSpacing: 14,
              itemDirection: "right-to-left",
            },
          ]}
        />
      </Box>
      <Divider sx={{ mt: 5 }} />
      <Box sx={{ mt: 3 }}>
        <Scatter options={options} data={datasets} />
      </Box>
    </>
  )
}

export default ConnectionEventPlots
