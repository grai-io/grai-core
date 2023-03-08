import React from "react"
import { Cancel, CheckCircle } from "@mui/icons-material"
import { Chip } from "@mui/material"

type TestResultChipProps = {
  testPass: boolean
}

const TestResultChip: React.FC<TestResultChipProps> = ({ testPass }) => (
  <Chip
    variant="outlined"
    label={testPass ? "Passed" : "Failed"}
    color={testPass ? "success" : "error"}
    icon={testPass ? <CheckCircle /> : <Cancel />}
  />
)

export default TestResultChip
