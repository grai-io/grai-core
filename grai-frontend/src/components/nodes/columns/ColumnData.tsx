import React from "react"
import { Stack } from "@mui/material"
import LinearProgress from "components/progress/LinearProgress"

const ColumnData: React.FC = () => (
  <Stack direction="row" spacing={1}>
    <LinearProgress value={100} title="Filled" percentage />
    <LinearProgress value={50} title="Unique" percentage />
  </Stack>
)

export default ColumnData
