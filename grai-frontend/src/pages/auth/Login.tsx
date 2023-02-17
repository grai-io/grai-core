import React from "react"
import { Box, Card, CardContent, Container, Typography } from "@mui/material"
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
  </Container>
)

export default Login
