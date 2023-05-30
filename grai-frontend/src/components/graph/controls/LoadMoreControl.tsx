import React from "react"
import { Alert, Button } from "@mui/material"

export type LoadMoreControlOptions = {
  count: number
  total: number
  onLoadMore: () => void
}

type LoadMoreControlProps = {
  options: LoadMoreControlOptions
}

const LoadMoreControl: React.FC<LoadMoreControlProps> = ({ options }) => (
  <Alert
    severity="warning"
    action={
      <Button color="inherit" size="small" onClick={options.onLoadMore}>
        Load More
      </Button>
    }
    sx={{ mt: 2 }}
  >
    Due to the large number of tables, we have only loaded the first{" "}
    {options.count}
  </Alert>
)

export default LoadMoreControl
