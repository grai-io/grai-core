import React from "react"
import { ArrowForward } from "@mui/icons-material"
import { Button, Grid, TextField } from "@mui/material"
import Form from "components/form/Form"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import ConnectionFile from "./ConnectionFile"
import CreateConnectionHelp from "./CreateConnectionHelp"
import { Values } from "./CreateConnectionWizard"
import ConnectionsMetadata from "../ConnectionsMetadata"

type SetupConnectionProps = {
  workspaceId: string
  opts: ElementOptions
  values: Values
  setValues: (values: Values) => void
}

const SetupConnection: React.FC<SetupConnectionProps> = ({
  workspaceId,
  opts,
  values,
  setValues,
}) => {
  if (values.connector?.metadata?.file?.name)
    return (
      <ConnectionFile
        connector={values.connector}
        workspaceId={workspaceId}
        opts={opts}
      />
    )

  return (
    <Form onSubmit={opts.forwardStep}>
      <WizardSubtitle
        title={`Connect to ${values.connector?.name}`}
        icon={values.connector?.icon}
      />
      <Grid container sx={{ mt: 5 }}>
        <Grid item md={8} sx={{ pr: 3 }}>
          <TextField
            label="Name"
            margin="normal"
            value={values.name}
            onChange={event =>
              setValues({ ...values, name: event.target.value })
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
          {values.connector && (
            <ConnectionsMetadata
              connector={values.connector}
              metadata={values.metadata}
              secrets={values.secrets}
              onChangeMetadata={value =>
                setValues({ ...values, metadata: value })
              }
              onChangeSecrets={value =>
                setValues({ ...values, secrets: value })
              }
            />
          )}
        </Grid>
        <Grid item md={4} sx={{}}>
          <CreateConnectionHelp connector={values.connector} />
        </Grid>
      </Grid>
      <WizardBottomBar opts={opts}>
        <Button
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          endIcon={<ArrowForward />}
        >
          Continue
        </Button>
      </WizardBottomBar>
    </Form>
  )
}

export default SetupConnection
