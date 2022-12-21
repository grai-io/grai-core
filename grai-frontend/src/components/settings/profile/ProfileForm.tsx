import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box, Grid, TextField, Typography } from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import React, { useState } from "react"
import {
  UpdateProfile,
  UpdateProfileVariables,
} from "./__generated__/UpdateProfile"

export const UPDATE_PROFILE = gql`
  mutation UpdateProfile($first_name: String!, $last_name: String!) {
    updateProfile(firstName: $first_name, lastName: $last_name) {
      id
      firstName
      lastName
    }
  }
`

type Values = {
  firstName: string
  lastName: string
}

interface Profile {
  username: string | null
  firstName: string
  lastName: string
}

type ProfileFormProps = {
  profile: Profile
}

const ProfileForm: React.FC<ProfileFormProps> = ({ profile }) => {
  const [values, setValues] = useState<Values>(profile)

  const [updateProfile, { loading, error }] = useMutation<
    UpdateProfile,
    UpdateProfileVariables
  >(UPDATE_PROFILE)

  const handleSubmit = () =>
    updateProfile({
      variables: {
        first_name: values.firstName,
        last_name: values.lastName,
      },
    }).catch(err => {})

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
              value={values.firstName}
              onChange={event =>
                setValues({ ...values, firstName: event.target.value })
              }
              margin="normal"
              fullWidth
              required
            />
            <TextField
              label="Last Name"
              value={values.lastName}
              onChange={event =>
                setValues({ ...values, lastName: event.target.value })
              }
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
        </Grid>
      </Grid>
    </Box>
  )
}

export default ProfileForm
