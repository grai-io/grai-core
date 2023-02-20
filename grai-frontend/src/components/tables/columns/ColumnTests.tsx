import { Chip, Stack } from "@mui/material"
import React from "react"
import { Column } from "./TableColumnsTable"

interface Source {
  name: string
  display_name: string
}

type Requirement = {
  type: string
  text: string
  data_type?: string
  source: Source
}

type ColumnTestsProps = {
  column: Column
}

const ColumnTests: React.FC<ColumnTestsProps> = ({ column }) => {
  const requirements = column.requirements_edges.reduce<Requirement[]>(
    (res, edge) => {
      const edge_attributes = edge.metadata?.grai?.edge_attributes
      const node_attributes = edge.source.metadata.grai?.node_attributes

      if (!edge_attributes || !node_attributes) return res

      //Nullable
      if (
        edge_attributes.preserves_nullable &&
        node_attributes.is_nullable === false
      )
        return res.concat({
          type: "not-null",
          text: "Not Null",
          source: edge.source,
        })

      //Unique
      if (edge_attributes.preserves_unique && node_attributes.is_unique)
        return res.concat({
          type: "unique",
          text: "Unique",
          source: edge.source,
        })

      //Data type
      if (edge_attributes.preserves_data_type && node_attributes.data_type)
        return res.concat({
          type: "data-type",
          text: `Data Type: ${node_attributes.data_type}`,
          source: edge.source,
          data_type: node_attributes.data_type,
        })

      return res
    },
    []
  )

  if (requirements.length === 0) return null

  return (
    <Stack direction="row" spacing={1}>
      {requirements.map((requirement, index) => (
        <Chip key={index} label={requirement.text} />
      ))}
    </Stack>
  )
}

export default ColumnTests
