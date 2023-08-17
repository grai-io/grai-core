import React, { useState } from "react"
import { gql, useQuery } from "@apollo/client"
import { Add, Close } from "@mui/icons-material"
import {
  Box,
  Button,
  Grid,
  InputAdornment,
  List,
  ListItem,
  TextField,
  Tooltip,
} from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import {
  GetFiltersDrawer,
  GetFiltersDrawerVariables,
} from "./__generated__/GetFiltersDrawer"
import GraphFilter from "./GraphFilter"

export const GET_FILTERS = gql`
  query GetFiltersDrawer(
    $organisationName: String!
    $workspaceName: String!
    $search: String
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      filters(search: $search) {
        data {
          id
          name
        }
      }
    }
  }
`

type GraphFiltersProps = {
  filters: string[]
  setFilters: (filters: string[]) => void
}

const GraphFilters: React.FC<GraphFiltersProps> = ({ filters, setFilters }) => {
  const [search, setSearch] = useState("")
  const { organisationName, workspaceName, routePrefix } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetFiltersDrawer,
    GetFiltersDrawerVariables
  >(GET_FILTERS, {
    variables: {
      organisationName,
      workspaceName,
      search,
    },
    context: {
      debounceKey: "filters",
      debounceTimeout: 1000,
    },
  })

  if (error) return <GraphError error={error} />

  return (
    <Box>
      <Box sx={{ p: 1 }}>
        <TextField
          fullWidth
          size="small"
          placeholder="Search Filters"
          value={search}
          onChange={event => setSearch(event.target.value)}
          InputProps={{
            endAdornment: search !== "" && (
              <InputAdornment position="end">
                <Tooltip title="Clear">
                  <Close
                    onClick={() => setSearch("")}
                    sx={{ color: "divider", cursor: "pointer" }}
                  />
                </Tooltip>
              </InputAdornment>
            ),
          }}
          inputProps={{
            "data-testid": "search-input",
          }}
        />
      </Box>
      {loading && <Loading />}
      <List
        disablePadding
        sx={{
          maxHeight: "calc(100vh - 200px)",
          overflowY: "auto",
          overflowX: "hidden",
          border: 0,
          borderTop: 1,
          borderColor: theme => theme.palette.grey[200],
          borderStyle: "solid",
        }}
      >
        <ListItem
          sx={{
            px: 1,
            border: 0,
            borderBottom: 1,
            borderColor: theme => theme.palette.grey[200],
            borderStyle: "solid",
          }}
        >
          <Grid container spacing={1}>
            <Grid item md={6}>
              <Button
                variant="outlined"
                fullWidth
                startIcon={<Add />}
                component={Link}
                to={`${routePrefix}/filters/create`}
              >
                Add Filter
              </Button>
            </Grid>
            <Grid item md={6}>
              <Button
                variant="outlined"
                fullWidth
                component={Link}
                to={`${routePrefix}/filters`}
              >
                Manage Filters
              </Button>
            </Grid>
          </Grid>
        </ListItem>
        {data?.workspace.filters.data.map(filter => (
          <GraphFilter
            key={filter.id}
            filter={filter}
            filters={filters}
            setFilters={setFilters}
          />
        ))}
      </List>
    </Box>
  )
}

export default GraphFilters
