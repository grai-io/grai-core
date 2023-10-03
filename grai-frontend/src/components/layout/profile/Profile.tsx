import React from "react"
import { gql, useQuery } from "@apollo/client"
import PopupState, { bindTrigger } from "material-ui-popup-state"
import notEmpty from "helpers/notEmpty"
import GraphError from "components/utils/GraphError"
import { GetProfile } from "./__generated__/GetProfile"
import ProfileListItem from "./ProfileListItem"
import ProfileMenu from "./ProfileMenu"

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

type ProfileProps = {
  expand: boolean
}

const Profile: React.FC<ProfileProps> = ({ expand }) => {
  const { error, data } = useQuery<GetProfile>(GET_PROFILE)

  if (error) return <GraphError error={error} />

  const profile = data?.profile

  if (!profile) return <ProfileListItem expand={expand} />

  const names = [profile.first_name, profile.last_name].filter(notEmpty)

  const name = names.length > 0 ? names.join(" ") : "Profile"
  const initials = names.map(name => name[0]).join("")

  return (
    <PopupState variant="popover" popupId="demo-popup-menu">
      {popupState => (
        <React.Fragment>
          <ProfileListItem
            {...bindTrigger(popupState)}
            expand={expand}
            name={name}
            initials={initials}
          />
          <ProfileMenu popupState={popupState} />
        </React.Fragment>
      )}
    </PopupState>
  )
}

export default Profile
