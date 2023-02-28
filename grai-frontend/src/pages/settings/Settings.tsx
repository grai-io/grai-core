import React from "react"
import { gql, useQuery } from "@apollo/client"
import { AccountCircle, Business, People, VpnKey } from "@mui/icons-material"
import {
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Divider,
  Grid,
  Typography,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link } from "react-router-dom"
import NotFound from "pages/NotFound"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import {
  GetWorkspaceSettings,
  GetWorkspaceSettingsVariables,
} from "./__generated__/GetWorkspaceSettings"

export const GET_WORKSPACE = gql`
  query GetWorkspaceSettings(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
    }
  }
`

const pages = [
  {
    label: "Profile",
    icon: (
      <AccountCircle
        fontSize="large"
        sx={{ color: theme => theme.palette.grey[500] }}
      />
    ),
    to: "profile",
  },
  {
    label: "API Keys",
    icon: (
      <VpnKey
        fontSize="large"
        sx={{ color: theme => theme.palette.grey[500] }}
      />
    ),
    to: "api-keys",
  },
  {
    label: "Workspace Settings",
    icon: (
      <Business
        fontSize="large"
        sx={{ color: theme => theme.palette.grey[500] }}
      />
    ),
    to: "workspace",
  },
  {
    label: "Users",
    icon: (
      <People
        fontSize="large"
        sx={{ color: theme => theme.palette.grey[500] }}
      />
    ),
    to: "memberships",
  },
]

const Settings: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetWorkspaceSettings,
    GetWorkspaceSettingsVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <SettingsLayout loading />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return (
    <SettingsLayout>
      <Grid container spacing={5} sx={{ p: 5 }}>
        {pages.map(page => (
          <Grid item md={2} key={page.label}>
            <Card variant="outlined">
              <CardActionArea component={Link} to={page.to}>
                <CardMedia sx={{ textAlign: "center", py: 2 }}>
                  {page.icon}
                </CardMedia>
                <Divider />
                <CardContent sx={{ py: 5 }}>
                  <Typography sx={{ textAlign: "center" }}>
                    {page.label}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </SettingsLayout>
  )
}

export default Settings
