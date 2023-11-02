import React from "react"
import { FilterAlt } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"

type FilterButtonProps = {
  onClick?: (event: React.MouseEvent<HTMLElement>) => void
}

const FilterButton: React.FC<FilterButtonProps> = ({ onClick }) => (
  <Button
    disableRipple
    onClick={onClick}
    sx={{
      width: 350,
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
      <Typography sx={{ flexGrow: 1, color: "#B4B4B4" }}>Filters</Typography>
      <FilterAlt sx={{ color: "#C2C2C2" }} />
    </Box>
  </Button>
)

export default FilterButton
