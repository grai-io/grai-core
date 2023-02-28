import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Navigate, useLocation, useParams } from "react-router-dom"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspace,
  GetWorkspaceVariables,
} from "./__generated__/GetWorkspace"

export const GET_WORKSPACE = gql`
  query GetWorkspace($workspaceId: ID!) {
    workspace(id: $workspaceId) {
      id
      name
      organisation {
        id
        name
      }
    }
  }
`

const WorkspaceRedirect: React.FC = () => {
  const { workspaceId } = useParams()
  const location = useLocation()

  const { loading, error, data } = useQuery<
    GetWorkspace,
    GetWorkspaceVariables
  >(GET_WORKSPACE, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  return (
    <Navigate
      to={{
        pathname: location.pathname.replace(
          `/workspaces/${workspaceId}`,
          `/${data?.workspace.organisation.name}/${data?.workspace.name}`
        ),
        search: location.search,
      }}
      replace
    />
  )
}

export default WorkspaceRedirect
