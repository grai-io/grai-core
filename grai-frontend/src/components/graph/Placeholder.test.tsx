import { render, screen } from "testing"
import Placeholder from "./Placeholder"

test("renders", async () => {
  render(<Placeholder />)

  await screen.findByTestId("placeholder")
})
