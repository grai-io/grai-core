import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import ProfileForm from "components/settings/profile/ProfileForm"
import SettingsAppBar from "components/settings/SettingsAppBar"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import { GetProfileSettings } from "./__generated__/GetProfileSettings"

export const GET_PROFILE = gql`
  query GetProfileSettings {
    profile {
      id
      username
      first_name
      last_name
    }
  }
`

const ProfileSettings: React.FC = () => {
  const { loading, error, data } = useQuery<GetProfileSettings>(GET_PROFILE)

  if (error) return <GraphError error={error} />
  if (loading) return <SettingsLayout loading />

  const profile = data?.profile

  if (!profile) return <NotFound />

  return (
    <SettingsLayout>
      <SettingsAppBar title="Personal info" />
      <ProfileForm profile={profile} />
    </SettingsLayout>
  )
}

export default ProfileSettings
