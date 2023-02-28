import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import useWorkspace from "helpers/useWorkspace"
import { useSnackbar } from "notistack"
import WizardLayout, { WizardSteps } from "components/wizards/WizardLayout"
import {
  CreateConnection,
  CreateConnectionVariables,
} from "./__generated__/CreateConnection"
import { NewConnection } from "./__generated__/NewConnection"
import ConnectorSelectTab from "./ConnectorSelectTab"
import SetSchedule from "./SetSchedule"
import SetupConnection from "./SetupConnection"
import TestConnection from "./TestConnection"
import { ConnectorType } from "../ConnectionsForm"
import { Connector } from "../connectors/ConnectorCard"

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

export type SchedulesValues = {
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

type CreateConnectionWizardProps = {
  workspaceId: string
}

const CreateConnectionWizard: React.FC<CreateConnectionWizardProps> = ({
  workspaceId,
}) => {
  const { workspaceNavigate } = useWorkspace()
  const { enqueueSnackbar } = useSnackbar()

  const [createConnection, { loading, error }] = useMutation<
    CreateConnection,
    CreateConnectionVariables
  >(CREATE_CONNECTION, {
    update(cache, { data }) {
      cache.modify({
        id: cache.identify({
          id: workspaceId,
          __typename: "Workspace",
        }),
        fields: {
          connections(existingConnections = []) {
            if (!data?.createConnection) return

            const newConnection = cache.writeFragment<NewConnection>({
              data: data.createConnection,
              fragment: gql`
                fragment NewConnection on Connection {
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
              `,
            })
            return [...existingConnections, newConnection]
          },
        },
      })
    },
  })

  const defaultValues: Values = {
    connector: null,
    namespace: "default",
    name: "",
    metadata: null,
    secrets: null,
    schedules: null,
  }

  const [values, setValues] = useState<Values>(defaultValues)

  const handleSubmit = () => {
    createConnection({
      variables: {
        workspaceId,
        connectorId: values.connector?.id as string,
        namespace: values.namespace,
        name: values.name,
        metadata: values.metadata,
        secrets: values.secrets,
        schedules: values.schedules,
        is_active: true,
      },
    })
      .then(res =>
        workspaceNavigate(`connections/${res.data?.createConnection.id}`)
      )
      .then(() => enqueueSnackbar("Connection created"))
      .catch(() => {})
  }

  const handleSelect =
    (setActiveStep: (step: number) => void) => (connector: Connector) => {
      setValues({
        ...values,
        connector,
        name: connector.name,
      })
      setActiveStep(1)
    }

  const steps: WizardSteps = [
    {
      title: "Select connector",
      element: opts => (
        <ConnectorSelectTab
          opts={opts}
          onSelect={handleSelect(opts.setActiveStep)}
        />
      ),
    },
    {
      title: "Setup connection",
      element: opts => (
        <SetupConnection
          workspaceId={workspaceId}
          opts={opts}
          values={values}
          setValues={setValues}
        />
      ),
    },
    {
      title: "Test connection",
      element: opts => <TestConnection opts={opts} values={values} />,
    },
    {
      title: "Set schedule",
      element: opts => (
        <SetSchedule
          opts={opts}
          values={values}
          setValues={setValues}
          error={error}
          loading={loading}
          onSubmit={handleSubmit}
        />
      ),
    },
  ]

  return (
    <WizardLayout
      title="Create Connection"
      steps={steps}
      onClose={() => workspaceNavigate("connections")}
    />
  )
}

export default CreateConnectionWizard
