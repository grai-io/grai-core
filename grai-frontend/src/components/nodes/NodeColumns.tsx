import { OpenInFull, SearchRounded } from "@mui/icons-material"
import { Box, Button, InputAdornment, TextField } from "@mui/material"
import React, { ChangeEvent, useState } from "react"
import NodeColumnsTable from "./NodeColumnsTable"

interface Node {
  id: string
  name: string
  metadata: {
    table_name: string
  }
  sourceEdges: {
    id: string
    destination: {
      id: string
      name: string
      displayName: string
      metadata: {
        node_type: string
        table_name: string
      }
    }
  }[]
}

type NodeColumnsProps = {
  node: Node
}

const NodeColumns: React.FC<NodeColumnsProps> = ({ node }) => {
  const [search, setSearch] = useState<string | null>(null)

  const handleSearch = (event: ChangeEvent<HTMLInputElement>) =>
    setSearch(event.target.value)

  const columns =
    node.sourceEdges
      .filter(
        edge =>
          edge.destination.metadata.table_name === node.metadata.table_name ||
          `public.${edge.destination.metadata.table_name}` === node.name
      )
      .map(edge => ({
        id: edge.destination.id,
        name: edge.destination.displayName ?? edge.destination.name,
      })) ?? []

  return (
    <>
      <Box sx={{ display: "flex", mt: 3 }}>
        <Box sx={{ flexGrow: 1 }}>
          <TextField
            placeholder="Search Columns"
            variant="outlined"
            size="small"
            value={search ?? ""}
            onChange={handleSearch}
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <SearchRounded />
                </InputAdornment>
              ),
            }}
            sx={{ minWidth: 350 }}
          />
        </Box>
        <Box>
          <Button variant="outlined" startIcon={<OpenInFull />}>
            Expand all rows
          </Button>
        </Box>
      </Box>
      <NodeColumnsTable search={search} columns={columns} />
    </>
  )
}

export default NodeColumns
