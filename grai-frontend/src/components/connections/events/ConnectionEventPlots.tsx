import React from "react"
import { Box } from "@mui/material"
import { ResponsiveCalendar } from "@nivo/calendar"
import { DateTime } from "luxon"
import theme from "theme"

interface Event {
  id: string
  metadata: any
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
    created_at: DateTime.fromFormat(
      event.metadata.grai_source_dbt_cloud.created_at,
      "yyyy-MM-dd HH:mm:ss.uZZ"
    ).toFormat("yyyy-MM-dd"),
  }))

  type Dates = {
    [key: string]: {
      [key: string]: number
    }
  }

  const startDates: Dates = {}

  const dates = transformedEvents.reduce<Dates>((result, event) => {
    const date = event.created_at
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
    <Box sx={{ height: 400 }}>
      <ResponsiveCalendar
        data={data}
        from={DateTime.now().minus({ years: 1 }).toJSDate()}
        to={DateTime.now().toJSDate()}
        emptyColor="#eeeeee"
        colors={[
          "blue",
          theme.palette.error.main,
          "orange",
          theme.palette.success.main,
        ]}
        margin={{ top: 40, right: 40, bottom: 40, left: 40 }}
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
  )
}

export default ConnectionEventPlots
