import React from "react"
import { gql, useQuery } from "@apollo/client"
import {
  Box,
  Button,
  Card,
  CircularProgress,
  Grid,
  Typography,
} from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import GraphError from "components/utils/GraphError"
import {
  GetReportsHome,
  GetReportsHomeVariables,
} from "./__generated__/GetReportsHome"
import ReportCard from "./ReportCard"

export const GET_REPORTS = gql`
  query GetReportsHome($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      runs(filters: { action: TESTS }, order: { created_at: DESC }) {
        data {
          id
          status
          connection {
            id
            name
            temp
            connector {
              id
              name
              icon
            }
          }
          commit {
            id
            reference
            title
            branch {
              id
              reference
            }
            pull_request {
              id
              reference
              title
            }
            repository {
              id
              type
              owner
              repo
            }
          }
          created_at
          started_at
          finished_at
          user {
            id
            first_name
            last_name
          }
          metadata
        }
      }
    }
  }
`

const ReportsCard: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetReportsHome,
    GetReportsHomeVariables
  >(GET_REPORTS, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />

  return (
    <Card
      sx={{ mt: "24px", borderRadius: "20px", padding: "24px" }}
      elevation={0}
    >
      <Box sx={{ display: "flex" }}>
        <Typography sx={{ fontWeight: 800, fontSize: "20px", flexGrow: 1 }}>
          Latest Reports
        </Typography>
        <Button component={Link} to="reports">
          Explore all Reports
        </Button>
      </Box>
      {loading && (
        <Box sx={{ textAlign: "center", py: 3 }}>
          <CircularProgress />
        </Box>
      )}
      {data?.workspace.runs.data.length === 0 ? (
        <Box sx={{ textAlign: "center", py: 3 }}>
          <Typography>No reports</Typography>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {data?.workspace.runs.data.slice(0, 3).map(run => (
            <Grid item md={4} key={run.id}>
              <ReportCard report={run} />
            </Grid>
          ))}
        </Grid>
      )}
    </Card>
  )
}

export default ReportsCard
