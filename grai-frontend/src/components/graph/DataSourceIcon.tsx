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

  return (
    <Box
      sx={{
        m: "10px",
        border: "1px solid rgba(0, 0, 0, 0.08)",
        borderRadius: "8px",
        height: "48px",
        width: "48px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {icon && (
        <img src={icon} alt={`${dataSource} logo`} height={32} width={32} />
      )}
    </Box>
  )
}

export default DataSourceIcon
