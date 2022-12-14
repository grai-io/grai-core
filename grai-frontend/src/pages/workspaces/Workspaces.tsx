import { gql, useQuery } from "@apollo/client"
import {
  Container,
  List,
  ListItem,
  ListItemButton,
  Typography,
} from "@mui/material"
import React from "react"
import { Link } from "react-router-dom"
import Loading from "../../components/layout/Loading"
import { GetWorkspaces } from "./__generated__/GetWorkspaces"

const GET_WORKSPACES = gql`
  query GetWorkspaces {
    workspaces {
      id
      name
    }
  }
`

const Workspaces: React.FC = () => {
  const { loading, error, data } = useQuery<GetWorkspaces>(GET_WORKSPACES)

  if (error) return <p>Error : {error.message}</p>
  if (loading) return <Loading />

  return (
    <Container maxWidth="sm" sx={{ textAlign: "center" }}>
      <Typography variant="h6" sx={{ mt: 20 }}>
        Select Workspace
      </Typography>
      <List>
        {data?.workspaces.map(workspace => (
          <ListItem key={workspace.id}>
            <ListItemButton component={Link} to={`/workspaces/${workspace.id}`}>
              {workspace.name}
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Container>
  )
}

export default Workspaces
