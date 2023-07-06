import React from "react"
import { Card, Link, Typography } from "@mui/material"
import { Link as RouterLink } from "react-router-dom"

const LoginLink: React.FC = () => (
  <Card
    elevation={0}
    sx={{
      pl: 2,
      mt: 2,
      mb: 10,
      height: "72px",
      backgroundColor: "transparent",
      borderRadius: "20px",
      borderColor: "#3A86FF12",
      borderWidth: "2px",
      borderStyle: "solid",
    }}
  >
    <Typography
      sx={{
        textAlign: "center",
        lineHeight: "70px",
        fontSize: "18px",
        fontWeight: "semibold",
        zIndex: 2,
      }}
    >
      Already have an account?{" "}
      <Link
        component={RouterLink}
        to="/login"
        sx={{
          textDecoration: "none",
          color: "#8338EC",
          "&:hover": {
            color: theme => theme.palette.grey[900],
          },
        }}
      >
        Sign In
      </Link>
    </Typography>
  </Card>
)

export default LoginLink
