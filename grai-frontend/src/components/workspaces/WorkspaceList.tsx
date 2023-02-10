import { ApolloError } from "@apollo/client"
import {
  Card,
  Box,
  Typography,
  List,
  ListSubheader,
  ListItem,
  ListItemButton,
  ListItemText,
} from "@mui/material"
import GraphError from "components/utils/GraphError"
import React from "react"
import { Link } from "react-router-dom"

export interface Organisation {
  id: string
  name: string
}

export interface Workspace {
  id: string
  name: string
  organisation: Organisation
}

interface OrganisationWithWorkspaces extends Organisation {
  workspaces: Workspace[]
}

type WorkspaceListProps = {
  workspaces: Workspace[]
  onSelect?: (workspace: Workspace) => void
  link?: boolean
  error?: ApolloError
}

const WorkspaceList: React.FC<WorkspaceListProps> = ({
  workspaces,
  onSelect,
  link,
  error,
}) => {
  const organisations = workspaces.reduce<OrganisationWithWorkspaces[]>(
    (res, workspace) => {
      const existingOrganisation = res.find(
        r => r.id === workspace.organisation.id
      )
      if (existingOrganisation) {
        existingOrganisation.workspaces =
          existingOrganisation.workspaces.concat(workspace)

        return res
      }

      return res.concat({ ...workspace.organisation, workspaces: [workspace] })
    },
    []
  )

  const handleClick = (workspace: Workspace) => () =>
    onSelect && onSelect(workspace)

  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <Box sx={{ p: 3 }}>
        {workspaces.length > 0 ? (
          <>
            <Typography variant="h6">Select Workspace</Typography>
            {error && <GraphError error={error} />}
            <List sx={{ pb: 0 }}>
              {organisations.map(organisation => (
                <React.Fragment key={organisation.id}>
                  <ListSubheader>{organisation.name}</ListSubheader>
                  {organisation.workspaces.map(workspace => (
                    <ListItem key={workspace.id} disablePadding>
                      {link ? (
                        <ListItemButton
                          component={Link}
                          to={`/${workspace.organisation.name}/${workspace.name}`}
                        >
                          <ListItemText primary={workspace.name} />
                        </ListItemButton>
                      ) : (
                        <ListItemButton onClick={handleClick(workspace)}>
                          <ListItemText primary={workspace.name} />
                        </ListItemButton>
                      )}
                    </ListItem>
                  ))}
                </React.Fragment>
              ))}
            </List>
          </>
        ) : (
          <Box sx={{ textAlign: "center" }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              No Workspaces
            </Typography>
            <Typography variant="body1">
              You are not a member of any workspaces.
              <br />
              Please contact your administrator.
            </Typography>
          </Box>
        )}
      </Box>
    </Card>
  )
}

export default WorkspaceList
