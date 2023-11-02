import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Alert, Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import GraphComponent from "components/graph/GraphComponent"
import useCombinedFilters from "components/graph/useCombinedFilters"
import useFilters from "components/graph/useFilters"
import useInlineFilters from "components/graph/useInlineFilters"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdgesSourceLineage,
  GetTablesAndEdgesSourceLineageVariables,
} from "./__generated__/GetTablesAndEdgesSourceLineage"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdgesSourceLineage(
    $organisationName: String!
    $workspaceName: String!
    $sourceId: ID!
    $n: Int!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph(filters: { source_id: $sourceId, n: $n }) {
        id
        name
        display_name
        namespace
        x
        y
        data_source
        columns {
          id
          name
          display_name
          destinations {
            edge_id
            column_id
          }
        }
        destinations {
          edge_id
          table_id
        }
        table_destinations
        table_sources
      }
    }
  }
`

interface Source {
  id: string
}

type SourceLineageProps = {
  source: Source
}

const SourceLineage: React.FC<SourceLineageProps> = ({ source }) => {
  const [value, setValue] = useState(0)
  const { organisationName, workspaceName } = useWorkspace()
  const { combinedFilters } = useCombinedFilters(
    `sources-${source.id}-graph-filters`,
    `sources-${source.id}-graph-inline-filters`,
  )

  const { loading, error, data } = useQuery<
    GetTablesAndEdgesSourceLineage,
    GetTablesAndEdgesSourceLineageVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      organisationName,
      workspaceName,
      sourceId: source.id,
      n: value,
    },
  })

  if (error) return <GraphError error={error} />

  const tables = data?.workspace.graph

  if (!loading && (!tables || tables.length === 0))
    return <Alert>No tables found</Alert>

  return (
    <Box
      sx={{
        height: "calc(100vh - 144px)",
      }}
      data-testid="source-lineage"
    >
      <GraphComponent
        tables={tables ?? []}
        loading={loading}
        fitView
        controlOptions={{
          steps: {
            value,
            setValue,
          },
        }}
        combinedFilters={combinedFilters}
      />
    </Box>
  )
}

export default SourceLineage
