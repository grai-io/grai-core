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
import useWorkspace from "helpers/useWorkspace"
import SourceNode from "./SourceNode"

export type SourceGraph = {
  id: string
  name: string
  icon: string | null
  targets: string[]
}[]

type GraphProps = {
  sourceGraph: SourceGraph
}

const elk = new ELK()

const defaultOptions = {
  "elk.algorithm": "layered",
  "elk.layered.spacing.nodeNodeBetweenLayers": 100,
  "elk.spacing.nodeNode": 80,
}

const nodeTypes = {
  custom: SourceNode,
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
          width: 300,
          height: 68,
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
  workspaceNavigate,
}: {
  initialNodes: Node[]
  initialEdges: Edge[]
  workspaceNavigate: (path: string) => void
}) => {
  const [nodes, , onNodesChange] = useNodesState(initialNodes)
  const [edges, , onEdgesChange] = useEdgesState(initialEdges)
  const { getLayoutedElements } = useLayoutedElements()

  useEffect(() => {
    let timer1 = setTimeout(
      () =>
        getLayoutedElements({
          "elk.algorithm": "layered",
          "elk.direction": "RIGHT",
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
      onNodeDoubleClick={(_event, node) =>
        workspaceNavigate(`sources/${node.data.id}`)
      }
      fitView
      proOptions={{ hideAttribution: true }}
      nodeTypes={nodeTypes}
    />
  )
}

const Graph: React.FC<GraphProps> = ({ sourceGraph }) => {
  const { workspaceNavigate } = useWorkspace()

  const initialNodes: Node[] = sourceGraph.map(source => ({
    id: source.id,
    position: { x: 0, y: 0 },
    data: { label: source.name, id: source.id, icon: source.icon },
    type: "custom",
  }))

  const initialEdges: Edge[] = sourceGraph.reduce<Edge[]>(
    (result, source) =>
      result.concat(
        source.targets
          .filter(target => source.id !== target)
          .map(target => ({
            id: `${source.id}-${target}`,
            source: source.id,
            target,
          })),
      ),
    [],
  )

  return (
    <ReactFlowProvider>
      <LayoutFlow
        initialNodes={initialNodes}
        initialEdges={initialEdges}
        workspaceNavigate={workspaceNavigate}
      />
    </ReactFlowProvider>
  )
}

export default Graph
