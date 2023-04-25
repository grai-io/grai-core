import React from "react"
import { Box } from "@mui/material"

type DataSourceIconProps = {
  dataSource: string
}

interface Icons {
  [key: string]: string
}

const icons: Icons = {
  "grai-source-dbt": "/icons/data-sources/dbt.png",
  "grai-source-postgres": "/icons/data-sources/postgres.png",
  "grai-source-snowflake": "/icons/data-sources/snowflake.png",
  "grai-source-mssql": "/icons/data-sources/mssql.png",
  "grai-source-bigquery": "/icons/data-sources/bigquery.png",
  "grai-source-mysql": "/icons/data-sources/mysql.png",
  "grai-source-redshift": "/icons/data-sources/redshift.png",
}

const DataSourceIcon: React.FC<DataSourceIconProps> = ({ dataSource }) => {
  const icon = icons[dataSource]

  if (!icon) return null

  return (
    <Box sx={{ pt: 0.75, pr: 1 }}>
      <img
        src={icon}
        alt={`${dataSource} logo`}
        style={{ height: 20, width: 20 }}
      />
    </Box>
  )
}

export default DataSourceIcon
