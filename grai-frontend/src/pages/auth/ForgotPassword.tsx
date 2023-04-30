import React from "react"
import { Container, Box, Card, CardContent } from "@mui/material"
import { Link } from "react-router-dom"
import RequestPasswordResetForm from "components/auth/RequestPasswordResetForm"
import GraiLogo from "components/icons/GraiLogo"

const ForgotPassword: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Box sx={{ mb: 3, ml: 1 }}>
      <GraiLogo />
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
