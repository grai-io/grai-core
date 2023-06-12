import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { TextField } from "@mui/material"
import { useSnackbar } from "notistack"
import { useNavigate, useSearchParams } from "react-router-dom"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  CreateOrganisationWorkspace,
  CreateOrganisationWorkspaceVariables,
} from "./__generated__/CreateOrganisationWorkspace"

export const CREATE_WORKSPACE = gql`
  mutation CreateOrganisationWorkspace($organisationId: ID!, $name: String!) {
    createWorkspace(organisationId: $organisationId, name: $name) {
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
  name: string
}

const WorkspaceForm: React.FC = () => {
  const { enqueueSnackbar } = useSnackbar()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()

  const [values, setValues] = useState<FormValues>({
    name: "",
  })

  const [createWorkspace, { loading, error }] = useMutation<
    CreateOrganisationWorkspace,
    CreateOrganisationWorkspaceVariables
  >(CREATE_WORKSPACE)

  const organisationId = searchParams.get("organisationId")

  if (!organisationId) return <>No organisationId found</>

  const handleSubmit = () =>
    createWorkspace({
      variables: {
        organisationId,
        name: values.name,
      },
    })
      .then(data => data.data?.createWorkspace)
      .then(data => data && navigate(`/${data.organisation.name}/${data.name}`))
      .then(() => enqueueSnackbar("Workspace created"))
      .catch(() => {})

  return (
    <Form onSubmit={handleSubmit}>
      {error && <GraphError error={error} />}
      <TextField
        id="name"
        label="Name"
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
        sx={{ height: 56, my: 2 }}
      >
        NEXT
      </LoadingButton>
    </Form>
  )
}

export default WorkspaceForm
