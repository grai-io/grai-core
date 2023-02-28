import { Error } from "components/graph/Graph"

interface Node {
  id: string
  name: string
  namespace: string
}

export interface Result {
  node: Node
  node_name: string
  failing_node: Node
  failing_node_name: string
  type: string
  message: string
  test_pass: boolean
}

const resultsToErrors = (results: Result[] | undefined): Error[] | null =>
  results
    ? results.map(result => ({
        source: result.node.name,
        destination: result.failing_node.name,
        test: result.type,
        message: result.message,
        test_pass: result.test_pass,
      }))
    : null

export default resultsToErrors
