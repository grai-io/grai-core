import React from "react"
import { gql, useQuery } from "@apollo/client"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import { GetConnectors } from "./__generated__/GetConnectors"
import { Connector } from "../connectors/ConnectorCard"
import ConnectorList from "../connectors/ConnectorList"

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

  return (
    <>
      {categories?.map(category => (
        <ConnectorList
          key={category.title}
          title={category.title}
          connectors={category.connectors}
          onSelect={onSelect}
        />
      ))}
    </>
  )
}

export default ConnectorSelect
