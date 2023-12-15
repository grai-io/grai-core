import { Box } from "@mui/material"
import { fireEvent, render, screen } from "testing"
import HoverState from "./HoverState"

test("renders", async () => {
  render(
    <HoverState>
      {(hover, bindHover) => <Box {...bindHover}>Test</Box>}
    </HoverState>,
  )

  await screen.findByText("Test")
})

test("hover", async () => {
  render(
    <HoverState>
      {(hover, bindHover) => <Box {...bindHover}>Test{hover && "hover"}</Box>}
    </HoverState>,
  )

  await screen.findByText("Test")

  fireEvent.mouseEnter(screen.getByText("Test"))

  await screen.findByText("Testhover")

  fireEvent.mouseLeave(screen.getByText("Testhover"))

  await screen.findByText("Test")
})
