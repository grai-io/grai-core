import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Navigate } from "react-router-dom"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import { GetWorkspacesIndex } from "./__generated__/GetWorkspacesIndex"

export const GET_WORKSPACES = gql`
  query GetWorkspacesIndex {
    workspaces {
      id
      name
      organisation {
        id
        name
      }
    }
  }
`

const Index: React.FC = () => {
  const { loading, error, data } = useQuery<GetWorkspacesIndex>(GET_WORKSPACES)

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspaces = data?.workspaces ?? []

  const firstWorkspace = workspaces[0]

  if (firstWorkspace)
    return (
      <Navigate
        to={`/${firstWorkspace.organisation.name}/${firstWorkspace.name}`}
      />
    )

  return <Navigate to="/workspaces" />
}

export default Index
