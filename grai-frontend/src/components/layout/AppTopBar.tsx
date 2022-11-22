import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material"
import React, { useContext } from "react"
import { Link } from "react-router-dom"
import AuthContext from "../auth/AuthContext"

const AppTopBar: React.FC = () => {
  const { logoutUser } = useContext(AuthContext)

  const handleLogout = () => logoutUser()

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          noWrap
          component={Link}
          to="/"
          sx={{
            mr: 2,
            fontWeight: 700,
            letterSpacing: ".3rem",
            color: "inherit",
            textDecoration: "none",
          }}
        >
          Grai
        </Typography>

        <Button component={Link} to="/nodes" sx={{ my: 2, color: "inherit" }}>
          Nodes
        </Button>
        <Button component={Link} to="/edges" sx={{ my: 2, color: "inherit" }}>
          Edges
        </Button>
        <Box sx={{ flexGrow: 1 }} />
        <Button color="inherit" onClick={handleLogout}>
          Logout
        </Button>
      </Toolbar>
    </AppBar>
  )
}

export default AppTopBar
