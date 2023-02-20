import { Chip, Stack } from "@mui/material"
import React from "react"
import { Column } from "./TableColumnsTable"

type ColumnPropertiesProps = {
  column: Column
}

const ColumnProperties: React.FC<ColumnPropertiesProps> = ({ column }) => {
  const attributes = column.metadata?.grai?.node_attributes

  if (!attributes) return null

  const constraints: string[] = []

  if (attributes.is_primary_key) constraints.push("Primary Key")
  if (attributes.is_unique) constraints.push("Unique")
  if (attributes.is_nullable === false) constraints.push("Not Null")

  return (
    <Stack direction="row" spacing={1}>
      {constraints.map(constraint => (
        <Chip key={constraint} label={constraint} />
      ))}
    </Stack>
  )
}

export default ColumnProperties
