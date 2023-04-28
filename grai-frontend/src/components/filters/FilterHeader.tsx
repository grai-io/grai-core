import React from "react"
import { KeyboardBackspace, ContentCopy } from "@mui/icons-material"
import {
  Box,
  Button,
  Typography,
  Tooltip,
  IconButton,
  Divider,
} from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

interface Filter {
  name: string | null
}

type FilterHeaderProps = {
  filter: Filter
}

const FilterHeader: React.FC<FilterHeaderProps> = ({ filter }) => {
  const { routePrefix } = useWorkspace()

  return (
    <>
      <Box sx={{ display: "flex", p: 2 }}>
        <Box>
          <Button
            component={Link}
            to={`${routePrefix}/filters`}
            color="secondary"
            startIcon={<KeyboardBackspace />}
          >
            Back
          </Button>
        </Box>
        <Typography
          variant="h6"
          sx={{ textTransform: "uppercase", mx: 1, mt: 0.3 }}
        >
          {filter.name}
        </Typography>
        <Box sx={{ flexGrow: 1 }}>
          <Tooltip title="Copy Filter Name">
            <IconButton sx={{ mt: 0.5 }}>
              <ContentCopy sx={{ fontSize: 15 }} />
            </IconButton>
          </Tooltip>
        </Box>
        {/* <ConnectionMenu connection={connection} workspaceId={workspaceId} /> */}
      </Box>
      <Divider />
    </>
  )
}

export default FilterHeader
