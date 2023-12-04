import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetConnector,
  GetConnectorVariables,
} from "./__generated__/GetConnector"
import SetupConnection from "./SetupConnection"

export const GET_CONNECTOR = gql`
  query GetConnector($connectorId: ID!) {
    connector(id: $connectorId) {
      id
      priority
      name
      metadata
      icon
      category
      status
    }
  }
`

type SetupConnectionTabProps = {
  workspaceId: string
  connectorId: string
}

const SetupConnectionTab: React.FC<SetupConnectionTabProps> = ({
  workspaceId,
  connectorId,
}) => {
  const { loading, error, data } = useQuery<
    GetConnector,
    GetConnectorVariables
  >(GET_CONNECTOR, {
    variables: {
      connectorId,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const connector = data?.connector

  if (!connector) return <NotFound />

  return (
    <SetupConnection
      workspaceId={workspaceId}
      connector={connector}
      connection={null}
    />
  )
}

export default SetupConnectionTab
