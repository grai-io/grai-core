import { gql, useQuery } from "@apollo/client"
import Loading from "components/layout/Loading"
import SettingsLayout from "components/settings/SettingsLayout"
import WorkspaceForm from "components/settings/workspace/WorkspaceForm"
import GraphError from "components/utils/GraphError"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"
import React from "react"
import {
  GetWorkspaceSettings,
  GetWorkspaceSettingsVariables,
} from "./__generated__/GetWorkspaceSettings"

export const GET_WORKSPACE = gql`
  query GetWorkspaceSettings(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
    }
  }
`

const WorkspaceSettings: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceSettings,
    GetWorkspaceSettingsVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading)
    return (
      <SettingsLayout>
        <Loading />
      </SettingsLayout>
    )

  const workspaceModel = data?.workspace

  if (!workspaceModel) return <NotFound />

  return (
    <SettingsLayout>
      <WorkspaceForm workspace={workspaceModel} />
    </SettingsLayout>
  )
}

export default WorkspaceSettings
