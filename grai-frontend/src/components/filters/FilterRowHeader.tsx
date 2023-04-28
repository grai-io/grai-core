import React from "react"
import { Grid, Typography } from "@mui/material"

const FilterRowHeader: React.FC = () => (
  <Grid container spacing={1}>
    <Grid item md={3}>
      <Typography>Property</Typography>
    </Grid>
    <Grid item md={3}>
      <Typography>Field</Typography>
    </Grid>
    <Grid item md={3}>
      <Typography>Operator</Typography>
    </Grid>
    <Grid item md={3}>
      <Typography>Value</Typography>
    </Grid>
  </Grid>
)

export default FilterRowHeader
