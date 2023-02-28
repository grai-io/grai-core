import React, { ReactNode } from "react"
import { TableRow, TableCell, Typography } from "@mui/material"
import theme from "theme"

type NodeDetailRowProps = {
  label: string
  value?: string
  children?: ReactNode
  right?: boolean
}

const NodeDetailRow: React.FC<NodeDetailRowProps> = ({
  label,
  value,
  children,
  right,
}) => (
  <TableRow>
    <TableCell
      sx={{
        backgroundColor: theme.palette.grey[100],
        borderRightWidth: 1,
        borderRightStyle: "solid",
        borderRightColor: "divider",
        width: 300,
      }}
    >
      <Typography sx={{ fontWeight: "bold" }} variant="body2">
        {label}
      </Typography>
    </TableCell>
    <TableCell sx={{ textAlign: right ? "right" : undefined }}>
      {value && <Typography variant="body2">{value}</Typography>}
      {children}
    </TableCell>
  </TableRow>
)

export default NodeDetailRow
