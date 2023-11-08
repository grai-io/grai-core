import { render } from "testing"
import PageLayoutOutlet from "./PageLayoutOutlet"

test("renders", async () => {
  render(<PageLayoutOutlet />, {
    withRouter: true,
  })
})
