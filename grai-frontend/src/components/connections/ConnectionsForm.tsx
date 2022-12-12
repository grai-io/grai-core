import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { TextField, Typography } from "@mui/material"
import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import Connector, { ConnectorType } from "../form/fields/Connector"
import Namespace from "../form/fields/Namespace"
import Form from "../form/Form"
import ConnectionsMetadata from "./ConnectionsMetadata"

const CREATE_CONNECTION = gql`
  mutation Login(
    $connector: ID!
    $namespace: String
    $name: String!
    $metadata: JSON!
    $secrets: JSON!
  ) {
    createConnection(
      input: {
        connector: { set: $connector }
        namespace: $namespace
        name: $name
        metadata: $metadata
        secrets: $secrets
      }
    ) {
      __typename
      ... on OperationInfo {
        messages {
          kind
          message
          field
        }
      }
      ... on ConnectionType {
        id
        connector {
          id
          name
        }
        namespace
        name
        metadata
        isActive
        createdAt
        updatedAt
      }
    }
  }
`

type Values = {
  connector: ConnectorType | null
  namespace: string | null
  name: string
  metadata: any
  secrets: any
}

const ConnectionsForm: React.FC = () => {
  const navigate = useNavigate()

  const [values, setValues] = useState<Values>({
    connector: null,
    namespace: "",
    name: "",
    metadata: null,
    secrets: null,
  })

  const [createConnection, { loading, error }] = useMutation(CREATE_CONNECTION)

  const handleSubmit = () =>
    createConnection({
      variables: {
        connector: values.connector?.id,
        namespace: values.namespace,
        name: values.name,
        metadata: values.metadata,
        secrets: values.secrets,
      },
    }).then(data => navigate("/connections"))

  return (
    <Form onSubmit={handleSubmit}>
      {error && <Typography>{JSON.stringify(error)}</Typography>}
      <Connector
        value={values.connector}
        onChange={value => setValues({ ...values, connector: value })}
      />
      <Namespace
        value={values.namespace}
        onChange={value => setValues({ ...values, namespace: value })}
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
          onChangeMetadata={value => setValues({ ...values, metadata: value })}
          onChangeSecrets={value => setValues({ ...values, secrets: value })}
        />
      )}
      <LoadingButton
        variant="contained"
        type="submit"
        sx={{ mt: 2 }}
        loading={loading}
      >
        Save
      </LoadingButton>
    </Form>
  )
}

export default ConnectionsForm
