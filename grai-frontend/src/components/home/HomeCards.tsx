import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Grid } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Connections } from "components/icons"
import GraphError from "components/utils/GraphError"
import {
  GetCountsHome,
  GetCountsHomeVariables,
} from "./__generated__/GetCountsHome"
import HomeCard from "./HomeCard"

export const GET_COUNTS = gql`
  query GetCountsHome($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      runs(filters: { action: TESTS }) {
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

const HomeCards: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { error, data } = useQuery<GetCountsHome, GetCountsHomeVariables>(
    GET_COUNTS,
    {
      variables: {
        organisationName,
        workspaceName,
      },
    },
  )

  return (
    <Grid container spacing={3}>
      {error && <GraphError error={error} />}
      <Grid item md={3}>
        <HomeCard
          count={data?.workspace.nodes.meta.filtered}
          text="Tables"
          color="#8338EC"
          to="nodes?node_type=Table"
        />
      </Grid>
      <Grid item md={3}>
        <HomeCard
          count={data?.workspace.sources.meta.total}
          text="Sources"
          color="#8338EC"
          to="sources"
        />
      </Grid>
      <Grid item md={3}>
        <HomeCard
          count={data?.workspace.runs.meta.filtered}
          text="Reports"
          color="#8338EC"
          to="reports"
        />
      </Grid>
      <Grid item md={3}>
        <HomeCard
          text="Add Connection"
          color="#8338EC"
          icon={<Connections />}
          to="connections/create"
          className="add-connection"
        />
      </Grid>
    </Grid>
  )
}

export default HomeCards
