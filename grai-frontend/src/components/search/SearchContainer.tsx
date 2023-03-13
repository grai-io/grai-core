import { gql, useQuery } from "@apollo/client"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import React from "react"
import SearchForm from "./SearchForm"
import algoliasearch from "algoliasearch/lite"
import { InstantSearch } from "react-instantsearch-hooks-web"
import {
  GetSearchKey,
  GetSearchKeyVariables,
} from "./__generated__/GetSearchKey"

export const GET_SEARCH_KEY = gql`
  query GetSearchKey($workspaceId: ID!) {
    workspace(id: $workspaceId) {
      id
      search_key
    }
  }
`

type SearchContainerProps = {
  workspaceId: string
  onClose: () => void
}

const SearchContainer: React.FC<SearchContainerProps> = ({
  onClose,
  workspaceId,
}) => {
  const { loading, error, data } = useQuery<
    GetSearchKey,
    GetSearchKeyVariables
  >(GET_SEARCH_KEY, {
    variables: {
      workspaceId,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  if (!process.env.REACT_APP_ALGOLIA_APP_ID) return <>No Algolia App Id</>
  if (!data?.workspace?.search_key) return <>No Search Key</>

  const searchClient = algoliasearch(
    process.env.REACT_APP_ALGOLIA_APP_ID,
    data.workspace.search_key
  )

  return (
    <InstantSearch searchClient={searchClient} indexName="main">
      <SearchForm onClose={onClose} />
    </InstantSearch>
  )
}

export default SearchContainer
