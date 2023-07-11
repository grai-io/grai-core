import React from "react"
import { Box } from "@mui/material"

type DataSourceIconProps = {
  dataSource: string
  noMargin?: boolean
  noBorder?: boolean
  size?: "small" | "medium" | "large"
  grayscale?: boolean
}

interface Icons {
  [key: string]: string
}

const icons: Icons = {
  "grai-source-dbt": "/icons/data-sources/dbt.png",
  "grai-source-dbt_cloud": "/icons/data-sources/dbt.png",
  "grai-source-postgres": "/icons/data-sources/postgres.png",
  "grai-source-snowflake": "/icons/data-sources/snowflake.png",
  "grai-source-mssql": "/icons/data-sources/mssql.png",
  "grai-source-bigquery": "/icons/data-sources/bigquery.png",
  "grai-source-mysql": "/icons/data-sources/mysql.png",
  "grai-source-redshift": "/icons/data-sources/redshift.png",
  "grai-source-metabase": "/icons/data-sources/metabase.png",
}

const heights = {
  small: 24,
  medium: 32,
  large: 48,
}

const DataSourceIcon: React.FC<DataSourceIconProps> = ({
  dataSource,
  noMargin,
  noBorder,
  size,
  grayscale,
}) => {
  const icon = icons[dataSource]

  const height = size ? heights[size] : heights.medium

  return (
    <Box
      sx={{
        m: noMargin ? 0 : "10px",
        border: noBorder ? null : "1px solid rgba(0, 0, 0, 0.08)",
        borderRadius: "8px",
        height: "48px",
        width: "48px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        filter: grayscale ? "grayscale(100%)" : null,
      }}
    >
      {icon && (
        <img
          src={icon}
          alt={`${dataSource} logo`}
          height={height}
          width={height}
        />
      )}
    </Box>
  )
}

export default DataSourceIcon
