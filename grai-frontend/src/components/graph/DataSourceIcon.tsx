import React from "react"
import { Box } from "@mui/material"

type DataSourceIconProps = {
  dataSource: string
}

interface Icons {
  [key: string]: string
}

const icons: Icons = {
  "grai-source-dbt": "/images/dbt-logo.png",
  "grai-source-postgres": "/images/postgres-logo.svg",
  "grai-source-snowflake": "/images/snowflake-logo.png",
  "grai-source-mssql": "/images/mssql-logo.png",
  "grai-source-bigquery": "/images/bigquery-logo.png",
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
