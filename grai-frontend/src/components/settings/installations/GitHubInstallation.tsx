import React from "react"
import { gql, useQuery } from "@apollo/client"
import { GitHub } from "@mui/icons-material"
import {
  Box,
  Button,
  Card,
  CardActionArea,
  CardContent,
  CircularProgress,
  Grid,
  Link,
  Stack,
  Typography,
} from "@mui/material"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import GraphError from "components/utils/GraphError"
import {
  GetRepositoriesGitHubInstallation,
  GetRepositoriesGitHubInstallationVariables,
} from "./__generated__/GetRepositoriesGitHubInstallation"

export const GET_REPOSITORIES = gql`
  query GetRepositoriesGitHubInstallation(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      repositories(filters: { type: "github", installed: true }) {
        data {
          id
          owner
          repo
        }
      }
    }
  }
`

const GitHubInstallation: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetRepositoriesGitHubInstallation,
    GetRepositoriesGitHubInstallationVariables
  >(GET_REPOSITORIES, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />

  const workspace = data?.workspace

  if (!loading && !workspace) return <NotFound />

  const repositories = workspace?.repositories.data ?? []

  return (
    <Box
      sx={{
        p: "24px",
        borderRadius: "12px",
        boxShadow: "0px 4px 14px rgba(0, 0, 0, 0.08)",
      }}
    >
      <Box sx={{ display: "flex" }}>
        <Typography variant="h6" sx={{ mb: 2, flexGrow: 1 }}>
          GitHub
        </Typography>
        {!loading && repositories.length > 0 && (
          <Button
            variant="contained"
            component={Link}
            href="https://github.com/apps/graibot"
          >
            Configure GitHub
          </Button>
        )}
      </Box>
      {loading ? (
        <CircularProgress />
      ) : repositories.length > 0 ? (
        <Grid container>
          <Grid item xs={12} md={6}>
            <Stack direction="column" spacing={1}>
              {repositories.map(repository => (
                <Card
                  key={repository.id}
                  sx={{
                    borderRadius: "12px",
                    boxShadow: "0px 4px 14px rgba(0, 0, 0, 0.08)",
                  }}
                >
                  <CardActionArea
                    component={Link}
                    href={`https://github.com/${repository.owner}/${repository.repo}`}
                    target="_blank"
                  >
                    <CardContent sx={{ display: "flex" }}>
                      <GitHub />
                      <Typography sx={{ ml: 2 }}>
                        {repository.owner}/{repository.repo}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
              ))}
            </Stack>
          </Grid>
        </Grid>
      ) : (
        <Button
          variant="contained"
          size="large"
          component={Link}
          href="https://github.com/apps/graibot"
          sx={{ mt: 5 }}
        >
          Connect GitHub
        </Button>
      )}
    </Box>
  )
}

export default GitHubInstallation
