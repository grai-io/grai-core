import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { TextField, Typography } from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  CreateWorkspace,
  CreateWorkspaceVariables,
} from "./__generated__/CreateWorkspace"
import { Workspace } from "./CreateOrganisation"

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

type OrganisationFormProps = {
  onCreate?: (workspace: Workspace) => void
}

const OrganisationForm: React.FC<OrganisationFormProps> = ({ onCreate }) => {
  const [values, setValues] = useState<FormValues>({
    organisationName: "",
    name: "demo",
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
      .then(workspace => workspace && onCreate && onCreate(workspace))
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
      <Typography sx={{ my: 2 }} variant="body2">
        Contact your administrator to access an existing organisation.
      </Typography>
    </Form>
  )
}

export default OrganisationForm
