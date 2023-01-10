import { gql, useMutation } from "@apollo/client"
import { ArrowForward } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import { Box, Button, Typography } from "@mui/material"
import WizardLayout, { WizardSteps } from "components/wizards/WizardLayout"
import React, { useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { ConnectorType } from "../ConnectionsForm"
import {
  CreateConnection,
  CreateConnectionVariables,
} from "../__generated__/CreateConnection"
import ConnectorSelect from "./ConnectorSelect"
import SetSchedule from "./SetSchedule"
import SetupConnection from "./SetupConnection"
import TestConnection from "./TestConnection"

export const CREATE_CONNECTION = gql`
  mutation CreateConnection(
    $workspaceId: ID!
    $connectorId: ID!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON
    $schedules: JSON
    $is_active: Boolean
  ) {
    createConnection(
      workspaceId: $workspaceId
      connectorId: $connectorId
      namespace: $namespace
      name: $name
      metadata: $metadata
      secrets: $secrets
      schedules: $schedules
      is_active: $is_active
    ) {
      id
      connector {
        id
        name
      }
      namespace
      name
      metadata
      is_active
      created_at
      updated_at
    }
  }
`

export type CronValue = {
  minutes: string
  hours: string
  day_of_week: string
  day_of_month: string
  month_of_year: string
}

type SchedulesValues = {
  type: string | null
  cron?: CronValue
}

export type Values = {
  connector: ConnectorType | null
  namespace: string
  name: string
  metadata: any
  secrets: any
  schedules: SchedulesValues | null
}

const CreateConnectionWizard: React.FC = () => {
  const { workspaceId } = useParams()
  const navigate = useNavigate()

  const [createConnection, { loading, error }] = useMutation<
    CreateConnection,
    CreateConnectionVariables
  >(CREATE_CONNECTION)

  const defaultValues: Values = {
    connector: null,
    namespace: "",
    name: "",
    metadata: null,
    secrets: null,
    schedules: null,
  }

  const [values, setValues] = useState<Values>(defaultValues)

  const handleSubmit = () =>
    createConnection({
      variables: {
        workspaceId: workspaceId ?? "",
        connectorId: values.connector?.id ?? "",
        namespace: values.namespace,
        name: values.name,
        metadata: values.metadata,
        secrets: values.secrets,
        schedules: values.schedules,
        is_active: true,
      },
    })
      .then(res =>
        navigate(
          `/workspaces/${workspaceId}/connections/${res.data?.createConnection.id}`
        )
      )
      .catch(() => {})

  const handleSelect = (setActiveStep: (step: number) => void) => {
    setValues({
      ...values,
      connector: {
        id: "768aea48-1146-4f14-9005-40e89504f4b3",
        name: "Postgres",
        metadata: {
          fields: [
            {
              name: "dbname",
              label: "Database Name",
              required: true,
            },
            {
              name: "user",
              required: true,
            },
            {
              name: "password",
              secret: true,
              required: true,
            },
            {
              name: "host",
              required: true,
            },
            {
              name: "port",
              default: 5432,
              required: true,
            },
          ],
        },
      },
    })
    setActiveStep(1)
  }

  const steps: WizardSteps = [
    {
      title: "Select connector",
      subTitle: "Select a connector",
      actionText: "Click on a connector to continue",
      element: ({ setActiveStep }) => (
        <ConnectorSelect onSelect={() => handleSelect(setActiveStep)} />
      ),
    },
    {
      title: "Setup connection",
      subTitle: (
        <Box sx={{ display: "flex" }}>
          <img
            src="https://cdn.sanity.io/images/pwmfmi47/production/245cb2ccbc976d6dc38d90456ca1fd7cdbcb2dc6-2424x2500.svg"
            alt="PostgreSQL logo"
            style={{ height: 28, width: 28 }}
          />
          <Typography variant="h5" sx={{ ml: 2 }}>
            Connect to PostgreSQL
          </Typography>
        </Box>
      ),
      element: <SetupConnection values={values} setValues={setValues} />,
      actionButtons: opts => (
        <Button
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          endIcon={<ArrowForward />}
          onClick={opts.forwardStep}
        >
          Continue
        </Button>
      ),
    },
    {
      title: "Test connection",
      subTitle: (
        <Box sx={{ display: "flex" }}>
          <img
            src="https://cdn.sanity.io/images/pwmfmi47/production/245cb2ccbc976d6dc38d90456ca1fd7cdbcb2dc6-2424x2500.svg"
            alt="PostgreSQL logo"
            style={{ height: 28, width: 28 }}
          />
          <Typography variant="h5" sx={{ ml: 2 }}>
            Test connection to PostgreSQL
          </Typography>
        </Box>
      ),
      element: <TestConnection />,
      actionButtons: opts => (
        <Button
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          endIcon={<ArrowForward />}
          onClick={opts.forwardStep}
        >
          Continue
        </Button>
      ),
    },
    {
      title: "Set schedule",
      subTitle: "Set a schedule for this connection",
      element: (
        <SetSchedule values={values} setValues={setValues} error={error} />
      ),
      actionButtons: (
        <LoadingButton
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          loading={loading}
          onClick={handleSubmit}
        >
          Finish
        </LoadingButton>
      ),
    },
  ]

  return (
    <WizardLayout
      title="Create Connection"
      steps={steps}
      closeRoute={workspaceId => `/workspaces/${workspaceId}/connections`}
    />
  )
}

export default CreateConnectionWizard
