import React from "react"
import {
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material"
import DataSourceIcon from "../DataSourceIcon"

interface Table {
  id: string
  name: string
  display_name: string
  data_source: string | null
  x: number
  y: number
}

type GraphTableProps = {
  table: Table
  onClick?: () => void
  selected: boolean
  onHover?: () => void
}

const GraphTable: React.FC<GraphTableProps> = ({
  table,
  onClick,
  selected,
  onHover,
}) => (
  <ListItem disablePadding divider selected={selected} onMouseEnter={onHover}>
    <ListItemButton onClick={onClick} sx={{ pl: 1 }}>
      <ListItemIcon>
        {table.data_source && (
          <DataSourceIcon
            dataSource={table.data_source}
            size="small"
            noMargin
            noBorder
          />
        )}
      </ListItemIcon>
      <ListItemText
        primary={
          <Typography variant="body2" sx={{ overflow: "hidden" }}>
            {table.display_name}
          </Typography>
        }
      />
    </ListItemButton>
  </ListItem>
)

export default GraphTable
