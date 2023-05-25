import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import { useSearchParams } from "react-router-dom"
import theme from "theme"
import useWorkspace from "helpers/useWorkspace"
import EmptyGraph from "components/graph/EmptyGraph"
import GraphComponent, { Error } from "components/graph/GraphComponent"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdges,
  GetTablesAndEdgesVariables,
} from "./__generated__/GetTablesAndEdges"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdges(
    $organisationName: String!
    $workspaceName: String! # $filters: WorkspaceTableFilter # $offset: Int!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph {
        id
        name
        namespace
        data_source
        columns {
          id
          name
          destinations
        }
        destinations
      }
    }
  }
`

const Graph: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const [searchParams] = useSearchParams()

  // const filter = searchParams.get("filter") ?? null

  const { loading, error, data } = useQuery<
    GetTablesAndEdges,
    GetTablesAndEdgesVariables
  >(GET_TABLES_AND_EDGES, {
    variables: {
      organisationName,
      workspaceName,
      // filters: {
      //   filter,
      // },
    },
  })

  if (error) return <GraphError error={error} />

  const errorsQS = searchParams.get("errors")
  const errors: Error[] | null = errorsQS ? JSON.parse(errorsQS) : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  const tables = data?.workspace.graph ?? []
  const total = tables.length

  return (
    <PageLayout>
      <Box
        sx={{
          height: "100vh",
          width: "100%",
          backgroundColor: theme.palette.grey[100],
        }}
      >
        {total > 0 || loading ? (
          <GraphComponent
            tables={tables}
            errors={errors}
            limitGraph={limitGraph}
            loading={loading}
          />
        ) : (
          <EmptyGraph />
        )}
      </Box>
    </PageLayout>
  )
}

export default Graph
