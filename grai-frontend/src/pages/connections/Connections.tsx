import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Add } from "@mui/icons-material"
import { Button } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import ConnectionsTable from "components/connections/ConnectionsTable"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import TableHeader from "components/table/TableHeader"
import GraphError from "components/utils/GraphError"
import {
  GetConnections,
  GetConnectionsVariables,
} from "./__generated__/GetConnections"

//Extra parameters required to make cache update work on connection run
export const GET_CONNECTIONS = gql`
  query GetConnections($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      connections {
        data {
          id
          namespace
          name
          is_active
          connector {
            id
            name
            events
          }
          runs(order: { created_at: DESC }) {
            data {
              id
              status
              created_at
              started_at
              finished_at
              user {
                id
                first_name
                last_name
              }
              metadata
            }
          }
          last_run {
            id
            status
            created_at
            started_at
            finished_at
            user {
              id
              first_name
              last_name
            }
            metadata
          }
          last_successful_run {
            id
            status
            created_at
            started_at
            finished_at
            user {
              id
              first_name
              last_name
            }
            metadata
          }
        }
        meta {
          total
        }
      }
    }
  }
`

const Connections: React.FC = () => {
  const [search, setSearch] = useState<string>()
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data, refetch } = useQuery<
    GetConnections,
    GetConnectionsVariables
  >(GET_CONNECTIONS, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  const handleRefresh = () => refetch()

  if (error) return <GraphError error={error} />

  const connections = data?.workspace.connections.data ?? []

  const filteredConnections = search
    ? connections.filter(connection =>
        connection.name.toLowerCase().includes(search.toLowerCase())
      )
    : connections

  return (
    <PageLayout>
      <PageHeader
        title="Connections"
        buttons={
          <Button
            variant="contained"
            startIcon={<Add />}
            component={Link}
            to="create"
            sx={{
              backgroundColor: "#FC6016",
              boxShadow: "0px 4px 6px rgba(252, 96, 22, 0.2)",
              borderRadius: "8px",
              height: "40px",
            }}
          >
            Add Connection
          </Button>
        }
      />
      <PageContent>
        <TableHeader
          search={search}
          onSearch={setSearch}
          onRefresh={handleRefresh}
        />
        <ConnectionsTable
          connections={filteredConnections}
          workspaceId={data?.workspace.id}
          loading={loading}
          total={data?.workspace.connections.meta.total ?? 0}
        />
      </PageContent>
    </PageLayout>
  )
}

export default Connections
