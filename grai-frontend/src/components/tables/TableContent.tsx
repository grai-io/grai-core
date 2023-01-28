import { Box } from "@mui/material"
import React from "react"
import { Edge, Table as GraphTable } from "helpers/graph"
import TableLineage from "../../components/tables/TableLineage"
import TableProfile, { Table } from "./TableProfile"
import Tabs from "components/tabs/Tabs"
import { BarChart, Mediation, TableRows } from "@mui/icons-material"

type TableContentProps = {
  table: Table
}

const TableContent: React.FC<TableContentProps> = ({ table }) => (
  <Box sx={{ px: 2, py: 1 }}>
    <Tabs
      tabs={[
        {
          value: "profile",
          label: "Profile",
          icon: <BarChart />,
          element: <TableProfile table={table} />,
        },
        {
          value: "sample",
          label: "Sample",
          icon: <TableRows />,
          disabled: true,
        },
        {
          value: "lineage",
          label: "Lineage",
          icon: <Mediation />,
          element: <TableLineage table={table} />,
        },
      ]}
    />
  </Box>
)

export default TableContent
