import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import CreateFilter from "components/filters/CreateFilter"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceFilterCreate,
  GetWorkspaceFilterCreateVariables,
} from "./__generated__/GetWorkspaceFilterCreate"

export const GET_WORKSPACE = gql`
  query GetWorkspaceFilterCreate(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
      namespaces {
        data
      }
      tags {
        data
      }
      sources {
        data {
          id
          name
        }
      }
    }
  }
`

const FilterCreate: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceFilterCreate,
    GetWorkspaceFilterCreateVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return (
    <PageLayout>
      <PageHeader title="Create Filter" />
      <PageContent>
        <CreateFilter
          workspaceId={workspace.id}
          namespaces={workspace.namespaces.data}
          tags={workspace.tags.data}
          sources={workspace.sources.data}
        />
      </PageContent>
    </PageLayout>
  )
}

export default FilterCreate
