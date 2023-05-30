import React from "react"
import { Box, Divider, lighten } from "@mui/material"
import { ResponsiveCalendar } from "@nivo/calendar"
import { DateTime } from "luxon"
import theme from "theme"
import HourlyChart from "./charts/HourlyChart"

interface Event {
  id: string
  date: string
  status: string
}

type ConnectionEventPlotsProps = {
  events: Event[]
  responsive?: boolean
}

const ConnectionEventPlots: React.FC<ConnectionEventPlotsProps> = ({
  events,
  responsive,
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
        <HourlyChart events={events} responsive={responsive} />
      </Box>
    </>
  )
}

export default ConnectionEventPlots
