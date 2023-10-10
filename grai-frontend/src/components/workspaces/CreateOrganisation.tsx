import React, { useState } from "react"
import { Card, CardContent, Container, Typography } from "@mui/material"
import GraiLogo from "components/icons/GraiLogo"
import CreateSampleData from "./CreateSampleData"
import OrganisationForm from "./OrganisationForm"

export interface Workspace {
  id: string
  name: string
  organisation: {
    id: string
    name: string
  }
}

const CreateOrganisation: React.FC = () => {
  const [workspace, setWorkspace] = useState<Workspace>()

  if (workspace) {
    return <CreateSampleData workspace={workspace} />
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 20 }}>
      <GraiLogo />
      <Card elevation={3} sx={{ mt: 2 }}>
        <CardContent sx={{ p: 5 }}>
          <Typography variant="h6" sx={{ mb: 1 }}>
            Create an organisation
          </Typography>
          <OrganisationForm onCreate={setWorkspace} />
        </CardContent>
      </Card>
    </Container>
  )
}

export default CreateOrganisation
