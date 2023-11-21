import React from "react"
import PopupState, { bindTrigger } from "material-ui-popup-state"
import ProfileListItem from "./ProfileListItem"
import ProfileMenu from "./ProfileMenu"

export interface User {
  id: string
  username: string | null
  first_name: string
  last_name: string
}

type ProfileProps = {
  expanded: boolean
  profile?: User
}

const Profile: React.FC<ProfileProps> = ({ expanded, profile }) => {
  if (!profile) return <ProfileListItem expand={expanded} />

  const names = [profile.first_name, profile.last_name].filter(n => n !== "")

  const name = names.length > 0 ? names.join(" ") : "Profile"
  const initials = names.length > 0 ? names.map(name => name[0]).join("") : null

  return (
    <PopupState variant="popover" popupId="demo-popup-menu">
      {popupState => (
        <React.Fragment>
          <ProfileListItem
            {...bindTrigger(popupState)}
            expand={expanded}
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
