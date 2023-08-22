import { createTheme } from "@mui/material"
import { render } from "testing"
import StyledInput from "./StyledInput"

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
