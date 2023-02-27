import React from "react"
import TableProfile, { TableInterface } from "./TableProfile"
import Tabs from "components/tabs/Tabs"
import { BarChart, Mediation, TableRows } from "@mui/icons-material"
import TableLineage from "./TableLineage"

type TableContentProps = {
  table: TableInterface
}

const TableContent: React.FC<TableContentProps> = ({ table }) => (
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
)

export default TableContent
