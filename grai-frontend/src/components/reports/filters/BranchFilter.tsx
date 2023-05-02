import React from "react"
import { Autocomplete, InputAdornment, TextField } from "@mui/material"
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
    <Autocomplete
      disablePortal
      disabled={disabled}
      options={branches}
      getOptionLabel={option => option.reference}
      value={value}
      onChange={handleChange}
      sx={{ width: 350, mb: "24px" }}
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
  )
}

export default BranchFilter
