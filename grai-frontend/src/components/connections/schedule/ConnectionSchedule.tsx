import React from "react"
import { Box, Stack } from "@mui/material"
import NodeDetailRow from "components/layout/NodeDetailRow"

export type CronValue = {
  minutes: string
  hours: string
  day_of_week: string
  day_of_month: string
  month_of_year: string
}

interface ConnectionScheduleItem {
  type: string | null
  cron?: CronValue
}

export interface Connection {
  id: string
  schedules: ConnectionScheduleItem | null
  is_active: boolean
  namespace: string
  name: string
  metadata: any
}

type ConnectionScheduleProps = {
  connection: Connection
}

const getScheduleString = (schedule: ConnectionScheduleItem | null): string => {
  switch (schedule?.type) {
    case "cron":
      return `Cron ${schedule?.cron?.minutes} ${schedule?.cron?.hours} ${schedule?.cron?.day_of_week} ${schedule?.cron?.day_of_month} ${schedule?.cron?.month_of_year}`
  }

  return "Manual"
}

const ConnectionSchedule: React.FC<ConnectionScheduleProps> = ({
  connection,
}) => (
  <NodeDetailRow label="Schedule">
    <Box sx={{ display: "flex" }}>
      <Stack spacing={1} sx={{ flexGrow: 1 }}>
        {getScheduleString(connection.schedules)}
      </Stack>
    </Box>
  </NodeDetailRow>
)

export default ConnectionSchedule
