import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import PageTabs from "components/layout/PageTabs"
import TableColumns from "components/nodes/columns/TableColumns"
import NodeProfile from "components/nodes/NodeProfile"
import TableEvents from "components/tables/TableEvents"
import TableLineage from "components/tables/TableLineage"
import TabState from "components/tabs/TabState"
import GraphError from "components/utils/GraphError"
import { GetNode, GetNodeVariables } from "./__generated__/GetNode"

export const GET_NODE = gql`
  query GetNode(
    $organisationName: String!
    $workspaceName: String!
    $nodeId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      node(id: $nodeId) {
        id
        namespace
        name
        display_name
        is_active
        metadata
        columns {
          data {
            id
            name
            display_name
            requirements_edges {
              data {
                id
                metadata
                destination {
                  id
                  name
                  display_name
                  metadata
                }
              }
            }
            metadata
          }
        }
        # source_tables {
        #   data {
        #     id
        #     name
        #     display_name
        #   }
        # }
        # destination_tables {
        #   data {
        #     id
        #     name
        #     display_name
        #   }
        # }
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
        events {
          data {
            id
            date
            status
            connection {
              id
              name
              connector {
                id
                name
              }
            }
          }
        }
      }
    }
  }
`

const Table: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { nodeId } = useParams()

  const { loading, error, data } = useQuery<GetNode, GetNodeVariables>(
    GET_NODE,
    {
      variables: {
        organisationName,
        workspaceName,
        nodeId: nodeId ?? "",
      },
    },
  )

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const node = data?.workspace?.node

  if (!node) return <NotFound />

  const tabs = [
    {
      label: "Profile",
      value: "profile",
      component: (
        <>
          <PageContent>
            <NodeProfile node={node} />
          </PageContent>
          {node.metadata.grai.node_type === "Table" && (
            <PageContent>
              <TableColumns columns={node.columns.data} />
            </PageContent>
          )}
        </>
      ),
      noWrapper: true,
    },
    {
      label: "Sample",
      value: "sample",
      disabled: true,
    },
    {
      label: "Lineage",
      value: "lineage",
      component: <TableLineage table={node} />,
      noWrapper: true,
    },
    {
      label: "Events",
      value: "events",
      component: <TableEvents table={node} />,
      noWrapper: true,
    },
  ]

  return (
    <PageLayout>
      <TabState tabs={tabs}>
        <PageHeader title={node.display_name} tabs />
        <PageTabs />
      </TabState>
    </PageLayout>
  )
}

export default Table
