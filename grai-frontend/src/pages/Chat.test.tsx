import { render, screen, waitFor } from "testing"
import Chat from "./Chat"

test("renders", async () => {
  render(<Chat />)

  await waitFor(() => {
    expect(screen.getByText("GrAI Chat")).toBeInTheDocument()
  })

  await waitFor(() => {
    expect(
      screen.getByText("Is there a customer table in the prod namespace?"),
    ).toBeTruthy()
  })
})
