import React from "react"
import { Card, CardContent, Container, Typography } from "@mui/material"
import LoginForm from "../../components/auth/LoginForm"

const Login: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Typography variant="h6" sx={{ mb: 5, ml: 1 }}>
      Grai
    </Typography>
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" sx={{ mb: 1 }}>
          Sign in to your account
        </Typography>
        <LoginForm />
      </CardContent>
    </Card>
  </Container>
)

export default Login
