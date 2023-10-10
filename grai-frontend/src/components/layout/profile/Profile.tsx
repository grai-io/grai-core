import React from "react"
import PopupState, { bindTrigger } from "material-ui-popup-state"
import notEmpty from "helpers/notEmpty"
import ProfileListItem from "./ProfileListItem"
import ProfileMenu from "./ProfileMenu"

export interface User {
  id: string
  username: string | null
  first_name: string
  last_name: string
}

type ProfileProps = {
  expand: boolean
  profile?: User
}

const Profile: React.FC<ProfileProps> = ({ expand, profile }) => {
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
