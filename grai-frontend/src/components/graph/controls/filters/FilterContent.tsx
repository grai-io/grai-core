import React, { useState } from "react"
import { Box } from "@mui/material"
import AddFilter from "./AddFilter"
import { Option } from "./FilterAutocomplete"
import SavedFilters from "./SavedFilters"

type FilterContentProps = {
  options: Option[]
  onClose?: () => void
}

const FilterContent: React.FC<FilterContentProps> = React.forwardRef(
  ({ options, onClose }, ref) => {
    const [add, setAdd] = useState(options.length === 0)

    return (
      <Box ref={ref}>
        {add ? (
          <AddFilter onClose={() => setAdd(false)} />
        ) : (
          <SavedFilters
            options={options}
            onClose={onClose}
            onAdd={() => setAdd(true)}
          />
        )}{" "}
      </Box>
    )
  },
)

export default FilterContent
