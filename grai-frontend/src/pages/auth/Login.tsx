import React from "react"
import {
  Box,
  Card,
  CardContent,
  Container,
  Link,
  Typography,
} from "@mui/material"
import { Link as RouterLink } from "react-router-dom"
import LoginForm from "components/auth/LoginForm"

const Login: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Box sx={{ mb: 3, ml: 1 }}>
      <img src="/images/grai-logo.svg" alt="Grai" />
    </Box>
    <Card elevation={3}>
      <CardContent sx={{ p: 5 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Sign in to your account
        </Typography>
        <LoginForm />
      </CardContent>
    </Card>
    <Box sx={{ display: "flex", ml: 2, mt: 2 }}>
      <Typography sx={{ mt: 0.8 }}>
        Don't have an account?{" "}
        <Link
          component={RouterLink}
          to="/register"
          sx={{
            textDecoration: "none",
            color: "blue",
            "&:hover": {
              color: theme => theme.palette.grey[900],
            },
          }}
        >
          Sign Up
        </Link>
      </Typography>
    </Box>
  </Container>
)

export default Login
