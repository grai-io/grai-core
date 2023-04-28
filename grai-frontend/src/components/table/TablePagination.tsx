import React from "react"
import {
  Box,
  Button,
  Stack,
  TableCell,
  TablePagination as BaseTablePagination,
  TableRow,
  Typography,
} from "@mui/material"

interface TablePaginationActionsProps {
  count: number
  page: number
  rowsPerPage: number
  onPageChange: (
    event: React.MouseEvent<HTMLButtonElement>,
    newPage: number
  ) => void
}

interface TablePaginationActionsExtendedProps
  extends TablePaginationActionsProps {
  disabled: boolean
}

const TablePaginationActions: React.FC<TablePaginationActionsExtendedProps> = ({
  count,
  page,
  rowsPerPage,
  onPageChange,
  disabled,
}) => {
  const handleBackButtonClick = (event: React.MouseEvent<HTMLButtonElement>) =>
    onPageChange(event, page - 1)

  const handleNextButtonClick = (event: React.MouseEvent<HTMLButtonElement>) =>
    onPageChange(event, page + 1)

  return (
    <Stack direction="row" spacing={1} sx={{ mr: 1 }}>
      <Button
        onClick={handleBackButtonClick}
        disabled={disabled || page === 0}
        variant="outlined"
      >
        Previous
      </Button>
      <Button
        onClick={handleNextButtonClick}
        disabled={disabled || page >= Math.ceil(count / rowsPerPage) - 1}
        variant="outlined"
      >
        Next
      </Button>
    </Stack>
  )
}

type TablePaginationProps = {
  count: number
  rowsPerPage: number
  page: number
  onPageChange?: (
    event: React.MouseEvent<HTMLButtonElement> | null,
    page: number
  ) => void
  type?: string
}

const TablePagination: React.FC<TablePaginationProps> = ({
  count,
  rowsPerPage,
  page,
  onPageChange,
  type,
}) => (
  <TableRow>
    <TableCell colSpan={99} sx={{ p: 0, borderBottom: "none" }}>
      <Box sx={{ display: "flex" }}>
        <Typography variant="body2" sx={{ flexGrow: 1, m: 2 }}>
          {count} {type ?? (count !== 1 ? "rows" : "row")}
        </Typography>
        <BaseTablePagination
          component="div"
          rowsPerPageOptions={[]}
          count={count}
          rowsPerPage={rowsPerPage}
          page={page}
          labelDisplayedRows={() => null}
          onPageChange={onPageChange ?? (() => {})}
          /* istanbul ignore next */
          onRowsPerPageChange={() => {}}
          ActionsComponent={(props: TablePaginationActionsProps) => (
            <TablePaginationActions {...props} disabled={!onPageChange} />
          )}
        />
      </Box>
    </TableCell>
  </TableRow>
)

export default TablePagination
