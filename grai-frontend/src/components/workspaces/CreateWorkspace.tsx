import React from "react"
import { Card, CardContent, Container, Typography } from "@mui/material"
import WorkspaceForm from "./WorkspaceForm"

const CreateWorkspace: React.FC = () => {
  return (
    <Container maxWidth="sm" sx={{ mt: 20 }}>
      <img src="/images/grai-logo.svg" alt="Grai" />
      <Card elevation={3} sx={{ mt: 2 }}>
        <CardContent sx={{ p: 5 }}>
          <Typography variant="h6" sx={{ mb: 1 }}>
            Create a workspace
          </Typography>
          <WorkspaceForm />
        </CardContent>
      </Card>
    </Container>
  )
}

export default CreateWorkspace
