import React from "react"
import { Box } from "@mui/material"
import GraphComponent, {
  ResultError,
  Table,
} from "components/graph/GraphComponent"
import useFilters from "components/graph/useFilters"

type ReportGraphProps = {
  tables: Table[]
  errors: ResultError[] | null
  limitGraph: boolean
}

const ReportGraph: React.FC<ReportGraphProps> = ({
  tables,
  errors,
  limitGraph,
}) => {
  const { filters, setFilters } = useFilters()

  return (
    <Box
      sx={{
        height: "calc(100vh - 212px)",
      }}
    >
      <GraphComponent
        tables={tables}
        errors={errors}
        limitGraph={limitGraph}
        filters={filters ?? []}
        setFilters={setFilters}
      />
    </Box>
  )
}

export default ReportGraph
