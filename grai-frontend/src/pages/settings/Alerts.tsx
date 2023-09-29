import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import AlertsHeader from "components/settings/alerts/AlertsHeader"
import AlertsTable from "components/settings/alerts/AlertsTable"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import { GetAlerts, GetAlertsVariables } from "./__generated__/GetAlerts"
import SettingsContent from "components/settings/SettingsContent"

export const GET_ALERTS = gql`
  query GetAlerts($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      alerts {
        data {
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
    },
  )

  if (error) return <GraphError error={error} />

  const workspace = data?.workspace

  if (!loading && !workspace) return <NotFound />

  return (
    <SettingsLayout>
      <AlertsHeader workspaceId={workspace?.id} />
      <SettingsContent>
        <AlertsTable
          alerts={data?.workspace?.alerts.data ?? []}
          loading={loading}
          workspaceId={workspace?.id}
        />
      </SettingsContent>
    </SettingsLayout>
  )
}

export default Alerts
