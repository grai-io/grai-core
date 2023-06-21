import { gql, useQuery } from "@apollo/client"
import { Box, List, TextField } from "@mui/material"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import useWorkspace from "helpers/useWorkspace"
import React, { useEffect, useState } from "react"
import {
  SearchGraphTables,
  SearchGraphTablesVariables,
} from "./__generated__/SearchGraphTables"
import GraphTable from "./GraphTable"
import { Viewport, useReactFlow, useStore } from "reactflow"

export const SEARCH_TABLES = gql`
  query SearchGraphTables(
    $organisationName: String!
    $workspaceName: String!
    $search: String
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph_tables(search: $search) {
        id
        name
        display_name
        x
        y
      }
    }
  }
`

type GraphSearchProps = {
  onMove?: (viewport: Viewport) => void
}

const GraphSearch: React.FC<GraphSearchProps> = ({ onMove }) => {
  const [search, setSearch] = useState<string>("")
  const { organisationName, workspaceName } = useWorkspace()
  const reactFlowInstance = useReactFlow()
  const [center, setCenter] = useState({ x: 0, y: 0 })

  const { loading, error, data } = useQuery<
    SearchGraphTables,
    SearchGraphTablesVariables
  >(SEARCH_TABLES, {
    variables: {
      organisationName,
      workspaceName,
      search,
    },
    context: {
      debounceKey: "edges",
      debounceTimeout: 1000,
    },
  })

  useEffect(() => {
    reactFlowInstance.setCenter(center.x, center.y, {
      zoom: 0.75,
    })

    const timer = setTimeout(() => {
      onMove && onMove(reactFlowInstance.getViewport())
    }, 1)

    return () => clearTimeout(timer)
  }, [center])

  if (error) return <GraphError error={error} />

  const tables = data?.workspace.graph_tables ?? []

  return (
    <>
      <Box sx={{ p: 1 }}>
        <TextField
          fullWidth
          size="small"
          placeholder="Search"
          value={search}
          onChange={event => setSearch(event.target.value)}
        />
      </Box>
      {loading && <Loading />}
      <List
        disablePadding
        sx={{
          maxHeight: "calc(100vh - 200px)",
          overflowY: "auto",
          overflowX: "hidden",
        }}
      >
        {tables.map(table => (
          <GraphTable
            key={table.id}
            table={table}
            onClick={() => setCenter({ x: table.x + 200, y: table.y })}
          />
        ))}
      </List>
    </>
  )
}

export default GraphSearch
