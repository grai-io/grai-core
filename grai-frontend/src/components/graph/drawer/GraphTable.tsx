import { TableChart } from "@mui/icons-material"
import { Box, Typography } from "@mui/material"
import React from "react"

interface Table {
  id: string
  name: string
  display_name: string
  x: number
  y: number
}

type GraphTableProps = {
  table: Table
  onClick?: () => void
}

const GraphTable: React.FC<GraphTableProps> = ({ table, onClick }) => (
  <Box
    sx={{
      display: "flex",
      m: 0.5,
      p: 1,
      fontSize: 12,
      borderWidth: 1,
      borderStyle: "solid",
      borderRadius: 1,
      boxShadow: "0px 8px 20px rgba(0, 0, 0, 0.06)",
      borderColor: "rgba(0, 0, 0, 0.08)",
      cursor: "pointer",
      alignItems: "center",
    }}
    onClick={onClick}
  >
    <TableChart sx={{ mr: 1 }} />
    <Typography variant="body2" sx={{ overflow: "hidden" }}>
      {table.display_name}
    </Typography>
  </Box>
  // <ListItem disablePadding>
  //   <ListItemButton onClick={onClick}>
  //     <ListItemIcon>
  //       <TableChart />
  //     </ListItemIcon>
  //     <ListItemText
  //       primary={`${table.display_name} (${table.x}, ${table.y})`}
  //     />
  //   </ListItemButton>
  // </ListItem>
)

export default GraphTable
