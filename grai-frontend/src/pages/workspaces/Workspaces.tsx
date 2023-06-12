import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Container } from "@mui/material"
import { useLocation } from "react-router-dom"
import GraiLogo from "components/icons/GraiLogo"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import CreateOrganisation from "components/workspaces/CreateOrganisation"
import WorkspaceList from "components/workspaces/WorkspaceList"
import WorkspaceNotFound from "components/workspaces/WorkspaceNotFound"
import { GetWorkspaces } from "./__generated__/GetWorkspaces"

export const GET_WORKSPACES = gql`
  query GetWorkspaces {
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

const Workspaces: React.FC = () => {
  const location = useLocation()

  const { loading, error, data } = useQuery<GetWorkspaces>(GET_WORKSPACES, {
    fetchPolicy: "network-only",
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  if (data?.workspaces.length === 0) return <CreateOrganisation />

  return (
    <Container maxWidth="sm" sx={{ mt: 20 }}>
      <GraiLogo />
      {location.state?.workspaceNotFound && (
        <WorkspaceNotFound
          organisationName={location.state.organisationName}
          workspaceName={location.state.workspaceName}
        />
      )}
      {data?.workspaces && <WorkspaceList workspaces={data.workspaces} link />}
    </Container>
  )
}

export default Workspaces
