import { ListAlt, ViewColumn } from "@mui/icons-material"
import { ListItemButton, ListItemIcon, ListItemText } from "@mui/material"
import React from "react"
import { Link } from "react-router-dom"
import type { BaseHit } from "instantsearch.js"
import useWorkspace from "helpers/useWorkspace"

export interface SearchHit extends BaseHit {
  id: string
  name: string
  display_name: string
  search_type: string
  table_id?: string | null
}

type SearchHitProps = {
  hit: SearchHit
}

const types = [
  {
    name: "Table",
    icon: <ListAlt />,
    route: (hit: SearchHit) => `/tables/${hit.id}`,
  },
  {
    name: "Column",
    icon: <ViewColumn />,
    route: (hit: SearchHit) => `/tables/${hit.table_id}`,
  },
]

const SearchHitRow: React.FC<SearchHitProps> = ({ hit }) => {
  const { routePrefix } = useWorkspace()

  const type = types.find(type => type.name === hit.search_type)

  const route = type?.route(hit)
  const to = route ? `${routePrefix}${route}` : ""

  return (
    <ListItemButton key={hit.id} component={Link} to={to}>
      <ListItemIcon>{type?.icon}</ListItemIcon>
      <ListItemText primary={hit.display_name} secondary={hit.name} />
    </ListItemButton>
  )
}

export default SearchHitRow
