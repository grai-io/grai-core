import React from "react"
import { gql, useMutation } from "@apollo/client"
import {
  Box,
  Card,
  Grid,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material"
import { useConfirm } from "material-ui-confirm"
import { useSnackbar } from "notistack"
import { clearWorkspace as clearWorkspaceCache } from "helpers/cache"
import {
  ClearWorkspace,
  ClearWorkspaceVariables,
} from "./__generated__/ClearWorkspace"
import { LoadingButton } from "@mui/lab"

export const CLEAR_WORKSPACE = gql`
  mutation ClearWorkspace($id: ID!) {
    clearWorkspace(id: $id) {
      id
    }
  }
`

interface Workspace {
  id: string
  name: string
}

type WorkspaceDangerProps = {
  workspace: Workspace
}

const WorkspaceDanger: React.FC<WorkspaceDangerProps> = ({ workspace }) => {
  const confirm = useConfirm()
  const { enqueueSnackbar } = useSnackbar()

  const [clearWorkspace, { loading }] = useMutation<
    ClearWorkspace,
    ClearWorkspaceVariables
  >(CLEAR_WORKSPACE, {
    variables: { id: workspace.id },
    update(cache) {
      clearWorkspaceCache(cache, workspace.id)
    },
  })

  const handleClick = () => {
    confirm({
      title: "Clear Workspace",
      description: `Are you sure you wish to clear the ${workspace.name} workspace?`,
      confirmationText: "Clear",
    })
      .then(() => clearWorkspace())
      .then(() => enqueueSnackbar("Workspace cleared", { variant: "success" }))
      .catch(
        error =>
          error &&
          enqueueSnackbar(`Failed to clear workspace ${error}`, {
            variant: "error",
          }),
      )
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Danger Zone
      </Typography>
      <Grid container>
        <Grid item md={6}>
          <Card
            variant="outlined"
            sx={{ borderColor: theme => theme.palette.error.dark }}
          >
            <List>
              <ListItem
                secondaryAction={
                  <LoadingButton
                    variant="outlined"
                    color="error"
                    onClick={handleClick}
                    loading={loading}
                  >
                    Clear Workspace
                  </LoadingButton>
                }
              >
                <ListItemText
                  primary="Clear Workspace"
                  secondary="Delete all nodes and edges from this workspace"
                />
              </ListItem>
            </List>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default WorkspaceDanger
