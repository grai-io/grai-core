import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"
import AlertsHeader from "components/settings/alerts/AlertsHeader"
import AlertsTable from "components/settings/alerts/AlertsTable"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import { GetAlerts, GetAlertsVariables } from "./__generated__/GetAlerts"

export const GET_ALERTS = gql`
  query GetAlerts($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      alerts {
        id
        name
        channel
        channel_metadata
        triggers
        is_active
        created_at
      }
    }
  }
`

const Alerts: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<GetAlerts, GetAlertsVariables>(
    GET_ALERTS,
    {
      variables: {
        organisationName,
        workspaceName,
      },
    }
  )

  if (error) return <GraphError error={error} />

  const workspace = data?.workspace

  if (!loading && !workspace) return <NotFound />

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <AlertsHeader workspaceId={workspace?.id} />
        <AlertsTable
          alerts={data?.workspace?.alerts ?? []}
          loading={loading}
          workspaceId={workspace?.id}
        />
      </Box>
    </SettingsLayout>
  )
}

export default Alerts
