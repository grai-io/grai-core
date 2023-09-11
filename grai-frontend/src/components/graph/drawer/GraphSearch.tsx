import React, { useCallback, useEffect, useMemo, useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Close } from "@mui/icons-material"
import { Box, InputAdornment, List, TextField, Tooltip } from "@mui/material"
import { Viewport, useReactFlow } from "reactflow"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  SearchGraphTables,
  SearchGraphTablesVariables,
} from "./__generated__/SearchGraphTables"
import GraphTable from "./GraphTable"

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
        data_source
        x
        y
      }
    }
  }
`

type Position = {
  x: number
  y: number
}

type GraphSearchProps = {
  search: string
  onSearch: (search: string | null) => void
  onMove?: (viewport: Viewport) => void
}

const GraphSearch: React.FC<GraphSearchProps> = ({
  search,
  onSearch,
  onMove,
}) => {
  const { organisationName, workspaceName } = useWorkspace()
  const reactFlowInstance = useReactFlow()
  const [center, setCenter] = useState<Position>()
  const [selected, setSelected] = useState(0)

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
    if (!center) return

    reactFlowInstance.setCenter(center.x, center.y, {
      zoom: 0.75,
    })

    const timer = setTimeout(() => {
      onMove && onMove(reactFlowInstance.getViewport())
    }, 1)

    return () => clearTimeout(timer)
  }, [center, onMove, reactFlowInstance])

  const tables = useMemo(() => data?.workspace.graph_tables ?? [], [data])

  const setTableCenter = useCallback(
    (table: { x: number; y: number }) =>
      setCenter({ x: table.x + 200, y: table.y }),
    [],
  )

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.code === "ArrowDown") {
        setSelected(Math.min(selected + 1, tables.length - 1))
      }
      if (event.code === "ArrowUp") {
        setSelected(Math.max(selected - 1, 0))
      }
      if (event.code === "Enter") {
        setTableCenter(tables[selected])
      }
      if (event.code === "Escape") {
        onSearch(null)
      }
    }

    document.addEventListener("keydown", handleKeyDown)

    // Don't forget to clean up
    return function cleanup() {
      document.removeEventListener("keydown", handleKeyDown)
    }
  }, [onSearch, selected, tables, setTableCenter])

  return (
    <Box>
      <Box sx={{ p: 1 }}>
        <TextField
          fullWidth
          size="small"
          placeholder="Search"
          value={search}
          onChange={event => onSearch(event.target.value)}
          InputProps={{
            endAdornment: search !== "" && (
              <InputAdornment position="end">
                <Tooltip title="Clear">
                  <Close
                    onClick={() => onSearch(null)}
                    sx={{ color: "divider", cursor: "pointer" }}
                  />
                </Tooltip>
              </InputAdornment>
            ),
          }}
          inputProps={{
            "data-testid": "search-input",
          }}
        />
      </Box>
      {error && <GraphError error={error} />}
      {loading && <Loading />}
      <List
        disablePadding
        sx={{
          maxHeight: "calc(100vh - 200px)",
          overflowY: "auto",
          overflowX: "hidden",
          border: 0,
          borderTop: 1,
          borderColor: theme => theme.palette.grey[200],
          borderStyle: "solid",
        }}
      >
        {tables.map((table, index) => (
          <GraphTable
            key={table.id}
            table={table}
            onClick={() => setTableCenter(table)}
            onHover={() => setSelected(index)}
            selected={selected === index}
          />
        ))}
      </List>
    </Box>
  )
}

export default GraphSearch
