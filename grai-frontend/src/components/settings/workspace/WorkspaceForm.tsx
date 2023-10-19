import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box, TextField } from "@mui/material"
import { useSnackbar } from "notistack"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  UpdateWorkspace,
  UpdateWorkspaceVariables,
} from "./__generated__/UpdateWorkspace"

export const UPDATE_WORKSPACE = gql`
  mutation UpdateWorkspace($id: ID!, $name: String!) {
    updateWorkspace(id: $id, name: $name) {
      id
      name
    }
  }
`

type Values = {
  name: string
}

interface Workspace {
  id: string
  name: string
}

type WorkspaceFormProps = {
  workspace: Workspace
}

const WorkspaceForm: React.FC<WorkspaceFormProps> = ({ workspace }) => {
  const [values, setValues] = useState<Values>(workspace)
  const { enqueueSnackbar } = useSnackbar()

  const [updateWorkspace, { loading, error }] = useMutation<
    UpdateWorkspace,
    UpdateWorkspaceVariables
  >(UPDATE_WORKSPACE)

  const handleSubmit = () =>
    updateWorkspace({
      variables: {
        id: workspace.id,
        name: values.name,
      },
    })
      .then(() => enqueueSnackbar("Workspace updated"))
      .catch(err => {})

  return (
    <Box sx={{ maxWidth: "475px", pl: "48px" }}>
      <Form onSubmit={handleSubmit}>
        {error && <GraphError error={error} />}
        <TextField
          label="Name"
          value={values.name}
          onChange={event => setValues({ ...values, name: event.target.value })}
          margin="normal"
          fullWidth
          required
        />
        <LoadingButton
          type="submit"
          variant="contained"
          sx={{ mt: 2 }}
          loading={loading}
        >
          Save
        </LoadingButton>
      </Form>
    </Box>
  )
}

export default WorkspaceForm
