import React from "react"
import { gql, useMutation } from "@apollo/client"
import { useSnackbar } from "notistack"
import {
  UpdateWorkspaceSampleData,
  UpdateWorkspaceSampleDataVariables,
} from "./__generated__/UpdateWorkspaceSampleData"
import DangerItem from "./DangerItem"

export const UPDATE_WORKSPACE = gql`
  mutation UpdateWorkspaceSampleData($id: ID!) {
    updateWorkspace(id: $id, sample_data: false) {
      id
      sample_data
    }
  }
`

interface Workspace {
  id: string
}

type HideDemoWorkspaceProps = {
  workspace: Workspace
}

const HideDemoWorkspace: React.FC<HideDemoWorkspaceProps> = ({ workspace }) => {
  const { enqueueSnackbar } = useSnackbar()

  const [updateWorkspace, { loading }] = useMutation<
    UpdateWorkspaceSampleData,
    UpdateWorkspaceSampleDataVariables
  >(UPDATE_WORKSPACE, {
    variables: { id: workspace.id },
  })

  const handleClick = () => {
    updateWorkspace()
      .then(() =>
        enqueueSnackbar("Demo banners hidden", { variant: "success" }),
      )
      .catch(error =>
        enqueueSnackbar(`Failed to update workspace ${error}`, {
          variant: "error",
        }),
      )
  }

  return (
    <DangerItem
      onClick={handleClick}
      loading={loading}
      primary="Hide Demo Banners"
      secondary="Hide all demo banners from this workspace"
      buttonText="Hide Demo Banners"
    />
  )
}

export default HideDemoWorkspace
