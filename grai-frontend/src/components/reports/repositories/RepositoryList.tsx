import React from "react"
import {
  Box,
  Card,
  List,
  ListItemButton,
  ListItemText,
  Typography,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { Link } from "react-router-dom"

interface Repository {
  type: string
  owner: string
  repo: string
}

type RepositoryListProps = {
  repositories: Repository[]
}

const RepositoryList: React.FC<RepositoryListProps> = ({ repositories }) => {
  const { routePrefix } = useWorkspace()

  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <Box sx={{ p: 3 }}>
        <Typography variant="h6">Select Repository</Typography>
        <List sx={{ pb: 0 }}>
          {repositories.map(repository => (
            <ListItemButton
              key={repository.repo}
              component={Link}
              to={`${routePrefix}/reports/${repository.type}/${repository.owner}/${repository.repo}`}
            >
              <ListItemText primary={repository.repo} />
            </ListItemButton>
          ))}
        </List>
      </Box>
    </Card>
  )
}

export default RepositoryList
