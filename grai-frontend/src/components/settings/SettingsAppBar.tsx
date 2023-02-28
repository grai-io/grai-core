import React from "react"
import { Close } from "@mui/icons-material"
import { AppBar, IconButton, Toolbar, Typography } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { useNavigate } from "react-router-dom"

const SettingsAppBar: React.FC = () => {
  const { routePrefix } = useWorkspace()
  const navigate = useNavigate()

  const handleClose = () => navigate(routePrefix)

  return (
    <AppBar
      position="fixed"
      color="transparent"
      elevation={0}
      sx={{
        borderBottomStyle: "solid",
        borderBottomWidth: 1,
        borderBottomColor: "divider",
        zIndex: theme => theme.zIndex.drawer + 1,
        backgroundColor: "white",
      }}
    >
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Settings
        </Typography>
        <IconButton onClick={handleClose}>
          <Close />
        </IconButton>
      </Toolbar>
    </AppBar>
  )
}

export default SettingsAppBar
