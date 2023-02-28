import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Grid, TextField, Typography } from "@mui/material"
import { clearWorkspace } from "helpers/cache"
import useWorkspace from "helpers/useWorkspace"
import { useSnackbar } from "notistack"
import { Accept } from "react-dropzone"
import FileUpload from "components/form/FileUpload"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import {
  UploadConnectorFile,
  UploadConnectorFileVariables,
} from "./__generated__/UploadConnectorFile"
import CreateConnectionHelp from "./CreateConnectionHelp"
import { ConnectorType } from "../ConnectionsForm"

export const UPLOAD_CONNECTOR_FILE = gql`
  mutation UploadConnectorFile(
    $workspaceId: ID!
    $connectorId: ID!
    $namespace: String!
    $file: Upload!
  ) {
    uploadConnectorFile(
      workspaceId: $workspaceId
      connectorId: $connectorId
      namespace: $namespace
      file: $file
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
}

type ConnectionFileProps = {
  connector: ConnectorType
  workspaceId: string
  opts: ElementOptions
}

const ConnectionFile: React.FC<ConnectionFileProps> = ({
  connector,
  workspaceId,
  opts,
}) => {
  const { workspaceNavigate } = useWorkspace()
  const { enqueueSnackbar } = useSnackbar()

  const [values, setValues] = useState<Values>({
    file: null,
    namespace: "default",
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
        workspaceNavigate(`runs/${res.data?.uploadConnectorFile.id}`)
      )
      .then(() => enqueueSnackbar("File uploaded"))

  const accept: Accept =
    connector.metadata?.file?.extension === "json"
      ? {
          "application/json": [".json"],
        }
      : {
          "application/yaml": [".yaml", ".yml"],
        }

  return (
    <Form onSubmit={handleSubmit}>
      <WizardSubtitle
        title={`Connect to ${connector?.name}`}
        icon={connector?.icon}
      />
      <Grid container sx={{ mt: 5 }}>
        <Grid item md={8} sx={{ pr: 3 }}>
          {error && <GraphError error={error} />}
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
        </Grid>
        <Grid item md={4} sx={{}}>
          <CreateConnectionHelp connector={connector} />
        </Grid>
      </Grid>
      <WizardBottomBar opts={opts}>
        <LoadingButton
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          disabled={!values.file}
          loading={loading}
        >
          Finish
        </LoadingButton>
      </WizardBottomBar>
    </Form>
  )
}

export default ConnectionFile
