import React from "react"
import { gql, useQuery } from "@apollo/client"
import { useParams } from "react-router-dom"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import FilterHeader from "components/filters/FilterHeader"
import UpdateFilter from "components/filters/UpdateFilter"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import { GetFilter, GetFilterVariables } from "./__generated__/GetFilter"

export const GET_FILTER = gql`
  query GetFilter(
    $organisationName: String!
    $workspaceName: String!
    $filterId: ID!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      filter(id: $filterId) {
        id
        name
        metadata
        created_at
      }
      tags {
        data
      }
    }
  }
`

const Filter: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const { filterId } = useParams()

  const { loading, error, data } = useQuery<GetFilter, GetFilterVariables>(
    GET_FILTER,
    {
      variables: {
        organisationName,
        workspaceName,
        filterId: filterId ?? "",
      },
    }
  )

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const filter = data?.workspace?.filter

  if (!filter) return <NotFound />

  return (
    <PageLayout>
      <FilterHeader filter={filter} />
      <UpdateFilter
        filter={filter}
        tags={data?.workspace?.tags.data}
        workspaceId={data?.workspace.id}
      />
    </PageLayout>
  )
}

export default Filter
