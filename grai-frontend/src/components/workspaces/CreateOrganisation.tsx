import React from "react"
import { Card, CardContent, Container, Typography } from "@mui/material"
import GraiLogo from "components/icons/GraiLogo"
import OrganisationForm from "./OrganisationForm"

const CreateOrganisation: React.FC = () => (
  <Container maxWidth="sm" sx={{ mt: 20 }}>
    <GraiLogo />
    <Card elevation={3} sx={{ mt: 2 }}>
      <CardContent sx={{ p: 5 }}>
        <Typography variant="h6" sx={{ mb: 1 }}>
          Create an organisation
        </Typography>
        <OrganisationForm />
      </CardContent>
    </Card>
  </Container>
)

export default CreateOrganisation
