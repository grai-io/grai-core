import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import {
  Box,
  Button,
  Grid,
  InputAdornment,
  TextField,
  Typography,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { useSnackbar } from "notistack"
import { Link } from "react-router-dom"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import {
  UpdateProfile,
  UpdateProfileVariables,
} from "./__generated__/UpdateProfile"

export const UPDATE_PROFILE = gql`
  mutation UpdateProfile($first_name: String!, $last_name: String!) {
    updateProfile(first_name: $first_name, last_name: $last_name) {
      id
      first_name
      last_name
    }
  }
`

type Values = {
  first_name: string
  last_name: string
}

interface Profile {
  username: string | null
  first_name: string
  last_name: string
}

type ProfileFormProps = {
  profile: Profile
}

const ProfileForm: React.FC<ProfileFormProps> = ({ profile }) => {
  const { routePrefix } = useWorkspace()
  const [values, setValues] = useState<Values>(profile)
  const { enqueueSnackbar } = useSnackbar()

  const [updateProfile, { loading, error }] = useMutation<
    UpdateProfile,
    UpdateProfileVariables
  >(UPDATE_PROFILE)

  const handleSubmit = () =>
    updateProfile({
      variables: {
        first_name: values.first_name,
        last_name: values.last_name,
      },
    })
      .then(() => enqueueSnackbar("Profile updated"))
      .catch(err => {})

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Profile Settings
      </Typography>
      <Grid container>
        <Grid item md={6}>
          <Form onSubmit={handleSubmit}>
            {error && <GraphError error={error} />}
            <TextField
              label="Email"
              value={profile.username}
              margin="normal"
              fullWidth
              disabled
            />
            <TextField
              label="First Name"
              value={values.first_name}
              onChange={event =>
                setValues({ ...values, first_name: event.target.value })
              }
              margin="normal"
              fullWidth
              required
            />
            <TextField
              label="Last Name"
              value={values.last_name}
              onChange={event =>
                setValues({ ...values, last_name: event.target.value })
              }
              margin="normal"
              fullWidth
              required
            />
            <TextField
              label="Password"
              value="password"
              type="password"
              margin="normal"
              fullWidth
              disabled
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <Button
                      component={Link}
                      to={`${routePrefix}/settings/password`}
                    >
                      Change password
                    </Button>
                  </InputAdornment>
                ),
              }}
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
  )
}

export default ProfileForm
