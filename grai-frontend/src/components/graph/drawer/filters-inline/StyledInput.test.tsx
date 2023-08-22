import { render } from "testing"
import StyledInput from "./StyledInput"
import { createTheme } from "@mui/material"

test("renders", async () => {
  render(<StyledInput />)
})

test("renders dark mode", async () => {
  const theme = createTheme({
    palette: {
      mode: "dark",
    },
  })

  render(<StyledInput />, {
    theme,
  })
})
