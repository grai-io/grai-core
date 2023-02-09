import {
  Card,
  Box,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
} from "@mui/material"
import React from "react"
import { Link } from "react-router-dom"

interface Organisation {
  id: string
  name: string
}

interface Workspace {
  id: string
  organisation: Organisation
  name: string
}

type WorkspaceChoiceProps = {
  workspaces: Workspace[]
}

const WorkspaceChoice: React.FC<WorkspaceChoiceProps> = ({ workspaces }) => (
  <Card variant="outlined" sx={{ mt: 2 }}>
    <Box sx={{ p: 3 }}>
      {workspaces.length > 0 ? (
        <>
          <Typography variant="h6">Select Workspace</Typography>
          <List sx={{ pb: 0 }}>
            {workspaces.map(workspace => (
              <ListItem key={workspace.id} disablePadding>
                <ListItemButton
                  component={Link}
                  to={`/${workspace.organisation.name}/${workspace.name}`}
                >
                  <ListItemText primary={workspace.name} />
                </ListItemButton>
              </ListItem>
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

export default WorkspaceChoice
