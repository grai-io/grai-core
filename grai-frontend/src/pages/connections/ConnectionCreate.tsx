import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import PageHeader from "components/layout/PageHeader"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceConnectionCreate,
  GetWorkspaceConnectionCreateVariables,
} from "./__generated__/GetWorkspaceConnectionCreate"
import ConnectionCreateContent from "../../components/connections/create/ConnectionCreateContent"

export const GET_WORKSPACE = gql`
  query GetWorkspaceConnectionCreate(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
    }
    connectors(order: { priority: DESC, name: ASC }) {
      id
      priority
      name
      metadata
      icon
      category
      status
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

  return (
    <>
      <PageHeader title="Add Source" />
      <ConnectionCreateContent workspace={workspace} />
    </>
  )
}

export default ConnectionCreate
