import React from "react"
import {
  Avatar,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material"

type ProfileListItemProps = {
  expand: boolean
  onClick?: (event: React.MouseEvent<Element, MouseEvent>) => void
  name?: string | null
  initials?: string | null
}

const ProfileListItem: React.FC<ProfileListItemProps> = ({
  expand,
  onClick,
  name,
  initials,
}) => (
  <ListItem disablePadding>
    <ListItemButton
      onClick={onClick}
      sx={{
        ":hover .child-icon": {
          color: "white",
          backgroundColor: "#3E546E",
        },
        ":hover .child-text": {
          color: "white",
        },
      }}
    >
      <ListItemIcon>
        <Avatar
          className="child-icon"
          sx={{
            bgcolor: "#324459",
            width: "40px",
            height: "40px",
            fontSize: "16px",
            ml: "4px",
            mr: "20px",
          }}
        >
          {initials}
        </Avatar>
      </ListItemIcon>
      {expand && (
        <ListItemText
          primary={name}
          primaryTypographyProps={{
            className: "child-text",
            sx: {
              fontWeight: 600,
              color: "#FFFFFF80",
            },
          }}
        />
      )}
    </ListItemButton>
  </ListItem>
)

export default ProfileListItem
