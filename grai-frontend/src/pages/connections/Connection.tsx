import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Stack } from "@mui/material"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useRunPolling from "helpers/runPolling"
import useWorkspace from "helpers/useWorkspace"
import ConnectionConfiguration from "components/connections/configuration/ConnectionConfiguration"
import ConnectionMenu from "components/connections/ConnectionMenu"
import ConnectionRun from "components/connections/ConnectionRun"
import ConnectionStatus from "components/connections/ConnectionStatus"
import ConnectionEvents from "components/connections/events/ConnectionEvents"
import ConnectionRunsTable from "components/connections/runs/ConnectionRunsTable"
import EditScheduleForm from "components/connections/schedule/EditScheduleForm"
import Loading from "components/layout/Loading"
import PageHeader from "components/layout/PageHeader"
import PageTabs from "components/layout/PageTabs"
import TabState from "components/tabs/TabState"
import GraphError from "components/utils/GraphError"
import {
  GetConnection,
  GetConnectionVariables,
} from "./__generated__/GetConnection"

export const GET_CONNECTION = gql`
  query GetConnection(
    $organisationName: String!
    $workspaceName: String!
    $connectionId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      connection(id: $connectionId) {
        id
        namespace
        name
        validated
        connector {
          id
          name
          events
          metadata
          icon
        }
        metadata
        schedules
        is_active
        created_at
        updated_at
        last_run {
          id
          status
          created_at
          started_at
          finished_at
          metadata
          user {
            id
            first_name
            last_name
          }
        }
        last_successful_run {
          id
          status
          created_at
          started_at
          finished_at
          metadata
          user {
            id
            first_name
            last_name
          }
        }
        runs(order: { created_at: DESC }, filters: { action: UPDATE }) {
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
          meta {
            total
          }
        }
      }
    }
  }
`

const Connection: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { connectionId } = useParams()

  const { loading, error, data, startPolling, stopPolling } = useQuery<
    GetConnection,
    GetConnectionVariables
  >(GET_CONNECTION, {
    variables: {
      organisationName,
      workspaceName,
      connectionId: connectionId ?? "",
    },
  })

  const status = data?.workspace.connection?.last_run?.status

  useRunPolling(status, startPolling, stopPolling)

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspace = data?.workspace
  const connection = data?.workspace?.connection

  if (!workspace || !connection) return <NotFound />

  const handleRun = () => startPolling(1000)

  const tabs = [
    {
      value: "runs",
      label: "Runs",
      component: <ConnectionRunsTable runs={connection.runs} />,
    },
    {
      value: "configuration",
      label: "Configuration",
      component: (
        <ConnectionConfiguration
          connection={connection}
          workspace={workspace}
        />
      ),
    },
    {
      value: "schedule",
      label: "Schedule",
      component: <EditScheduleForm connection={connection} />,
    },
    {
      value: "events",
      label: "Events",
      component: <ConnectionEvents connection={connection} />,
      noWrapper: true,
    },
    {
      value: "activity",
      label: "Activity",
      disabled: true,
    },
    {
      value: "alerts",
      label: "Alerts",
      disabled: true,
    },
  ]

  return (
    <TabState tabs={tabs}>
      <PageHeader
        title={connection.name}
        status={<ConnectionStatus connection={connection} />}
        buttons={
          <Stack direction="row" spacing={2}>
            <ConnectionRun
              connection={connection}
              workspaceId={workspace.id}
              onRun={handleRun}
            />
            <ConnectionMenu
              connection={connection}
              workspaceId={workspace.id}
            />
          </Stack>
        }
        tabs
      />
      <PageTabs />
    </TabState>
  )
}

export default Connection
