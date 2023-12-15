import { render, screen } from "@testing-library/react"
import App from "./App"

test("renders", async () => {
  render(<App />)

  await screen.findByText(/Welcome back!/i)
})
