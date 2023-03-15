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
import RegisterForm from "components/auth/RegisterForm"

const Register: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Box sx={{ mb: 3, ml: 1 }}>
      <img src="/images/grai-logo.svg" alt="Grai" />
    </Box>
    <Card elevation={3}>
      <CardContent sx={{ p: 5 }}>
        <Typography variant="h6" sx={{ mb: 1 }}>
          Register for an account
        </Typography>
        <RegisterForm />
        <Typography
          variant="body2"
          sx={{ color: theme => theme.palette.grey[600], lineHeight: 1.5 }}
        >
          By creating an account, you agree to our{" "}
          <Link
            href="https://www.grai.io/terms"
            sx={{
              textDecoration: "none",
              color: theme => theme.palette.grey[900],
              "&:hover": {
                textDecoration: "underline",
              },
            }}
            target="_blank"
          >
            Terms of Service
          </Link>{" "}
          and{" "}
          <Link
            href="https://www.grai.io/privacy"
            sx={{
              textDecoration: "none",
              color: theme => theme.palette.grey[900],
              "&:hover": {
                textDecoration: "underline",
              },
            }}
            target="_blank"
          >
            Privacy Policy
          </Link>
          .
        </Typography>
      </CardContent>
    </Card>
    <Box sx={{ display: "flex", ml: 2, mt: 2 }}>
      <Typography sx={{ mt: 0.8 }}>
        Already have an account?{" "}
        <Link
          component={RouterLink}
          to="/login"
          sx={{
            textDecoration: "none",
            color: "blue",
            "&:hover": {
              color: theme => theme.palette.grey[900],
            },
          }}
        >
          Login
        </Link>
      </Typography>
    </Box>
  </Container>
)

export default Register
