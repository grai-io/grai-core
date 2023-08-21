import React from "react"
import { Box } from "@mui/material"
import GraphComponent, {
  ResultError,
  Table,
} from "components/graph/GraphComponent"
import useFilters from "components/graph/useFilters"
import useInlineFilters from "components/graph/useInlineFilters"
import { Run } from "./run/RunLog"

type ReportGraphProps = {
  tables: Table[]
  errors: ResultError[] | null
  limitGraph: boolean
  run: Run | null
}

const ReportGraph: React.FC<ReportGraphProps> = ({
  tables,
  errors,
  limitGraph,
  run,
}) => {
  const { filters, setFilters } = useFilters(`reports-${run?.id}-graph-filters`)
  const { inlineFilters, setInlineFilters } = useInlineFilters(
    `reports-${run?.id}-graph-inline-filters`,
  )

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
        inlineFilters={inlineFilters ?? []}
        setInlineFilters={setInlineFilters}
      />
    </Box>
  )
}

export default ReportGraph
