import { Edit } from "@mui/icons-material"
import { Box, Button, Stack } from "@mui/material"
import NodeDetailRow from "components/nodes/NodeDetailRow"
import React, { useState } from "react"
import EditScheduleDialog from "./schedule/EditScheduleDialog"

interface ConnectionScheduleItem {
  type: string | null
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

const ConnectionSchedule: React.FC<ConnectionScheduleProps> = ({
  connection,
}) => {
  const [open, setOpen] = useState(false)

  const handleClick = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <NodeDetailRow label="Schedule">
      <Box sx={{ display: "flex" }}>
        <Stack spacing={1} sx={{ flexGrow: 1 }}>
          {connection.schedules ? "Schedule" : "Manual"}
        </Stack>
        <Box>
          <Button
            variant="outlined"
            startIcon={<Edit />}
            size="small"
            onClick={handleClick}
          >
            Edit
          </Button>
        </Box>
      </Box>
      <EditScheduleDialog
        open={open}
        onClose={handleClose}
        connection={connection}
      />
    </NodeDetailRow>
  )
}

export default ConnectionSchedule
