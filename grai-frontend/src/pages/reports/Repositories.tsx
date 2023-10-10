import React from "react"
import { useQuery } from "@apollo/client"
import { Container } from "@mui/material"
import gql from "graphql-tag"
import { useParams } from "react-router"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import RepositoryList from "components/reports/repositories/RepositoryList"
import GraphError from "components/utils/GraphError"
import {
  GetRepositories,
  GetRepositoriesVariables,
} from "./__generated__/GetRepositories"

export const GET_REPOSITORIES = gql`
  query GetRepositories(
    $organisationName: String!
    $workspaceName: String!
    $type: String!
    $owner: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      repositories(filters: { type: $type, owner: $owner }) {
        data {
          id
          type
          owner
          repo
        }
      }
    }
  }
`

const Repositories: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  const params = useParams()

  const { loading, error, data } = useQuery<
    GetRepositories,
    GetRepositoriesVariables
  >(GET_REPOSITORIES, {
    variables: {
      organisationName,
      workspaceName,
      type: params.type ?? "",
      owner: params.owner ?? "",
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  return (
    <Container maxWidth="sm" sx={{ mt: 20 }}>
      <RepositoryList repositories={data?.workspace.repositories.data ?? []} />
    </Container>
  )
}

export default Repositories
