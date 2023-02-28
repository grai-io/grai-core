import React from "react"
import { Container, Box, Card, CardContent } from "@mui/material"
import { Link } from "react-router-dom"
import RequestPasswordResetForm from "components/auth/RequestPasswordResetForm"

const ForgotPassword: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Box sx={{ mb: 3, ml: 1 }}>
      <img src="/images/grai-logo.svg" alt="Grai" />
    </Box>
    <Card elevation={3}>
      <CardContent sx={{ p: 5 }}>
        <RequestPasswordResetForm />
        <Box sx={{ m: 1, textAlign: "center" }}>
          <Link to="/login" style={{ textDecoration: "none", fontSize: 14 }}>
            Return to sign in
          </Link>
        </Box>
      </CardContent>
    </Card>
  </Container>
)

export default ForgotPassword
