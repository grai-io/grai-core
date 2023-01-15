import React, { useState } from "react"
import SettingsLayout from "components/settings/SettingsLayout"
import Form from "components/form/Form"
import { Box, Grid, TextField, Typography } from "@mui/material"
import { LoadingButton } from "@mui/lab"
import { gql, useMutation } from "@apollo/client"
import GraphError from "components/utils/GraphError"
import { useNavigate, useParams } from "react-router-dom"
import {
  UpdatePassword,
  UpdatePasswordVariables,
} from "./__generated__/UpdatePassword"
import { useSnackbar } from "notistack"

export const UPDATE_PASSWORD = gql`
  mutation UpdatePassword($old_password: String!, $password: String!) {
    updatePassword(old_password: $old_password, password: $password) {
      id
    }
  }
`

type Values = {
  old_password: string
  password: string
}

const PasswordSettings: React.FC = () => {
  const { workspaceId } = useParams()
  const navigate = useNavigate()
  const { enqueueSnackbar } = useSnackbar()

  const [values, setValues] = useState<Values>({
    old_password: "",
    password: "",
  })

  const [updatePassword, { loading, error }] = useMutation<
    UpdatePassword,
    UpdatePasswordVariables
  >(UPDATE_PASSWORD)

  const handleSubmit = () =>
    updatePassword({
      variables: values,
    })
      .then(() => enqueueSnackbar("Password updated"))
      .then(() => navigate(`/workspaces/${workspaceId}/settings/profile`))
      .catch(err => {})

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <Typography variant="h5" sx={{ mb: 3 }}>
          Change Password
        </Typography>
        <Grid container>
          <Grid item md={6}>
            {error && <GraphError error={error} />}
            <Form onSubmit={handleSubmit}>
              <TextField
                label="Current Password"
                value={values.old_password}
                onChange={event =>
                  setValues({ ...values, old_password: event.target.value })
                }
                margin="normal"
                type="password"
                fullWidth
                required
                inputProps={{ "data-testid": "current-password" }}
              />
              <TextField
                label="New Password"
                value={values.password}
                onChange={event =>
                  setValues({ ...values, password: event.target.value })
                }
                margin="normal"
                type="password"
                fullWidth
                required
                inputProps={{ "data-testid": "new-password" }}
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
          </Grid>
        </Grid>
      </Box>
    </SettingsLayout>
  )
}

export default PasswordSettings
