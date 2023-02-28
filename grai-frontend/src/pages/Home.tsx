import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Search } from "@mui/icons-material"
import {
  Box,
  Container,
  InputAdornment,
  TextField,
  Typography,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import HomeCards from "components/home/HomeCards"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceHome,
  GetWorkspaceHomeVariables,
} from "./__generated__/GetWorkspaceHome"
import NotFound from "./NotFound"

export const GET_WORKSPACE = gql`
  query GetWorkspaceHome($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
    }
  }
`

const Home: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceHome,
    GetWorkspaceHomeVariables
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
      <Container maxWidth="lg" sx={{ textAlign: "center" }}>
        <Box sx={{ mt: 15 }}>
          <img src="/logo512.png" width="75px" height="75px" alt="logo" />
        </Box>

        <Typography variant="h4" sx={{ mt: 2, mb: 15 }}>
          Welcome to Grai
        </Typography>
        <TextField
          placeholder="Search data assets"
          sx={{ width: 750, mb: 15 }}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <Search />
              </InputAdornment>
            ),
          }}
        />
        <HomeCards />
      </Container>
    </PageLayout>
  )
}

export default Home
