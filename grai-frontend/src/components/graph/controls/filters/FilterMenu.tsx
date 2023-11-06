import React, { useState } from "react"
import { ClickAwayListener, Popper, styled } from "@mui/material"
import { CombinedFilters } from "components/graph/useCombinedFilters"
import { Option } from "./FilterAutocomplete"
import FilterButton from "./FilterButton"
import FilterContent from "./FilterContent"
import { Values } from "../FilterControl"

const StyledPopper = styled(Popper)(({ theme }) => ({
  border: "1px solid #e1e4e8",
  boxShadow: "0 8px 24px rgba(149, 157, 165, 0.2)",
  borderRadius: 6,
  zIndex: theme.zIndex.modal,
  fontSize: 13,
  color: "#24292e",
  backgroundColor: "#fff",
}))

type FilterMenuProps = {
  options: Option[]
  combinedFilters: CombinedFilters
  values: Values
  workspaceId: string
}

const FilterMenu: React.FC<FilterMenuProps> = ({
  options,
  combinedFilters,
  values,
  workspaceId,
}) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    if (anchorEl) {
      anchorEl.focus()
    }
    setAnchorEl(null)
  }

  const open = Boolean(anchorEl)
  const id = open ? "github-label" : undefined

  return (
    <>
      <FilterButton onClick={handleClick} />
      <StyledPopper
        id={id}
        open={open}
        anchorEl={anchorEl}
        placement="bottom-start"
        modifiers={[
          {
            name: "offset",
            options: {
              offset: [0, 10],
            },
          },
        ]}
      >
        <ClickAwayListener onClickAway={handleClose}>
          <FilterContent
            options={options}
            onClose={handleClose}
            combinedFilters={combinedFilters}
            values={values}
            workspaceId={workspaceId}
          />
        </ClickAwayListener>
      </StyledPopper>
    </>
  )
}

export default FilterMenu
