import React from "react"
import { Autocomplete, Box, InputAdornment, TextField } from "@mui/material"
import useSearchParams from "helpers/useSearchParams"

export interface Branch {
  reference: string
}

type BranchFilterProps = {
  branches: Branch[]
  disabled?: boolean
}

const BranchFilter: React.FC<BranchFilterProps> = ({ branches, disabled }) => {
  const { searchParams, setSearchParam } = useSearchParams()

  const handleChange = (
    event: React.SyntheticEvent<Element, Event>,
    value: Branch | null
  ) => setSearchParam("branch", value?.reference)

  const value =
    branches.find(branch => branch.reference === searchParams.get("branch")) ??
    null

  return (
    <Box sx={{ py: 2, display: "flex" }}>
      <Autocomplete
        disablePortal
        disabled={disabled}
        options={branches}
        getOptionLabel={option => option.reference}
        value={value}
        onChange={handleChange}
        sx={{ minWidth: 350 }}
        data-testid="autocomplete"
        renderInput={params => (
          <TextField
            {...params}
            size="small"
            InputProps={{
              ...params.InputProps,
              startAdornment: (
                <InputAdornment position="start" sx={{ ml: 1 }}>
                  Branch
                </InputAdornment>
              ),
            }}
          />
        )}
      />
    </Box>
  )
}

export default BranchFilter
