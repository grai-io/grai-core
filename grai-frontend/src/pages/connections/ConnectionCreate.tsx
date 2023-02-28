import React from "react"
import { gql, useQuery } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"
import CreateConnectionWizard from "components/connections/create/CreateConnectionWizard"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceConnectionCreate,
  GetWorkspaceConnectionCreateVariables,
} from "./__generated__/GetWorkspaceConnectionCreate"

export const GET_WORKSPACE = gql`
  query GetWorkspaceConnectionCreate(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
    }
  }
`

const ConnectionCreate: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceConnectionCreate,
    GetWorkspaceConnectionCreateVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return <CreateConnectionWizard workspaceId={workspace.id} />
}

export default ConnectionCreate
