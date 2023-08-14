import React, { useCallback, useEffect } from "react"
import ELK, { ElkNode, LayoutOptions } from "elkjs/lib/elk.bundled.js"
import ReactFlow, {
  Edge,
  Node,
  ReactFlowProvider,
  useEdgesState,
  useNodesState,
  useReactFlow,
} from "reactflow"
import "reactflow/dist/style.css"
import notEmpty from "helpers/notEmpty"

interface SourceGraph {
  [key: string]: string[]
}

type GraphProps = {
  sourceGraph: SourceGraph
}

const elk = new ELK()

const defaultOptions = {
  "elk.algorithm": "layered",
  "elk.layered.spacing.nodeNodeBetweenLayers": 100,
  "elk.spacing.nodeNode": 80,
}

const useLayoutedElements = () => {
  const { getNodes, setNodes, getEdges, fitView } = useReactFlow()

  const getLayoutedElements = useCallback(
    (options: LayoutOptions) => {
      const nodes = getNodes()

      const layoutOptions = { ...defaultOptions, ...options }
      const graph: any = {
        id: "root",
        layoutOptions: layoutOptions,
        children: nodes.map(node => ({
          ...node,
          width: node.width ?? undefined,
          height: node.height ?? undefined,
        })),
        edges: getEdges(),
      }

      elk.layout(graph).then(({ children }) => {
        const newNodes: Node[] =
          children
            ?.map((child: ElkNode) => {
              const initialNode = nodes.find(node => node.id === child.id)

              if (!initialNode) return undefined

              return {
                ...initialNode,
                position: {
                  x: child.x ?? 0,
                  y: child.y ?? 0,
                },
              }
            })
            .filter(notEmpty) ?? []

        setNodes(newNodes)
        window.requestAnimationFrame(() => {
          fitView()
        })
      })
    },
    [fitView, getEdges, getNodes, setNodes],
  )

  return { getLayoutedElements }
}

const LayoutFlow = ({
  initialNodes,
  initialEdges,
}: {
  initialNodes: Node[]
  initialEdges: Edge[]
}) => {
  const [nodes, , onNodesChange] = useNodesState(initialNodes)
  const [edges, , onEdgesChange] = useEdgesState(initialEdges)
  const { getLayoutedElements } = useLayoutedElements()

  useEffect(() => {
    let timer1 = setTimeout(
      () =>
        getLayoutedElements({
          "elk.algorithm": "layered",
          "elk.direction": "DOWN",
        }),
      1,
    )

    return () => {
      clearTimeout(timer1)
    }
  }, [getLayoutedElements])

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      fitView
      proOptions={{ hideAttribution: true }}
    />
  )
}

const Graph: React.FC<GraphProps> = ({ sourceGraph }) => {
  const initialNodes: Node[] = Array.from(
    new Set(Object.values(sourceGraph).flat()),
  ).map(name => ({
    id: name,
    position: { x: 0, y: 0 },
    data: { label: name },
  }))

  const initialEdges: Edge[] = Object.entries(sourceGraph).reduce<Edge[]>(
    (result, [source, targets]) =>
      result.concat(
        targets
          .filter(target => source !== target)
          .map(target => ({
            id: `${source}-${target}`,
            source,
            target,
          })),
      ),
    [],
  )

  return (
    <ReactFlowProvider>
      <LayoutFlow initialNodes={initialNodes} initialEdges={initialEdges} />
    </ReactFlowProvider>
  )
}

export default Graph
