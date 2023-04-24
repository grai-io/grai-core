import React from "react"
import { Card, Link, Typography } from "@mui/material"
import { Link as RouterLink } from "react-router-dom"

const SignupLink: React.FC = () => (
  <Card
    elevation={0}
    sx={{
      pl: 2,
      mt: 2,
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
      }}
    >
      Don't have an account?{" "}
      <Link
        component={RouterLink}
        to="/register"
        sx={{
          textDecoration: "none",
          color: "#8338EC",
          "&:hover": {
            color: theme => theme.palette.grey[900],
          },
        }}
      >
        Sign Up
      </Link>
    </Typography>
  </Card>
)

export default SignupLink
