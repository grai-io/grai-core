import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Container } from "@mui/material"
import { useSearchParams } from "react-router-dom"
import WorkspaceChoice from "components/installations/WorkspaceChoice"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import { GetWorkspacesPostInstall } from "./__generated__/GetWorkspacesPostInstall"

export const GET_WORKSPACES = gql`
  query GetWorkspacesPostInstall {
    workspaces {
      id
      name
      organisation {
        id
        name
      }
    }
  }
`

const PostInstall: React.FC = () => {
  const [searchParams] = useSearchParams()

  const installationId = Number(searchParams.get("installation_id"))

  const { loading, error, data } =
    useQuery<GetWorkspacesPostInstall>(GET_WORKSPACES)

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspaces = data?.workspaces ?? []

  return (
    <Container maxWidth="sm" sx={{ mt: 20 }}>
      <WorkspaceChoice
        workspaces={workspaces}
        installationId={installationId}
      />
    </Container>
  )
}

export default PostInstall
