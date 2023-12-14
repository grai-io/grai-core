import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box, Grid, TextField, Typography } from "@mui/material"
import { useSnackbar } from "notistack"
import { clearWorkspace } from "helpers/cache"
import useWorkspace from "helpers/useWorkspace"
import FileUpload from "components/form/fields/FileUpload"
import Form from "components/form/Form"
import PageContent from "components/layout/PageContent"
import GraphError from "components/utils/GraphError"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import {
  UploadConnectorFile,
  UploadConnectorFileVariables,
} from "./__generated__/UploadConnectorFile"
import ConnectionToolbar from "./ConnectionToolbar"
import CreateConnectionHelp from "./CreateConnectionHelp"
import getAccept from "./getAccept"
import { ConnectorType } from "../ConnectionsForm"

export const UPLOAD_CONNECTOR_FILE = gql`
  mutation UploadConnectorFile(
    $workspaceId: ID!
    $connectorId: ID!
    $namespace: String!
    $file: Upload!
    $sourceName: String!
  ) {
    uploadConnectorFile(
      workspaceId: $workspaceId
      connectorId: $connectorId
      namespace: $namespace
      file: $file
      sourceName: $sourceName
    ) {
      id
      connection {
        id
        name
        connector {
          id
          name
        }
      }
      status
      metadata
      created_at
      updated_at
      started_at
      finished_at
      user {
        id
        username
        first_name
        last_name
      }
    }
  }
`

type Values = {
  file: File | null
  namespace: string
  sourceName: string
}

type ConnectionFileProps = {
  connector: ConnectorType
  workspaceId: string
}

const ConnectionFile: React.FC<ConnectionFileProps> = ({
  connector,
  workspaceId,
}) => {
  const { workspaceNavigate, routePrefix } = useWorkspace()
  const { enqueueSnackbar } = useSnackbar()

  const [values, setValues] = useState<Values>({
    file: null,
    namespace: "default",
    sourceName: connector.name,
  })

  const [uploadConnectorFile, { loading, error }] = useMutation<
    UploadConnectorFile,
    UploadConnectorFileVariables
  >(UPLOAD_CONNECTOR_FILE, {
    update(cache) {
      clearWorkspace(cache, workspaceId)
    },
  })

  const handleSubmit = () =>
    uploadConnectorFile({
      variables: {
        workspaceId,
        connectorId: connector.id,
        ...values,
      },
    })
      .then(res =>
        workspaceNavigate(`runs/${res.data?.uploadConnectorFile.id}`),
      )
      .then(() => enqueueSnackbar("File uploaded"))
      .catch(() => {})

  const connExtension = connector.metadata?.file?.extension

  const accept = getAccept(connExtension)

  return (
    <PageContent noPadding>
      <ConnectionToolbar
        title="Setup Connection"
        activeStep={1}
        onBack={`${routePrefix}/connections/create`}
      />
      <Box sx={{ px: 3 }}>
        <Form onSubmit={handleSubmit}>
          <WizardSubtitle subTitle="Choose a file to upload" />
          <Grid container sx={{ mt: 5 }}>
            <Grid item md={8} sx={{ pr: 3, mb: 3 }}>
              {error && <GraphError error={error} />}
              <TextField
                label="Source"
                margin="normal"
                value={values.sourceName}
                onChange={event =>
                  setValues({ ...values, sourceName: event.target.value })
                }
                required
                fullWidth
              />
              <TextField
                label="Namespace"
                margin="normal"
                value={values.namespace}
                onChange={event =>
                  setValues({ ...values, namespace: event.target.value })
                }
                required
                fullWidth
              />
              <Typography variant="body1" sx={{ mt: 3, mb: 2 }}>
                Select a {connector.metadata?.file?.name} file
              </Typography>
              <FileUpload
                value={values.file}
                onChange={file => setValues({ ...values, file })}
                accept={accept}
              />
              <Box sx={{ textAlign: "right", mt: 2 }}>
                <LoadingButton
                  variant="contained"
                  type="submit"
                  sx={{
                    minWidth: 120,
                    backgroundColor: "#FC6016",
                    boxShadow: "0px 4px 6px 0px rgba(252, 96, 22, 0.20)",
                  }}
                  disabled={!values.file}
                  loading={loading}
                >
                  Finish
                </LoadingButton>
              </Box>
            </Grid>
            <Grid item md={4} sx={{}}>
              <CreateConnectionHelp connector={connector} />
            </Grid>
          </Grid>
        </Form>
      </Box>
    </PageContent>
  )
}

export default ConnectionFile
