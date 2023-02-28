import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import { useSnackbar } from "notistack"
import { useNavigate } from "react-router-dom"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  CreateWorkspace,
  CreateWorkspaceVariables,
} from "./__generated__/CreateWorkspace"

export const CREATE_WORKSPACE = gql`
  mutation CreateWorkspace($organisationName: String!, $name: String!) {
    createWorkspace(organisationName: $organisationName, name: $name) {
      id
      name
      organisation {
        id
        name
      }
    }
  }
`

type FormValues = {
  organisationName: string
  name: string
}

const WorkspaceForm: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar()
  const navigate = useNavigate()

  const [values, setValues] = useState<FormValues>({
    organisationName: "",
    name: "",
  })

  const [createWorkspace, { loading, error }] = useMutation<
    CreateWorkspace,
    CreateWorkspaceVariables
  >(CREATE_WORKSPACE)

  const handleSubmit = () =>
    createWorkspace({
      variables: values,
    })
      .then(data => data.data?.createWorkspace)
      .then(data => data && navigate(`/${data.organisation.name}/${data.name}`))
      .then(() => enqueueSnackbar("Workspace created"))
      .catch(() => {})

  return (
    <Form onSubmit={handleSubmit}>
      {error && <GraphError error={error} />}
      <TextField
        id="organisationName"
        label="Organisation Name"
        fullWidth
        margin="normal"
        required
        value={values.organisationName}
        onChange={event =>
          setValues({ ...values, organisationName: event.target.value })
        }
      />
      <TextField
        id="name"
        label="Workspace Name"
        fullWidth
        margin="normal"
        required
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
      />
      <LoadingButton
        variant="contained"
        fullWidth
        type="submit"
        size="large"
        loading={loading}
        sx={{ height: 56, my: 2, color: "white" }}
      >
        SAVE
      </LoadingButton>
    </Form>
  )
}

export default WorkspaceForm
