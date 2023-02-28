import React from "react"
import { Container, Box, Card, CardContent } from "@mui/material"
import CompleteSignupForm from "components/auth/CompleteSignupForm"

const CompleteSignup: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Box sx={{ mb: 3, ml: 1 }}>
      <img src="/images/grai-logo.svg" alt="Grai" />
    </Box>
    <Card elevation={3}>
      <CardContent sx={{ p: 5 }}>
        <CompleteSignupForm />
      </CardContent>
    </Card>
  </Container>
)

export default CompleteSignup
