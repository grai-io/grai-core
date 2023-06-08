import React from "react"
import { Container, Card, CardContent, Typography } from "@mui/material"
import { GraiLogo } from "components/icons"
import WorkspaceForm from "components/workspaces/WorkspaceForm"

const WorkspaceCreate: React.FC = () => (
  <Container maxWidth="sm" sx={{ mt: 20 }}>
    <GraiLogo />
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

export default WorkspaceCreate
