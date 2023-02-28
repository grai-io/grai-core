import React from "react"
import { Table, TableBody, TableCell, TableHead, TableRow } from "@mui/material"
import { Error } from "components/graph/Graph"

type TestResultsProps = {
  errors: Error[] | null
}

const TestResults: React.FC<TestResultsProps> = ({ errors }) => (
  <Table sx={{ mt: 2 }}>
    <TableHead>
      <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
        <TableCell>Changed Node</TableCell>
        <TableCell>Failing Dependency</TableCell>
        <TableCell>Test</TableCell>
        <TableCell>Message</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {errors?.map((error, index) => (
        <TableRow key={index}>
          <TableCell>{error.destination}</TableCell>
          <TableCell>{error.source}</TableCell>
          <TableCell>{error.test}</TableCell>
          <TableCell>{error.message}</TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
)

export default TestResults
