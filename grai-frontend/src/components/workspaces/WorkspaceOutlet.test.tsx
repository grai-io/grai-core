import { render } from "testing"
import WorkspaceOutlet from "./WorkspaceOutlet"

test("renders", async () => {
  render(<WorkspaceOutlet />, {
    withRouter: true,
  })
})
