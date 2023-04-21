import React from "react"
import { Container, Box, Card, CardContent } from "@mui/material"
import { Link } from "react-router-dom"
import ResetPasswordForm from "components/auth/ResetPasswordForm"
import GraiLogo from "components/icons/GraiLogo"

const PasswordReset: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Box sx={{ mb: 3, ml: 1 }}>
      <GraiLogo />
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
