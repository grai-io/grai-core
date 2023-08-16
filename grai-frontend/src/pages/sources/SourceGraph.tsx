import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import Graph from "components/sources/Graph"
import GraphError from "components/utils/GraphError"
import {
  GetSourceGraph,
  GetSourceGraphVariables,
} from "./__generated__/GetSourceGraph"

export const GET_WORKSPACE = gql`
  query GetSourceGraph($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
      source_graph {
        id
        name
        icon
        targets
      }
    }
  }
`

const SourceGraph: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetSourceGraph,
    GetSourceGraphVariables
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
      <PageHeader title={workspace.name} />
      <Graph sourceGraph={workspace.source_graph} />
    </PageLayout>
  )
}

export default SourceGraph
