import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box, Grid, TextField, Typography } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { useSnackbar } from "notistack"
import { useNavigate } from "react-router-dom"
import Form from "components/form/Form"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import {
  UpdatePassword,
  UpdatePasswordVariables,
} from "./__generated__/UpdatePassword"

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
  const { routePrefix } = useWorkspace()
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
      .then(() => navigate(`${routePrefix}/settings/profile`))
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
