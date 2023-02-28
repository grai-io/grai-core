import React, { useState } from "react"
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
  CircularProgress,
} from "@mui/material"
import { Link } from "react-router-dom"
import GraphError from "components/utils/GraphError"

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
  loading?: boolean
}

const WorkspaceList: React.FC<WorkspaceListProps> = ({
  workspaces,
  onSelect,
  link,
  error,
  loading,
}) => {
  const [selected, setSelected] = useState<Workspace | null>(null)

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

  const handleClick = (workspace: Workspace) => () => {
    setSelected(workspace)
    if (onSelect) onSelect(workspace)
  }

  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <Box sx={{ p: 3 }}>
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
                    <ListItem
                      button
                      secondaryAction={
                        loading && workspace.id === selected?.id ? (
                          <CircularProgress size={20} />
                        ) : null
                      }
                      onClick={handleClick(workspace)}
                      disabled={loading}
                    >
                      <ListItemText primary={workspace.name} />
                    </ListItem>
                  )}
                </ListItem>
              ))}
            </React.Fragment>
          ))}
        </List>
      </Box>
    </Card>
  )
}

export default WorkspaceList
