import { gql, useMutation } from "@apollo/client"
import WorkspaceList, { Workspace } from "components/workspaces/WorkspaceList"
import { useSnackbar } from "notistack"
import React from "react"
import { useNavigate } from "react-router-dom"
import {
  AddInstallation,
  AddInstallationVariables,
} from "./__generated__/AddInstallation"

export const ADD_INSTALLATION = gql`
  mutation AddInstallation($workspaceId: ID!, $installationId: Int!) {
    addInstallation(
      workspaceId: $workspaceId
      installationId: $installationId
    ) {
      success
    }
  }
`

type WorkspaceChoiceProps = {
  installationId: number
  workspaces: Workspace[]
}

const WorkspaceChoice: React.FC<WorkspaceChoiceProps> = ({
  installationId,
  workspaces,
}) => {
  const { enqueueSnackbar } = useSnackbar()
  const navigate = useNavigate()

  const [addInstallation, { loading, error }] = useMutation<
    AddInstallation,
    AddInstallationVariables
  >(ADD_INSTALLATION)

  const handleSelect = (workspace: Workspace) =>
    addInstallation({
      variables: {
        workspaceId: workspace.id,
        installationId,
      },
    })
      .then(() => navigate(`/${workspace.organisation.name}/${workspace.name}`))
      .then(() => enqueueSnackbar("Github updated"))

      .catch(() => {})

  return (
    <WorkspaceList
      workspaces={workspaces}
      onSelect={handleSelect}
      error={error}
      loading={loading}
    />
  )
}

export default WorkspaceChoice
