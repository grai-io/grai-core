import React from "react"
import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material"
import { Error } from "components/graph/Graph"
import TestResultChip from "./TestResultChip"

type TestResultsProps = {
  errors: Error[] | null
}

const TestResults: React.FC<TestResultsProps> = ({ errors }) => (
  <Table sx={{ mt: 2 }}>
    <TableHead>
      <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
        <TableCell>Changed Node</TableCell>
        <TableCell>Dependency</TableCell>
        <TableCell>Test</TableCell>
        <TableCell>Result</TableCell>
        <TableCell>Message</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {errors?.map((error, index) => (
        <TableRow key={index}>
          <TableCell>{error.destination}</TableCell>
          <TableCell>{error.source}</TableCell>
          <TableCell>{error.test}</TableCell>
          <TableCell sx={{ py: 0 }}>
            <TestResultChip testPass={error.test_pass} />
          </TableCell>
          <TableCell>{error.message}</TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
)

export default TestResults
