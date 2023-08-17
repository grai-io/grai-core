import React, { useState } from "react"
import { Add } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import { Box, Button, Stack, TextField } from "@mui/material"
import Form from "components/form/Form"
import { Filter, Source } from "./FilterRow"
import FilterRows from "./FilterRows"

const defaultFilter: Filter = {
  type: "table",
  field: null,
  operator: null,
  value: null,
}

export type Values = {
  name: string
  metadata: Filter[]
}

type FilterFormProps = {
  namespaces: string[]
  tags: string[]
  sources: Source[]
  defaultValues?: Values
  onClose?: () => void
  onSave: (values: Values) => void
  loading?: boolean
}

const FilterForm: React.FC<FilterFormProps> = ({
  namespaces,
  tags,
  sources,
  defaultValues,
  onClose,
  onSave,
  loading,
}) => {
  const [values, setValues] = useState<Values>(
    defaultValues ?? {
      name: "",
      metadata: [defaultFilter],
    },
  )

  const handleAddFilters = () =>
    setValues({ ...values, metadata: [...values.metadata, defaultFilter] })
  const handleChangeFilters = (filters: Filter[]) =>
    setValues({ ...values, metadata: filters })

  const handleSave = () => onSave(values)

  return (
    <Form onSubmit={handleSave}>
      <TextField
        label="Name"
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
        margin="normal"
        sx={{ mb: 3, minWidth: 450 }}
      />
      <FilterRows
        filters={values.metadata}
        onChange={handleChangeFilters}
        namespaces={namespaces}
        tags={tags}
        sources={sources}
      />

      <Stack spacing={2} direction="row" sx={{ mt: 3 }}>
        <Button
          startIcon={<Add />}
          variant="outlined"
          onClick={handleAddFilters}
        >
          Add Filter
        </Button>
        <Box sx={{ flexGrow: 1 }} />
        {onClose && (
          <Button variant="outlined" onClick={onClose}>
            Cancel
          </Button>
        )}
        <LoadingButton type="submit" variant="contained" loading={loading}>
          Save
        </LoadingButton>
      </Stack>
    </Form>
  )
}

export default FilterForm
