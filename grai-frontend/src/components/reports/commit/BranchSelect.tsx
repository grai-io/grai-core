import { Box, InputAdornment, MenuItem, TextField } from "@mui/material"
import useSearchParams from "helpers/useSearchParams"
import React, { ChangeEvent } from "react"
import { Repository } from "./CommitBreadcrumbs"

interface Branch {
  reference: string
}

type BranchSelectProps = {
  branches: Branch[]
}

const BranchSelect: React.FC<BranchSelectProps> = ({ branches }) => {
  const { searchParams, setSearchParam } = useSearchParams()

  const handleChange = (event: ChangeEvent<HTMLInputElement>) =>
    setSearchParam("branch", event.target.value, event.target.value === "any")

  return (
    <Box sx={{ py: 2, display: "flex" }}>
      <TextField
        select
        value={searchParams.get("branch") ?? "any"}
        onChange={handleChange}
        size="small"
        sx={{ minWidth: 300 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">Branch</InputAdornment>
          ),
        }}
      >
        <MenuItem value="any">Any</MenuItem>
        {branches.map(branch => (
          <MenuItem key={branch.reference} value={branch.reference}>
            {branch.reference}
          </MenuItem>
        ))}
      </TextField>
    </Box>
  )
}

export default BranchSelect
