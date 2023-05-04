import { render } from "testing"
import DataSourceIcon from "./DataSourceIcon"

test("renders", async () => {
  render(<DataSourceIcon dataSource="grai-source-dbt" />)
})

test("renders empty", async () => {
  render(<DataSourceIcon dataSource="none" />)
})
