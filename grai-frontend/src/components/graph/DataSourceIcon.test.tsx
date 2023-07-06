import { render } from "testing"
import DataSourceIcon from "./DataSourceIcon"

test("renders", async () => {
  render(<DataSourceIcon dataSource="grai-source-dbt" />)
})

test("renders empty", async () => {
  render(<DataSourceIcon dataSource="none" />)
})

test("renders small", async () => {
  render(<DataSourceIcon dataSource="grai-source-dbt" size="small" />)
})

test("renders grayscale", async () => {
  render(<DataSourceIcon dataSource="grai-source-dbt" grayscale />)
})

test("renders noBorder", async () => {
  render(<DataSourceIcon dataSource="grai-source-dbt" noBorder />)
})

test("renders noMargin", async () => {
  render(<DataSourceIcon dataSource="grai-source-dbt" noMargin />)
})
