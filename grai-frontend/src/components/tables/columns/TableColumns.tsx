import React, { useState } from "react"
import { CloseFullscreen, OpenInFull } from "@mui/icons-material"
import { Button } from "@mui/material"
import TableHeader from "components/table/TableHeader"
import TableColumnsTable, { Column } from "./TableColumnsTable"

type TableColumnsProps = {
  columns: Column[]
}

const TableColumns: React.FC<TableColumnsProps> = ({ columns }) => {
  const [search, setSearch] = useState<string | null>(null)
  const [expanded, setExpanded] = useState<string[]>([])

  const handleExpand = (id: string, expand: boolean) =>
    setExpanded(expand ? [...expanded, id] : expanded.filter(e => e !== id))
  const handleExpandAll = () => setExpanded(columns.map(column => column.id))
  const handleCollapseAll = () => setExpanded([])

  return (
    <>
      <TableHeader
        search={search}
        onSearch={setSearch}
        rightButtons={
          expanded.length > 0 ? (
            <Button
              variant="outlined"
              startIcon={<CloseFullscreen />}
              onClick={handleCollapseAll}
            >
              Collapse all rows
            </Button>
          ) : (
            <Button
              variant="outlined"
              startIcon={<OpenInFull />}
              onClick={handleExpandAll}
            >
              Expand all rows
            </Button>
          )
        }
      />
      <TableColumnsTable
        search={search}
        columns={columns}
        expanded={expanded}
        onExpand={handleExpand}
      />
    </>
  )
}

export default TableColumns
