import { Check, Close } from "@mui/icons-material"
import { Chip, Stack } from "@mui/material"
import { EnrichedColumn } from "helpers/columns"
import React from "react"

type ColumnTestsProps = {
  column: EnrichedColumn
}

const ColumnTests: React.FC<ColumnTestsProps> = ({ column }) => (
  <Stack direction="row" spacing={1}>
    {column.tests.map((test, index) => (
      <Chip
        key={index}
        label={test.text}
        color={test.passed ? "success" : "error"}
        icon={test.passed ? <Check /> : <Close />}
        size="small"
        variant="outlined"
      />
    ))}
  </Stack>
)

export default ColumnTests
