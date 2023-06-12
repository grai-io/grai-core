import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import SettingsLayout from "components/settings/SettingsLayout"
import WorkspaceDanger from "components/settings/workspace/WorkspaceDanger"
import WorkspaceForm from "components/settings/workspace/WorkspaceForm"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceSettingsW,
  GetWorkspaceSettingsWVariables,
} from "./__generated__/GetWorkspaceSettingsW"

export const GET_WORKSPACE = gql`
  query GetWorkspaceSettingsW(
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
    GetWorkspaceSettingsW,
    GetWorkspaceSettingsWVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <SettingsLayout loading />

  const workspaceModel = data?.workspace

  if (!workspaceModel) return <NotFound />

  return (
    <SettingsLayout>
      <WorkspaceForm workspace={workspaceModel} />
      <WorkspaceDanger workspace={workspaceModel} />
    </SettingsLayout>
  )
}

export default WorkspaceSettings
