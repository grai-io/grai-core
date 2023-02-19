import { Container, Box, Card, CardContent } from "@mui/material"
import ResetPasswordForm from "components/auth/ResetPasswordForm"
import React from "react"
import { Link } from "react-router-dom"

const PasswordReset: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Box sx={{ mb: 3, ml: 1 }}>
      <img src="/images/grai-logo.svg" alt="Grai" />
    </Box>
    <Card elevation={3}>
      <CardContent sx={{ p: 5 }}>
        <ResetPasswordForm />
        <Box sx={{ m: 1, textAlign: "center" }}>
          <Link to="/login" style={{ textDecoration: "none", fontSize: 14 }}>
            Return to sign in
          </Link>
        </Box>
      </CardContent>
    </Card>
  </Container>
)

export default PasswordReset
