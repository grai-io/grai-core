import { TableRow, TableCell, Typography } from "@mui/material"
import React, { ReactNode } from "react"
import theme from "../../theme"

type NodeDetailRowProps = {
  label: string
  value?: string
  children?: ReactNode
}

const NodeDetailRow: React.FC<NodeDetailRowProps> = ({
  label,
  value,
  children,
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
    <TableCell>
      {value && <Typography variant="body2">{value}</Typography>}
      {children}
    </TableCell>
  </TableRow>
)

export default NodeDetailRow
