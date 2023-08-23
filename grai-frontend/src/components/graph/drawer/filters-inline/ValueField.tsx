import React from "react"
import { Close, Done } from "@mui/icons-material"
import {
  Autocomplete,
  AutocompleteChangeReason,
  AutocompleteCloseReason,
  Box,
} from "@mui/material"
import arrayWrap from "helpers/arrayWrap"
import notEmpty from "helpers/notEmpty"
import {
  Field,
  Filter,
  OperationOption,
  Operator,
} from "components/filters/filters"
import PopperComponent from "./PopperComponent"
import StyledInput from "./StyledInput"

type ValueFieldProps = {
  field: Field | null
  operator: Operator | null
  filter: Filter
  setFilter: (filter: Filter) => void
  onClose: () => void
}

const ValueField: React.FC<ValueFieldProps> = ({
  field,
  operator,
  filter,
  setFilter,
  onClose,
}) => {
  const handleValueChange = (
    event: React.SyntheticEvent<Element, Event>,
    newValue:
      | null
      | string
      | OperationOption
      | (null | string | OperationOption)[],
    reason: AutocompleteChangeReason,
  ) =>
    setFilter({
      ...filter,
      value: Array.isArray(newValue)
        ? newValue
            .map(option =>
              typeof option === "string" ? option : option?.value,
            )
            .filter(notEmpty)
        : (typeof newValue === "string" ? newValue : newValue?.value) ?? null,
    })

  if (!operator?.options)
    return (
      <StyledInput
        autoFocus
        placeholder={filter.field ?? ""}
        onChange={event => setFilter({ ...filter, value: event.target.value })}
        value={filter.value ?? ""}
      />
    )

  if (operator.multiple)
    return (
      <Autocomplete<OperationOption | string, true>
        open
        multiple
        onClose={(
          _: React.ChangeEvent<{}>,
          reason: AutocompleteCloseReason,
        ) => {
          if (reason === "escape") {
            onClose()
          }
        }}
        value={operator.options.filter(option =>
          arrayWrap(filter.value).includes(
            typeof option === "string" ? option : option?.value,
          ),
        )}
        onChange={handleValueChange}
        disableCloseOnSelect
        PopperComponent={PopperComponent}
        renderTags={() => null}
        noOptionsText={`No ${field?.label ?? filter.field}`}
        renderOption={(props, option, { selected }) => (
          <li {...props}>
            <Box
              component={Done}
              sx={{ width: 17, height: 17, mr: "5px", ml: "-2px" }}
              style={{
                visibility: selected ? "visible" : "hidden",
              }}
            />
            <Box
              sx={{
                flexGrow: 1,
                "& span": {
                  color: "#586069",
                },
              }}
            >
              {typeof option === "string" ? option : option?.label}
            </Box>
            <Box
              component={Close}
              sx={{ opacity: 0.6, width: 18, height: 18 }}
              style={{
                visibility: selected ? "visible" : "hidden",
              }}
            />
          </li>
        )}
        options={operator.options}
        getOptionLabel={option =>
          (typeof option === "string" ? option : option?.label) ?? ""
        }
        renderInput={params => (
          <StyledInput
            ref={params.InputProps.ref}
            inputProps={params.inputProps}
            autoFocus
            placeholder={`Filter ${filter.field}s`}
          />
        )}
      />
    )

  return (
    <Autocomplete<OperationOption | string, false>
      open
      onClose={(_: React.ChangeEvent<{}>, reason: AutocompleteCloseReason) => {
        if (reason === "escape") {
          onClose()
        }
      }}
      value={
        operator.options.find(option =>
          typeof option === "string"
            ? option === filter.value
            : option.value === filter.value,
        ) ?? null
      }
      onChange={handleValueChange}
      disableCloseOnSelect
      PopperComponent={PopperComponent}
      noOptionsText={`No ${field?.label ?? filter.field}`}
      renderOption={(props, option, { selected }) => (
        <li {...props}>
          <Box
            component={Done}
            sx={{ width: 17, height: 17, mr: "5px", ml: "-2px" }}
            style={{
              visibility: selected ? "visible" : "hidden",
            }}
          />
          <Box
            sx={{
              flexGrow: 1,
              "& span": {
                color: "#586069",
              },
            }}
          >
            {typeof option === "string" ? option : option?.label}
          </Box>
        </li>
      )}
      options={operator.options}
      getOptionLabel={option =>
        (typeof option === "string" ? option : option?.label) ?? ""
      }
      renderInput={params => (
        <StyledInput
          ref={params.InputProps.ref}
          inputProps={params.inputProps}
          autoFocus
          placeholder={`Filter ${filter.field}s`}
        />
      )}
    />
  )
}

export default ValueField
