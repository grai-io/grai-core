import React, { ReactNode } from "react"
import { Box, Typography, Divider, Stack, SxProps } from "@mui/material"

interface Test {
  message: string
}

type TestSectionProps = {
  tests?: Test[]
  type: string
  icon?: ReactNode
  sx?: SxProps
}

const TestSection: React.FC<TestSectionProps> = ({ tests, type, icon, sx }) =>
  tests ? (
    <>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          flexWrap: "wrap",
          ...sx,
        }}
      >
        <Typography sx={{ flexGrow: 1 }}>
          {tests.length} {type}
        </Typography>
        <Box>{icon}</Box>
      </Box>
      <Divider sx={{ mt: 0.75, mb: 1 }} />
      <Stack spacing={1}>
        {tests.map((test, index) => (
          <Typography variant="body2" key={index}>
            {test.message}
          </Typography>
        ))}
      </Stack>
    </>
  ) : null

export default TestSection
