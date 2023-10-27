import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import PageHeader from "components/layout/PageHeader"
import PageTabs from "components/layout/PageTabs"
import SourceDetail from "components/sources/SourceDetail"
import SourceLineage from "components/sources/SourceLineage"
import SourceMenu from "components/sources/SourceMenu"
import SourceNodes from "components/sources/SourceNodes"
import TabState from "components/tabs/TabState"
import GraphError from "components/utils/GraphError"
import { GetSource, GetSourceVariables } from "./__generated__/GetSource"

export const GET_SOURCE = gql`
  query GetSource(
    $organisationName: String!
    $workspaceName: String!
    $sourceId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      source(id: $sourceId) {
        id
        name
        priority
        connections(filters: { temp: false }) {
          data {
            id
            name
            connector {
              id
              name
              icon
            }
            last_run {
              id
              status
            }
          }
        }
      }
    }
  }
`

const Source: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { sourceId } = useParams()

  const { loading, error, data } = useQuery<GetSource, GetSourceVariables>(
    GET_SOURCE,
    {
      variables: {
        organisationName,
        workspaceName,
        sourceId: sourceId ?? "",
      },
    },
  )

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspace = data?.workspace
  const source = data?.workspace?.source

  if (!workspace || !source) return <NotFound />

  const tabs = [
    {
      value: "configuration",
      label: "Configuration",
      component: <SourceDetail source={source} workspaceId={workspace.id} />,
      noWrapper: true,
    },
    {
      value: "nodes",
      label: "Nodes",
      component: <SourceNodes source={source} workspaceId={workspace.id} />,
    },
    {
      value: "lineage",
      label: "Lineage",
      component: <SourceLineage source={source} />,
      noWrapper: true,
    },
  ]

  return (
    <TabState tabs={tabs}>
      <PageHeader
        title={source.name}
        buttons={<SourceMenu source={source} workspaceId={workspace.id} />}
        tabs
      />
      <PageTabs />
    </TabState>
  )
}

export default Source
