import React from "react"
import { FilterAlt } from "@mui/icons-material"
import { Box, Button, Chip, Stack, Typography } from "@mui/material"
import { Filter } from "components/filters/filters"
import { CombinedFilters } from "components/graph/useCombinedFilters"
import { Option } from "./FilterAutocomplete"

const inlineFilterLabel = (filter: Filter) =>
  [filter.field, filter.operator, filter.value].join(" ")

const filterNotEmpty = (filter: Filter) =>
  filter.field && filter.operator && filter.value

type FilterButtonProps = {
  options: Option[]
  combinedFilters: CombinedFilters
  onClick?: (event: React.MouseEvent<HTMLElement>) => void
}

const FilterButton: React.FC<FilterButtonProps> = ({
  options,
  combinedFilters,
  onClick,
}) => {
  const selectedFilters = options.filter(
    option => combinedFilters.filters?.includes(option.value),
  )

  const handleRemoveFilter = (filter: string) =>
    combinedFilters.setFilters(
      combinedFilters.filters?.filter(f => f !== filter) ?? [],
    )

  const onRemoveInlineFilter = (index: number) =>
    combinedFilters.setInlineFilters(
      combinedFilters.inlineFilters?.filter((_, i) => i !== index) ?? [],
    )

  return (
    <Button
      disableRipple
      onClick={onClick}
      sx={{
        minWidth: 240,
        backgroundColor: "white",
        border: "1px solid #CBCBCB",
        borderRadius: "4px",
        ":hover": {
          borderColor: "black",
          backgroundColor: "white",
        },
        pl: "14px",
      }}
    >
      <Box sx={{ display: "flex", width: "100%", textAlign: "left" }}>
        <Typography sx={{ color: "#B4B4B4", mr: 2 }}>Filters</Typography>
        <Stack direction="row" spacing={1}>
          {selectedFilters?.map(filter => (
            <Chip
              key={filter.value}
              label={filter.label}
              size="small"
              onDelete={() => handleRemoveFilter(filter.value)}
            />
          ))}
          {combinedFilters.inlineFilters
            ?.filter(filterNotEmpty)
            .map((filter, index) => (
              <Chip
                key={index}
                label={inlineFilterLabel(filter)}
                size="small"
                onDelete={() => onRemoveInlineFilter(index)}
              />
            ))}
        </Stack>
        <Box sx={{ flexGrow: 1 }} />
        <FilterAlt sx={{ color: "#C2C2C2", ml: 1 }} />
      </Box>
    </Button>
  )
}

export default FilterButton
