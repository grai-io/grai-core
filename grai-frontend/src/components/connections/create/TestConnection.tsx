import React, { useEffect, useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { ArrowForward } from "@mui/icons-material"
import { Grid, Button } from "@mui/material"
import GraphError from "components/utils/GraphError"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import {
  ValidateConnection,
  ValidateConnectionVariables,
} from "./__generated__/ValidateConnection"
import CreateConnectionHelp from "./CreateConnectionHelp"
import { Connection } from "./CreateConnectionWizard"
import ValidationRun from "./ValidationRun"
import { Connector } from "../connectors/ConnectorCard"

export const CREATE_RUN = gql`
  mutation ValidateConnection($connectionId: ID!) {
    runConnection(connectionId: $connectionId, action: "validate") {
      id
    }
  }
`

interface Run {
  id: string
}

type TestConnectionProps = {
  workspaceId: string
  opts: ElementOptions
  connector: Connector
  connection: Connection
}

const TestConnection: React.FC<TestConnectionProps> = ({
  workspaceId,
  opts,
  connector,
  connection,
}) => {
  const [run, setRun] = useState<Run | null>(null)

  const [createRun, { error }] = useMutation<
    ValidateConnection,
    ValidateConnectionVariables
  >(CREATE_RUN)

  useEffect(() => {
    createRun({
      variables: {
        connectionId: connection.id,
      },
    }).then(data => data.data?.runConnection && setRun(data.data.runConnection))
  }, [connection, createRun])

  return (
    <>
      <WizardSubtitle
        title={`Test connection to ${connector?.name}`}
        icon={connector?.icon}
      />
      {run ? (
        <ValidationRun
          workspaceId={workspaceId}
          run={run}
          connector={connector}
          opts={opts}
        />
      ) : (
        <>
          <Grid container sx={{ mt: 5 }}>
            <Grid item md={8} sx={{ pr: 3 }}>
              {error && <GraphError error={error} />}
            </Grid>
            <Grid item md={4} sx={{}}>
              <CreateConnectionHelp connector={connector} />
            </Grid>
          </Grid>
          <WizardBottomBar opts={opts}>
            <Button
              variant="contained"
              type="submit"
              sx={{ minWidth: 120, color: "white" }}
              endIcon={<ArrowForward />}
              disabled
            >
              Continue
            </Button>
          </WizardBottomBar>
        </>
      )}
    </>
  )
}

export default TestConnection
