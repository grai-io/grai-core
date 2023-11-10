import { render, screen, waitFor } from "testing"
import TooltipWrap from "./TooltipWrap"

test("renders", async () => {
  render(
    <TooltipWrap title="title" show>
      <>Hello</>
    </TooltipWrap>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Hello")).toBeTruthy()
  })
})

test("renders no show", async () => {
  render(
    <TooltipWrap title={null} show={false}>
      <>Hello</>
    </TooltipWrap>,
    {
      withRouter: true,
    },
  )

  await waitFor(() => {
    expect(screen.getByText("Hello")).toBeTruthy()
  })
})
