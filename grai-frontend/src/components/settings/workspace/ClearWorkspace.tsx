import React from "react"
import { gql, useMutation } from "@apollo/client"
import { useConfirm } from "material-ui-confirm"
import { useSnackbar } from "notistack"
import { clearWorkspace as clearWorkspaceCache } from "helpers/cache"
import {
  ClearWorkspace as ClearWorkspaceType,
  ClearWorkspaceVariables,
} from "./__generated__/ClearWorkspace"
import DangerItem from "./DangerItem"
import { Workspace } from "./WorkspaceDanger"

export const CLEAR_WORKSPACE = gql`
  mutation ClearWorkspace($id: ID!) {
    clearWorkspace(id: $id) {
      id
    }
  }
`

type ClearWorkspaceProps = { workspace: Workspace }

const ClearWorkspace: React.FC<ClearWorkspaceProps> = ({ workspace }) => {
  const confirm = useConfirm()
  const { enqueueSnackbar } = useSnackbar()

  const [clearWorkspace, { loading }] = useMutation<
    ClearWorkspaceType,
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
    <DangerItem
      onClick={handleClick}
      loading={loading}
      primary="Clear Workspace"
      secondary="Delete all nodes and edges from this workspace"
      buttonText="Clear Workspace"
    />
  )
}

export default ClearWorkspace
