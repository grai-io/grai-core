import React, { useState } from "react"
import { Box } from "@mui/material"
import { CombinedFilters } from "components/graph/useCombinedFilters"
import AddFilter from "./AddFilter"
import { Option } from "./FilterAutocomplete"
import SavedFilters from "./SavedFilters"
import { Values } from "../FilterControl"

type FilterContentProps = {
  options: Option[]
  onClose?: () => void
  combinedFilters: CombinedFilters
  values: Values
  workspaceId: string
}

const FilterContent: React.FC<FilterContentProps> = React.forwardRef(
  ({ options, onClose, combinedFilters, values, workspaceId }, ref) => {
    const [add, setAdd] = useState(options.length === 0)

    return (
      <Box ref={ref}>
        {add ? (
          <AddFilter
            onClose={() => setAdd(false)}
            inlineFilters={combinedFilters.inlineFilters ?? []}
            setInlineFilters={combinedFilters.setInlineFilters}
            values={values}
            workspaceId={workspaceId}
          />
        ) : (
          <SavedFilters
            options={options}
            onClose={onClose}
            onAdd={() => setAdd(true)}
            filters={combinedFilters.filters ?? []}
            setFilters={combinedFilters.setFilters}
          />
        )}{" "}
      </Box>
    )
  },
)

export default FilterContent
