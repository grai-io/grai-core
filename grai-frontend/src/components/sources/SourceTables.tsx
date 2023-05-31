import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Typography } from "@mui/material"
import NotFound from "pages/NotFound"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetSourceTables,
  GetSourceTablesVariables,
} from "./__generated__/GetSourceTables"
import SourceTablesTable from "./SourceTablesTable"

export const GET_SOURCE_TABLES = gql`
  query GetSourceTables($workspaceId: ID!, $sourceId: ID!) {
    workspace(id: $workspaceId) {
      id
      source(id: $sourceId) {
        id
        nodes(filters: { node_type: "Table" }) {
          data {
            id
            namespace
            name
            display_name
          }
        }
      }
    }
  }
`

interface Source {
  id: string
}

type SourceTablesProps = {
  source: Source
  workspaceId: string
}

const SourceTables: React.FC<SourceTablesProps> = ({ source, workspaceId }) => {
  const { loading, error, data } = useQuery<
    GetSourceTables,
    GetSourceTablesVariables
  >(GET_SOURCE_TABLES, {
    variables: {
      workspaceId,
      sourceId: source.id,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspace = data?.workspace
  const sourceData = data?.workspace?.source

  if (!workspace || !sourceData) return <NotFound />

  if (sourceData.nodes.data.length === 0) {
    return (
      <Typography sx={{ textAlign: "center", p: 5 }}>
        No tables found!
      </Typography>
    )
  }

  return <SourceTablesTable tables={sourceData.nodes.data} />
}

export default SourceTables
