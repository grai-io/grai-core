import React from "react"
import { Card, CardContent, Container, Typography } from "@mui/material"
import GraiLogo from "components/icons/GraiLogo"
import WorkspaceForm from "./WorkspaceForm"

const CreateWorkspace: React.FC = () => {
  return (
    <Container maxWidth="sm" sx={{ mt: 20 }}>
      <GraiLogo />
      <Card elevation={3} sx={{ mt: 2 }}>
        <CardContent sx={{ p: 5 }}>
          <Typography variant="h6" sx={{ mb: 1 }}>
            Create an organisation
          </Typography>
          <WorkspaceForm />
        </CardContent>
      </Card>
    </Container>
  )
}

export default CreateWorkspace
