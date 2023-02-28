import React from "react"
import { Autocomplete, Box, InputAdornment, TextField } from "@mui/material"
import useSearchParams from "helpers/useSearchParams"

export interface Repository {
  type: string
  owner: string
  repo: string
}

type RepositoryFilterProps = {
  repositories: Repository[]
  disabled?: boolean
}

const RepositoryFilter: React.FC<RepositoryFilterProps> = ({
  repositories,
  disabled,
}) => {
  const { searchParams, setSearchParam } = useSearchParams()

  const handleChange = (
    event: React.SyntheticEvent<Element, Event>,
    value: Repository | null
  ) =>
    setSearchParam("repository", value ? `${value.owner}/${value.repo}` : null)

  const param = searchParams.get("repository")?.split("/")

  const value =
    (param
      ? repositories.find(
          repository =>
            repository.owner === param[0] && repository.repo === param[1]
        )
      : null) ?? null

  return (
    <Box sx={{ py: 2, display: "flex" }}>
      <Autocomplete
        disablePortal
        disabled={disabled}
        options={repositories}
        getOptionLabel={option => `${option.owner}/${option.repo}`}
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
                  Repository
                </InputAdornment>
              ),
            }}
          />
        )}
      />
    </Box>
  )
}

export default RepositoryFilter
