import { render, screen } from "testing"
import ConnectionConfiguration from "./ConnectionConfiguration"

const connection = {
  id: "1",
  schedules: null,
  is_active: false,
  namespace: "default",
  name: "c1",
  metadata: {},
  connector: {
    id: "1",
    name: "c1",
    metadata: null,
  },
}

test("renders", async () => {
  render(<ConnectionConfiguration connection={connection} />)

  expect(screen.getByText("Namespace")).toBeTruthy()
})
