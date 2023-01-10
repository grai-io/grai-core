import { Grid, TextField } from "@mui/material"
import React from "react"
import ConnectionsMetadata from "../ConnectionsMetadata"
import CreateConnectionHelp from "./CreateConnectionHelp"
import { Values } from "./CreateConnectionWizard"

type SetupConnectionProps = {
  values: Values
  setValues: (values: Values) => void
}

const SetupConnection: React.FC<SetupConnectionProps> = ({
  values,
  setValues,
}) => {
  return (
    <Grid container sx={{ mt: 5 }}>
      <Grid item md={8} sx={{ pr: 3 }}>
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
        <TextField
          label="Name"
          margin="normal"
          value={values.name}
          onChange={event => setValues({ ...values, name: event.target.value })}
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
            onChangeSecrets={value => setValues({ ...values, secrets: value })}
          />
        )}
      </Grid>
      <Grid item md={4} sx={{}}>
        <CreateConnectionHelp />
      </Grid>
    </Grid>
  )
}

export default SetupConnection
