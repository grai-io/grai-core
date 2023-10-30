import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
// import { ShepherdTourContext } from "react-shepherd"
// import useLocalState from "helpers/useLocalState"
import useLocalState from "helpers/useLocalState"
import useWorkspace from "helpers/useWorkspace"
import GettingStarted from "components/home/GettingStarted"
import HomeCards from "components/home/HomeCards"
import ReportsCard from "components/home/ReportsCard"
import SampleDataDialog from "components/home/SampleDataDialog"
import SourceGraph from "components/home/SourceGraph"
import WelcomeCard from "components/home/WelcomeCard"
import Loading from "components/layout/Loading"
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
      sample_data
      runs(filters: { action: TESTS }, order: { created_at: DESC }) {
        meta {
          filtered
        }
      }
      nodes(filters: { node_type: { equals: "Table" } }) {
        meta {
          filtered
        }
      }
      sources {
        meta {
          total
        }
      }
    }
  }
`

const Home: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()
  // const tour = useContext(ShepherdTourContext)
  const [search, setSearch] = useState(false)

  // const [tourHidden, setTourHidden] = useLocalState(
  //   "getting-started-tour",
  //   false,
  // )

  const [sampleDialogHidden, setSampleDialogHidden] = useLocalState(
    "sample-dialog",
    false,
  )

  const { loading, error, data } = useQuery<
    GetWorkspaceHome,
    GetWorkspaceHomeVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  // useEffect(() => {
  //   if (!tour || tourHidden) return

  //   tour.on("cancel", () => {
  //     setTourHidden(true)
  //   })

  //   tour.start()
  // }, [tour, tourHidden, setTourHidden])

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  const handleClose = () => setSearch(false)

  return (
    <>
      <Box sx={{ padding: "24px" }}>
        <WelcomeCard search={search} setSearch={setSearch} />
        <HomeCards />
        {workspace.sources.meta.total === 0 &&
          workspace.nodes.meta.filtered === 0 && <GettingStarted />}
        <ReportsCard />
        <SourceGraph workspaceId={workspace.id} />
      </Box>
      <SearchDialog
        open={search}
        onClose={handleClose}
        workspaceId={workspace.id}
      />
      {workspace.sample_data && (
        <SampleDataDialog
          open={!sampleDialogHidden}
          onClose={() => setSampleDialogHidden(true)}
        />
      )}
    </>
  )
}

export default Home
