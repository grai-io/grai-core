import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import CreateSource from "components/sources/CreateSource"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceSourceCreate,
  GetWorkspaceSourceCreateVariables,
} from "./__generated__/GetWorkspaceSourceCreate"

export const GET_WORKSPACE = gql`
  query GetWorkspaceSourceCreate(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
    }
  }
`

const SourceCreate: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceSourceCreate,
    GetWorkspaceSourceCreateVariables
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
    <PageLayout>
      <PageHeader title="Create Source" />
      <PageContent>
        <CreateSource workspaceId={workspace.id} />
      </PageContent>
    </PageLayout>
  )
}

export default SourceCreate
