import React from "react"
import { Container, Box, Card, CardContent } from "@mui/material"
import CompleteSignupForm from "components/auth/CompleteSignupForm"
import GraiLogo from "components/icons/GraiLogo"

const CompleteSignup: React.FC = () => (
  <Container sx={{ pt: 10 }} maxWidth="xs">
    <Box sx={{ mb: 3, ml: 1 }}>
      <GraiLogo />
    </Box>
    <Card elevation={3}>
      <CardContent sx={{ p: 5 }}>
        <CompleteSignupForm />
      </CardContent>
    </Card>
  </Container>
)

export default CompleteSignup
