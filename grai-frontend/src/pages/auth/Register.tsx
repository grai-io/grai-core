import React from "react"
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Typography,
} from "@mui/material"
import { Link } from "react-router-dom"
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
      </CardContent>
    </Card>
    <Box sx={{ display: "flex", ml: 2, mt: 2 }}>
      <Typography sx={{ mt: 0.8 }}>Already have an account?</Typography>
      <Button component={Link} to="/login">
        Login
      </Button>
    </Box>
  </Container>
)

export default Register
