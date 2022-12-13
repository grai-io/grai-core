import { TableRow, TableCell, Typography } from "@mui/material"
import React from "react"
import theme from "../../theme"

type NodeDetailRowProps = {
  label: string
  value: string
}

const NodeDetailRow: React.FC<NodeDetailRowProps> = ({ label, value }) => (
  <TableRow>
    <TableCell
      sx={{
        backgroundColor: theme.palette.grey[100],
      }}
    >
      <Typography sx={{ fontWeight: "bold" }} variant="body2">
        {label}
      </Typography>
    </TableCell>
    <TableCell>
      <Typography variant="body2">{value}</Typography>
    </TableCell>
  </TableRow>
)

export default NodeDetailRow
