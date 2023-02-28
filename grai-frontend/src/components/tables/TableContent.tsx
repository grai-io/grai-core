import React from "react"
import { BarChart, Mediation, TableRows } from "@mui/icons-material"
import Tabs from "components/tabs/Tabs"
import TableProfile, { TableInterface } from "./TableProfile"
import TableLineage from "../../components/tables/TableLineage"

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
