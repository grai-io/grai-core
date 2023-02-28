import React from "react"
import { Check, Close } from "@mui/icons-material"
import { Chip, Stack } from "@mui/material"
import { Edge } from "helpers/columns"

const getType = (edge: Edge) => {
  if (!edge.preserved) return { color: "default" as const }

  if (edge.passed) return { icon: <Check />, color: "success" as const }

  return { icon: <Close />, color: "error" as const }
}

type ColumnRequirementsProps = { edges: Edge[] }

const ColumnRequirements: React.FC<ColumnRequirementsProps> = ({ edges }) => (
  <Stack direction="row" spacing={1}>
    {edges.map(edge => (
      <Chip
        key={edge.text}
        label={edge.text}
        size="small"
        icon={getType(edge).icon}
        color={getType(edge).color}
        variant="outlined"
      />
    ))}
  </Stack>
)

export default ColumnRequirements
