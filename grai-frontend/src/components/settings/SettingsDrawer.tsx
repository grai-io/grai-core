import React from "react"
import { Drawer, Typography } from "@mui/material"
import PersonalInfo from "components/icons/PersonalInfo"
import TwoFactor from "components/icons/TwoFactor"
import ApiKeys from "components/icons/ApiKeys"
import Workspace from "components/icons/Workspace"
import Users from "components/icons/Users"
import Alerts from "components/icons/Alerts"
import Installations from "components/icons/Installations"
import SettingsDrawerSection, { Page } from "./SettingsDrawerSection"

const drawerWidth = 300

const profilePages: Page[] = [
  {
    name: "Personal info",
    icon: <PersonalInfo />,
    path: "/settings/profile",
  },
  {
    name: "2 Factor",
    icon: <TwoFactor />,
    path: "/settings/2fa",
  },
  {
    name: "API Keys",
    icon: <ApiKeys />,
    path: "/settings/api-keys",
  },
]

const workspacePages: Page[] = [
  {
    name: "Settings",
    icon: <Workspace />,
    path: "/settings/workspace",
  },
  {
    name: "Users",
    icon: <Users />,
    path: "/settings/memberships",
  },
  {
    name: "Alerts",
    icon: <Alerts />,
    path: "/settings/alerts",
  },
  {
    name: "Installations",
    icon: <Installations />,
    path: "/settings/installations",
  },
]

const SettingsDrawer: React.FC = () => (
  <Drawer
    variant="permanent"
    sx={{
      width: drawerWidth,
      "& .MuiDrawer-paper": {
        marginLeft: "76px",
        width: drawerWidth,
        boxSizing: "border-box",
        backgroundColor: "#F8F8F8",
      },
    }}
  >
    <Typography
      variant="h1"
      sx={{
        pl: "24px",
        pt: "32px",
        color: "rgba(0, 0, 0, 0.80)",
        fontSize: "18px",
        fontWeight: 700,
      }}
    >
      Settings
    </Typography>
    <SettingsDrawerSection
      title="Profile"
      pages={profilePages}
      sx={{ pt: 2 }}
    />
    <SettingsDrawerSection
      title="Workspace"
      pages={workspacePages}
      sx={{ pt: "36px" }}
    />
  </Drawer>
)

export default SettingsDrawer
