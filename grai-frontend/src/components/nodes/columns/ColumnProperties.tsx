import React from "react"
import { Chip, Stack } from "@mui/material"
import { EnrichedColumn } from "helpers/columns"

type ColumnPropertiesProps = {
  column: EnrichedColumn
}

const ColumnProperties: React.FC<ColumnPropertiesProps> = ({ column }) => (
  <Stack direction="row" spacing={1}>
    {column.properties.map(property => (
      <Chip
        key={property}
        label={property}
        size="small"
        variant="outlined"
        color="info"
      />
    ))}
  </Stack>
)

export default ColumnProperties
