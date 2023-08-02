import React from "react"
import { gql, useQuery } from "@apollo/client"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import { GetConnectors } from "./__generated__/GetConnectors"
import { Connector } from "../connectors/ConnectorCard"
import ConnectorList from "../connectors/ConnectorList"
import { Connections } from "components/icons"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"

export const GET_CONNECTORS = gql`
  query GetConnectors {
    connectors(order: { name: ASC }) {
      id
      name
      metadata
      icon
      category
      coming_soon
    }
  }
`

type Category = {
  title: string
  connectors: Connector[]
}

type ConnectorSelectProps = {
  onSelect: (connector: Connector) => void
}

const ConnectorSelect: React.FC<ConnectorSelectProps> = ({ onSelect }) => {
  const { routePrefix } = useWorkspace()
  const { loading, error, data } = useQuery<GetConnectors>(GET_CONNECTORS)

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const categories = data?.connectors.reduce<Category[]>((res, connector) => {
    const category = connector.category ?? "other"

    const group = res.find(g => g.title === category)

    if (group) {
      group.connectors.push(connector)
    } else {
      const newCategory = {
        title: category,
        connectors: [connector],
      }

      return res.concat(newCategory)
    }

    return res
  }, [])

  const databases = categories?.find(c => c.title === "databases")
  const datatools = categories?.find(c => c.title === "data tools")
  const others = categories?.filter(
    c => !["databases", "data tools"].includes(c.title),
  )

  const emptySource = {
    id: "source",
    name: "Empty Source",
    metadata: null,
    icon: (
      <Box sx={{ m: -3, ml: -1 }}>
        <Connections stroke="black" />
      </Box>
    ),
    to: `${routePrefix}/sources/create`,
  }

  return (
    <>
      {databases && (
        <ConnectorList
          title={databases.title}
          connectors={databases.connectors}
          onSelect={onSelect}
        />
      )}
      {datatools && (
        <ConnectorList
          title={datatools.title}
          connectors={datatools.connectors}
          onSelect={onSelect}
        />
      )}
      {others?.map(category => (
        <ConnectorList
          key={category.title}
          title={category.title}
          connectors={
            category.title === "other"
              ? [...category.connectors, emptySource]
              : category.connectors
          }
          onSelect={onSelect}
        />
      ))}
    </>
  )
}

export default ConnectorSelect
