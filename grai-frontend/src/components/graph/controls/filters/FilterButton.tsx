import React from "react"
import { FilterAlt } from "@mui/icons-material"
import { Box, Button, Chip, Stack, Typography } from "@mui/material"
import { Option } from "./FilterAutocomplete"

type FilterButtonProps = {
  selectedFilters: Option[]
  onClick?: (event: React.MouseEvent<HTMLElement>) => void
  onRemoveFilter?: (filter: string) => void
}

const FilterButton: React.FC<FilterButtonProps> = ({
  selectedFilters,
  onClick,
  onRemoveFilter,
}) => (
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
            onDelete={() => onRemoveFilter && onRemoveFilter(filter.value)}
          />
        ))}
      </Stack>
      <Box sx={{ flexGrow: 1 }} />
      <FilterAlt sx={{ color: "#C2C2C2", ml: 1 }} />
    </Box>
  </Button>
)

export default FilterButton
