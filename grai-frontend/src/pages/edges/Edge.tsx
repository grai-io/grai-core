import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import EdgeLineage from "components/edges/EdgeLineage"
import EdgeProfile from "components/edges/EdgeProfile"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import PageTabs from "components/layout/PageTabs"
import TabState from "components/tabs/TabState"
import GraphError from "components/utils/GraphError"

export const GET_EDGE = gql`
  query GetEdge(
    $organisationName: String!
    $workspaceName: String!
    $edgeId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      edge(id: $edgeId) {
        id
        namespace
        name
        display_name
        is_active
        metadata
        source {
          id
          namespace
          name
          display_name
        }
        destination {
          id
          namespace
          name
          display_name
        }
      }
    }
  }
`

const Edge: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { edgeId } = useParams()

  const { loading, error, data } = useQuery(GET_EDGE, {
    variables: {
      organisationName,
      workspaceName,
      edgeId: edgeId ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const edge = data?.workspace?.edge

  if (!edge) return <NotFound />

  const tabs = [
    {
      label: "Profile",
      value: "profile",
      component: (
        <>
          <PageContent>
            <EdgeProfile edge={edge} />
          </PageContent>
        </>
      ),
      noWrapper: true,
    },
    {
      label: "Lineage",
      value: "lineage",
      component: <EdgeLineage edge={edge} />,
      noWrapper: true,
    },
  ]

  return (
    <PageLayout>
      <TabState tabs={tabs}>
        <PageHeader title={edge.display_name} tabs />
        <PageTabs />
      </TabState>
    </PageLayout>
  )
}

export default Edge
