import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Checkbox, FormControlLabel, FormGroup, TextField } from "@mui/material"
import { useSnackbar } from "notistack"
import { useNavigate } from "react-router-dom"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  CreateWorkspace,
  CreateWorkspaceVariables,
} from "./__generated__/CreateWorkspace"

export const CREATE_WORKSPACE = gql`
  mutation CreateWorkspace(
    $organisationName: String!
    $name: String!
    $sample_data: Boolean!
  ) {
    createWorkspace(
      organisationName: $organisationName
      name: $name
      sample_data: $sample_data
    ) {
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
  sample_data: boolean
}

const OrganisationForm: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar()
  const navigate = useNavigate()

  const [values, setValues] = useState<FormValues>({
    organisationName: "",
    name: "production",
    sample_data: false,
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
        label="Name"
        fullWidth
        margin="normal"
        required
        value={values.organisationName}
        onChange={event =>
          setValues({ ...values, organisationName: event.target.value })
        }
      />
      <FormGroup sx={{ my: 2 }}>
        <FormControlLabel
          control={
            <Checkbox
              checked={values.sample_data}
              onChange={(event, checked) =>
                setValues({ ...values, sample_data: checked })
              }
            />
          }
          label="Populate with sample data"
        />
      </FormGroup>
      <LoadingButton
        variant="contained"
        fullWidth
        type="submit"
        size="large"
        loading={loading}
        sx={{ height: 56, my: 2 }}
      >
        NEXT
      </LoadingButton>
    </Form>
  )
}

export default OrganisationForm
