import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import HomeCards from "components/home/HomeCards"
import ReportsCard from "components/home/ReportsCard"
import WelcomeCard from "components/home/WelcomeCard"
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
        <WelcomeCard search={search} setSearch={setSearch} />
        <HomeCards />
        <ReportsCard />
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
