import { Chip } from "@mui/material"
import NodeDetailRow from "components/nodes/NodeDetailRow"
import React from "react"

interface Run {
  id: string
  status: string
}

type ConnectionRunDetailProps = {
  label: string
  run: Run | null
}

const ConnectionRunDetail: React.FC<ConnectionRunDetailProps> = ({
  label,
  run,
}) => (
  <NodeDetailRow label={label}>
    {run && (
      <>
        <Chip label={run?.status} />
      </>
    )}
  </NodeDetailRow>
)

export default ConnectionRunDetail
