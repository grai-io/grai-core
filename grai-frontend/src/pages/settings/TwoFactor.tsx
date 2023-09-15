import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import NotFound from "pages/NotFound"
import SettingsLayout from "components/settings/SettingsLayout"
import TwoFactorHeader from "components/settings/twoFactor/TwoFactorHeader"
import TwoFactorTable from "components/settings/twoFactor/TwoFactorTable"
import GraphError from "components/utils/GraphError"
import { GetProfileTwoFactor } from "./__generated__/GetProfileTwoFactor"

export const GET_PROFILE = gql`
  query GetProfileTwoFactor {
    profile {
      id
      username
      first_name
      last_name
      devices {
        data {
          id
          name
        }
      }
    }
  }
`

const ProfileSettings: React.FC = () => {
  const { loading, error, data } = useQuery<GetProfileTwoFactor>(GET_PROFILE)

  if (error) return <GraphError error={error} />
  if (loading) return <SettingsLayout loading />

  const profile = data?.profile

  if (!profile) return <NotFound />

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <TwoFactorHeader />
        <TwoFactorTable keys={profile?.devices.data ?? []} loading={loading} />
      </Box>
    </SettingsLayout>
  )
}

export default ProfileSettings
