import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import ProfileForm from "components/settings/profile/ProfileForm"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import { GetProfile } from "./__generated__/GetProfile"

export const GET_PROFILE = gql`
  query GetProfile {
    profile {
      id
      username
      first_name
      last_name
    }
  }
`

const ProfileSettings: React.FC = () => {
  const { loading, error, data } = useQuery<GetProfile>(GET_PROFILE)

  if (error) return <GraphError error={error} />
  if (loading) return <SettingsLayout loading />

  const profile = data?.profile

  if (!profile) return <NotFound />

  return (
    <SettingsLayout>
      <ProfileForm profile={profile} />
    </SettingsLayout>
  )
}

export default ProfileSettings
