import { gql, useQuery } from "@apollo/client"
import React from "react"
import { Navigate } from "react-router-dom"
import Loading from "components/layout/Loading"

const GET_WORKSPACES = gql`
  query GetWorkspacesIndex {
    workspaces {
      id
      name
    }
  }
`

const Index: React.FC = () => {
  const { loading, error, data } = useQuery(GET_WORKSPACES)

  if (error) return <p>Error : {error.message}</p>
  if (loading) return <Loading />

  const workspaces = data.workspaces

  return <Navigate to={`/workspaces/${workspaces[0]?.id}`} />
}

export default Index
