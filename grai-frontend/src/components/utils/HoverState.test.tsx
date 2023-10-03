import { Box } from "@mui/material"
import { fireEvent, render, screen, waitFor } from "testing"
import HoverState from "./HoverState"

test("renders", async () => {
  render(
    <HoverState>
      {(hover, bindHover) => <Box {...bindHover}>Test</Box>}
    </HoverState>,
  )

  await waitFor(() => {
    expect(screen.getByText("Test")).toBeInTheDocument()
  })
})

test("hover", async () => {
  render(
    <HoverState>
      {(hover, bindHover) => <Box {...bindHover}>Test{hover && "hover"}</Box>}
    </HoverState>,
  )

  await waitFor(() => {
    expect(screen.getByText("Test")).toBeInTheDocument()
  })

  fireEvent.mouseEnter(screen.getByText("Test"))

  await waitFor(() => {
    expect(screen.getByText("Testhover")).toBeInTheDocument()
  })

  fireEvent.mouseLeave(screen.getByText("Testhover"))

  await waitFor(() => {
    expect(screen.getByText("Test")).toBeInTheDocument()
  })
})
