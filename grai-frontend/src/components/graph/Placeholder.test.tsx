import { render, screen, waitFor } from "testing"
import Placeholder from "./Placeholder"

test("renders", async () => {
  render(<Placeholder />)

  // eslint-disable-next-line testing-library/no-wait-for-empty-callback
  await waitFor(() => {
    expect(screen.getByTestId("placeholder")).toBeInTheDocument()
  })
})
