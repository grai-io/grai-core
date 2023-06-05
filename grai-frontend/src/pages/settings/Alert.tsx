import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import AlertConfiguration from "components/settings/alerts/AlertConfiguration"
import AlertHeader from "components/settings/alerts/AlertHeader"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import { GetAlert, GetAlertVariables } from "./__generated__/GetAlert"

export const GET_ALERT = gql`
  query GetAlert(
    $organisationName: String!
    $workspaceName: String!
    $id: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      alert(id: $id) {
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

const Alert: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { alertId } = useParams()

  const { loading, error, data } = useQuery<GetAlert, GetAlertVariables>(
    GET_ALERT,
    {
      variables: {
        organisationName,
        workspaceName,
        id: alertId ?? "",
      },
    }
  )

  if (error) return <GraphError error={error} />
  if (loading) return <SettingsLayout loading />

  const alert = data?.workspace.alert

  if (!alert) return <NotFound />

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <AlertHeader alert={alert} />
        <AlertConfiguration alert={alert} />
      </Box>
    </SettingsLayout>
  )
}

export default Alert
