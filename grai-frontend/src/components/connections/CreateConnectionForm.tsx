import { gql, useMutation } from "@apollo/client"
import React from "react"
import { useNavigate } from "react-router-dom"
import ConnectionsForm, { Values } from "./ConnectionsForm"

const CREATE_CONNECTION = gql`
  mutation CreateConnection(
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

const CreateConnectionForm: React.FC = () => {
  const navigate = useNavigate()

  const [createConnection, { loading, error }] = useMutation(CREATE_CONNECTION)

  const handleSubmit = (values: Values) =>
    createConnection({
      variables: {
        connector: values.connector?.id,
        namespace: values.namespace,
        name: values.name,
        metadata: values.metadata,
        secrets: values.secrets,
      },
    }).then(data => navigate("/connections"))

  const defaultValues: Values = {
    connector: null,
    namespace: "",
    name: "",
    metadata: null,
    secrets: null,
  }

  return (
    <ConnectionsForm
      defaultValues={defaultValues}
      onSubmit={handleSubmit}
      loading={loading}
      error={error}
      chooseConnector
    />
  )
}

export default CreateConnectionForm
