import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Connections } from "components/icons"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import { GetConnectors } from "./__generated__/GetConnectors"
import ConnectorCategoryTabs from "./ConnectorCategoryTabs"
import ConnectorSearch from "./ConnectorSearch"
import { Connector } from "../connectors/ConnectorCard"
import ConnectorList from "../connectors/ConnectorList"

export const GET_CONNECTORS = gql`
  query GetConnectors {
    connectors(order: { priority: DESC, name: ASC }) {
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

type ConnectorSelectProps = {
  onSelect: (connector: Connector) => void
}

const ConnectorSelect: React.FC<ConnectorSelectProps> = ({ onSelect }) => {
  const [search, setSearch] = useState("")
  const [category, setCategory] = useState<string | null>(null)

  const { routePrefix } = useWorkspace()
  const { loading, error, data } = useQuery<GetConnectors>(GET_CONNECTORS)

  if (error) return <GraphError error={error} />
  if (loading || !data) return <Loading />

  const categories = data.connectors.reduce<string[]>((res, connector) => {
    const category = connector.category ?? "others"

    if (!res.includes(category)) {
      return res.concat(category)
    }

    return res
  }, [])

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
    category: "others",
  }

  const connectors = [...data.connectors, emptySource]
  const filteredConnectors = category
    ? connectors.filter(
        connector => (connector.category ?? "others") === category,
      )
    : connectors
  const searchedConnectors = search
    ? filteredConnectors.filter(connector =>
        connector.name.toLowerCase().includes(search.toLowerCase()),
      )
    : filteredConnectors

  return (
    <>
      <Box sx={{ display: "flex", my: 3 }}>
        <Box sx={{ flexGrow: 1 }}>
          <ConnectorCategoryTabs
            categories={categories}
            value={category}
            onChange={setCategory}
          />
        </Box>
        <ConnectorSearch value={search} onChange={setSearch} />
      </Box>
      <Box sx={{ mt: 5, pb: 5 }}>
        <ConnectorList connectors={searchedConnectors} onSelect={onSelect} />
      </Box>
    </>
  )
}

export default ConnectorSelect
