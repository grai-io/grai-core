import React, { useEffect } from "react"
import { gql, useMutation } from "@apollo/client"
import {
  Card,
  CardContent,
  CircularProgress,
  Container,
  Typography,
} from "@mui/material"
import { useSnackbar } from "notistack"
import { useNavigate } from "react-router-dom"
import { GraiLogo } from "components/icons"
import GraphError from "components/utils/GraphError"
import {
  LoadWorkspaceSampleData,
  LoadWorkspaceSampleDataVariables,
} from "./__generated__/LoadWorkspaceSampleData"
import { Workspace } from "./CreateOrganisation"

export const LOAD_WORKSPACE_SAMPLE_DATA = gql`
  mutation LoadWorkspaceSampleData($id: ID!) {
    loadWorkspaceSampleData(id: $id) {
      id
      name
      organisation {
        id
        name
      }
    }
  }
`

type CreateSampleDataProps = {
  workspace: Workspace
}

const CreateSampleData: React.FC<CreateSampleDataProps> = ({ workspace }) => {
  const navigate = useNavigate()
  const { enqueueSnackbar } = useSnackbar()

  const [loadWorkspaceSampleData, { loading, error }] = useMutation<
    LoadWorkspaceSampleData,
    LoadWorkspaceSampleDataVariables
  >(LOAD_WORKSPACE_SAMPLE_DATA, {
    variables: {
      id: workspace.id,
    },
  })

  useEffect(() => {
    loadWorkspaceSampleData()
      .then(() => navigate(`/${workspace.organisation.name}/${workspace.name}`))
      .then(() => enqueueSnackbar("Workspace created"))
      .catch(() => {})
  }, [loadWorkspaceSampleData, enqueueSnackbar, navigate, workspace])

  return (
    <Container maxWidth="sm" sx={{ mt: 20 }}>
      <GraiLogo />
      <Card elevation={3} sx={{ mt: 2 }}>
        <CardContent sx={{ p: 5, textAlign: "center" }}>
          <Typography variant="h6" sx={{ mb: 5 }}>
            Your workspace will be ready very soon
          </Typography>
          <Typography variant="body1">Generating sample data</Typography>
          {error && <GraphError error={error} />}
          {loading && <CircularProgress sx={{ my: 5 }} />}
        </CardContent>
      </Card>
    </Container>
  )
}

export default CreateSampleData
