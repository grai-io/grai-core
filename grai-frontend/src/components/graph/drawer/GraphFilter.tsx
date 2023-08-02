import React, { useState } from "react"
import { Edit } from "@mui/icons-material"
import {
  Button,
  Checkbox,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Tooltip,
  Typography,
} from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

interface Filter {
  id: string
  name: string | null
}

type GraphFilterProps = {
  filter: Filter
  filters: string[]
  setFilters: (filters: string[]) => void
}

const GraphFilter: React.FC<GraphFilterProps> = ({
  filter,
  filters,
  setFilters,
}) => {
  const [hover, setHover] = useState(false)
  const { routePrefix } = useWorkspace()

  const checked = filters.includes(filter.id)

  const handleToggle = () =>
    setFilters(
      checked ? filters.filter(f => f !== filter.id) : [...filters, filter.id],
    )

  const handleOnly = () => setFilters([filter.id])

  return (
    <ListItem
      divider
      secondaryAction={
        hover && (
          <Stack direction="row" spacing={1}>
            <Tooltip title="Enable only this filter">
              <Button size="small" sx={{ minWidth: 0 }} onClick={handleOnly}>
                <Typography variant="caption">ONLY</Typography>
              </Button>
            </Tooltip>
            <Tooltip title="Edit filter">
              <IconButton
                component={Link}
                to={`${routePrefix}/filters/${filter.id}`}
              >
                <Edit fontSize="small" />
              </IconButton>
            </Tooltip>
          </Stack>
        )
      }
      disablePadding
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
    >
      <ListItemButton onClick={handleToggle} sx={{ px: 1 }}>
        <ListItemIcon sx={{ minWidth: 32 }}>
          <Checkbox
            edge="end"
            sx={{ p: 0 }}
            checked={checked}
            onChange={handleToggle}
          />
        </ListItemIcon>
        <ListItemText
          primary={
            <Typography variant="body2" sx={{ overflow: "hidden" }}>
              {filter.name}
            </Typography>
          }
        />
      </ListItemButton>
    </ListItem>
  )
}

export default GraphFilter
