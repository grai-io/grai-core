import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Search } from "@mui/icons-material"
import {
  Box,
  Button,
  Card,
  InputAdornment,
  TextField,
  Typography,
} from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import HomeCards from "components/home/HomeCards"
import { GraiLogo, PersonAdd } from "components/icons"
import PageLayout from "components/layout/PageLayout"
import SearchDialog from "components/search/SearchDialog"
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

  const [search, setSearch] = React.useState(false)

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

  const handleClose = () => {
    setSearch(false)
  }

  return (
    <PageLayout>
      <Box sx={{ padding: "24px" }}>
        <Card
          elevation={0}
          sx={{
            borderRadius: "20px",
            borderColor: "#8338EC",
            borderWidth: "3px",
            borderStyle: "solid",
            padding: "16px",
            height: "470px",
            mb: "24px",
          }}
        >
          <Box sx={{ display: "flex" }}>
            <Box sx={{ flexGrow: 1 }} />
            <Button
              component={Link}
              to="settings/memberships"
              variant="outlined"
              startIcon={<PersonAdd />}
              sx={{
                color: "#8338EC",
                fontSize: "16px",
                fontWeight: 600,
                borderColor: "#8338EC24",
                borderRadius: "8px",
                py: 1,
                px: 3,
                boxShadow: "0 4px 6px #8338EC10",
              }}
            >
              Invite User
            </Button>
          </Box>
          <Box sx={{ textAlign: "center" }}>
            <Box>
              <GraiLogo />
            </Box>
            <Typography
              variant="h4"
              sx={{
                color: "#1F2A37",
                fontSize: 36,
                fontWeight: 800,
                mt: "20px",
              }}
            >
              Welcome to Grai
            </Typography>
            <TextField
              placeholder="Search data assets"
              onClick={() => setSearch(true)}
              disabled
              sx={{ width: 620, mb: 15, mt: "40px" }}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
          </Box>
        </Card>
        <HomeCards />
      </Box>
      <SearchDialog
        open={search}
        onClose={handleClose}
        workspaceId={workspace.id}
      />
    </PageLayout>
  )
}

export default Home
