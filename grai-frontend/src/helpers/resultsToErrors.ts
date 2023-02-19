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
}

const resultsToErrors = (results: Result[] | undefined): Error[] | null =>
  results
    ? results.map(result => ({
        source: result.node.name,
        destination: result.failing_node.name,
        test: result.type,
        message: result.message,
      }))
    : null

export default resultsToErrors
