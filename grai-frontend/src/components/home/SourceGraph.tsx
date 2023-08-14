import React from "react"
import { Box, Button, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import PageContent from "components/layout/PageContent"
import Graph, { SourceGraph as SourceGraphType } from "components/sources/Graph"

type SourceGraphProps = {
  source_graph: SourceGraphType
}

const SourceGraph: React.FC<SourceGraphProps> = ({ source_graph }) => (
  <PageContent noGutter noPadding>
    <Box sx={{ display: "flex", mb: 2, pt: "24px", mx: "24px" }}>
      <Typography
        sx={{ fontWeight: 800, fontSize: "20px", flexGrow: 1 }}
        variant="h5"
      >
        Sources
      </Typography>
      <Button
        component={Link}
        to="sources"
        size="large"
        sx={{ color: "#8338EC", fontWeight: 600, fontSize: "16px", mt: -1 }}
      >
        Explore all Sources
      </Button>
    </Box>
    <Box sx={{ height: "500px" }}>
      <Graph sourceGraph={source_graph} />
    </Box>
  </PageContent>
)

export default SourceGraph
