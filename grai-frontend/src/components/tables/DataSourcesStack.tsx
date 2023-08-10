import { Stack } from "@mui/material"
import DataSourceIcon from "components/graph/DataSourceIcon"

interface Connector {
  slug: string | null
}

interface Connection {
  id: string
  connector: Connector
}

export interface Source {
  id: string
  name: string
  connections: { data: Connection[] }
}

type DataSourcesStackProps = {
  data_sources: { data: Source[] }
}

const DataSourcesStack: React.FC<DataSourcesStackProps> = ({
  data_sources,
}) => (
  <Stack direction="row" spacing={1}>
    {data_sources?.data?.map(
      source =>
        source.connections.data[0].connector.slug && (
          // <Tooltip title={source.name} key={source.name}>
          <DataSourceIcon
            key={source.name}
            dataSource={`grai-source-${source.connections.data[0].connector.slug}`}
            noMargin
            noBorder
          />
          // </Tooltip>
        ),
    )}
  </Stack>
)

export default DataSourcesStack
