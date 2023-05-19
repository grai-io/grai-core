import React, { useRef, useState } from "react"
import {
  ArrowDropDown,
  CalendarMonth,
  EventRepeat,
  PlayArrow,
} from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import {
  Button,
  ButtonGroup,
  ClickAwayListener,
  Grow,
  ListItemIcon,
  ListItemText,
  MenuItem,
  MenuList,
  Paper,
  Popper,
} from "@mui/material"

type ConnectionRunButtonProps = {
  onRun: (type: string) => void
  disabled?: boolean
  loading?: boolean
  events: boolean
  status: string | null
}

const ConnectionRunButton: React.FC<ConnectionRunButtonProps> = ({
  onRun,
  disabled,
  loading,
  events,
  status,
}) => {
  const [open, setOpen] = useState(false)
  const anchorRef = useRef<HTMLDivElement>(null)

  const handleClose = (event: Event) => {
    if (
      anchorRef.current &&
      anchorRef.current.contains(event.target as HTMLElement)
    ) {
      return
    }

    setOpen(false)
  }

  const handleToggle = () => {
    setOpen(prevOpen => !prevOpen)
  }

  const handleClick = (type: string) => () => {
    setOpen(false)
    onRun(type)
  }

  return (
    <>
      <ButtonGroup ref={anchorRef}>
        <LoadingButton
          onClick={handleClick("UPDATE")}
          variant="outlined"
          startIcon={<PlayArrow />}
          disabled={disabled}
          loading={loading}
          loadingPosition="start"
          data-testid="connection-run"
          sx={{ height: "40px", px: 3 }}
        >
          {(loading && status) || "Run"}
        </LoadingButton>
        {events && (
          <Button
            disabled={loading}
            onClick={handleToggle}
            sx={{ minWidth: 0, px: 1 }}
          >
            <ArrowDropDown />
          </Button>
        )}
      </ButtonGroup>
      {events && (
        <Popper
          sx={{
            zIndex: 1,
          }}
          open={open}
          anchorEl={anchorRef.current}
          role={undefined}
          transition
          disablePortal
        >
          {({ TransitionProps, placement }) => (
            <Grow
              {...TransitionProps}
              style={{
                transformOrigin:
                  placement === "bottom" ? "left top" : "left bottom",
              }}
            >
              <Paper>
                <ClickAwayListener onClickAway={handleClose}>
                  <MenuList id="split-button-menu" autoFocusItem>
                    <MenuItem onClick={handleClick("EVENTS")}>
                      <ListItemIcon>
                        <CalendarMonth />
                      </ListItemIcon>
                      <ListItemText primary="Run Events" />
                    </MenuItem>
                    <MenuItem onClick={handleClick("EVENTS_ALL")}>
                      <ListItemIcon>
                        <EventRepeat />
                      </ListItemIcon>
                      <ListItemText primary="Run All Events" />
                    </MenuItem>
                  </MenuList>
                </ClickAwayListener>
              </Paper>
            </Grow>
          )}
        </Popper>
      )}
    </>
  )
}

export default ConnectionRunButton
