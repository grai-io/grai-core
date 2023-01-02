import React from "react"
import {
  TableCell as BaseTableCell,
  TableCellProps as BaseTableCellProps,
} from "@mui/material"

export interface TableCellProps extends BaseTableCellProps {
  stopPropagation?: boolean
}

const TableCell: React.FC<TableCellProps> = ({
  stopPropagation,
  children,
  ...rest
}) => (
  <BaseTableCell
    onClick={event => stopPropagation && event.stopPropagation()}
    {...rest}
  >
    {children}
  </BaseTableCell>
)

export default TableCell
