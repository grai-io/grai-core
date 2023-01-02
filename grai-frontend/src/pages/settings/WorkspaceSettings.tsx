import { gql, useQuery } from "@apollo/client"
import Loading from "components/layout/Loading"
import SettingsLayout from "components/settings/SettingsLayout"
import WorkspaceForm from "components/settings/workspace/WorkspaceForm"
import GraphError from "components/utils/GraphError"
import NotFound from "pages/NotFound"
import React from "react"
import { useParams } from "react-router-dom"
import {
  GetWorkspace,
  GetWorkspaceVariables,
} from "./__generated__/GetWorkspace"

export const GET_WORKSPACE = gql`
  query GetWorkspace($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      name
    }
  }
`

const WorkspaceSettings: React.FC = () => {
  const { workspaceId } = useParams()

  const { loading, error, data } = useQuery<
    GetWorkspace,
    GetWorkspaceVariables
  >(GET_WORKSPACE, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading)
    return (
      <SettingsLayout>
        <Loading />
      </SettingsLayout>
    )

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return (
    <SettingsLayout>
      <WorkspaceForm workspace={workspace} />
    </SettingsLayout>
  )
}

export default WorkspaceSettings
