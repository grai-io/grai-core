import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import EdgeLineage from "components/edges/EdgeLineage"
import EdgeProfile from "components/edges/EdgeProfile"
import Loading from "components/layout/Loading"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageTabs from "components/layout/PageTabs"
import TabState from "components/tabs/TabState"
import GraphError from "components/utils/GraphError"
import { GetEdge, GetEdgeVariables } from "./__generated__/GetEdge"

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
        data_sources {
          data {
            id
            name
            connections {
              data {
                id
                connector {
                  id
                  name
                  slug
                }
              }
            }
          }
        }
      }
    }
  }
`

const Edge: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { edgeId } = useParams()

  const { loading, error, data } = useQuery<GetEdge, GetEdgeVariables>(
    GET_EDGE,
    {
      variables: {
        organisationName,
        workspaceName,
        edgeId: edgeId ?? "",
      },
    },
  )

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

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
    <TabState tabs={tabs}>
      <PageHeader title={edge.display_name} tabs />
      <PageTabs />
    </TabState>
  )
}

export default Edge
