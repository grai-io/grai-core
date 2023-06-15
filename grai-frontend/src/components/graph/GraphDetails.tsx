import React from "react"
import { ReactFlowState, useStore } from "reactflow"

const transformSelector = (state: ReactFlowState) => state.transform

const GraphDetails: React.FC = () => {
  const transform = useStore(transformSelector)
  const width = useStore(state => state.width)
  const height = useStore(state => state.height)

  return (
    <aside>
      <div className="description">
        This is an example of how you can access the internal state outside of
        the ReactFlow component.
      </div>
      <div className="title">Zoom & pan transform</div>
      <div className="transform">
        [{transform[0].toFixed(2)}, {transform[1].toFixed(2)},{" "}
        {transform[2].toFixed(2)}]
      </div>
      {width},{height}
      {/* <div className="title">Nodes</div> */}
      {/* {nodes.map((node) => (
        <div key={node.id}>
          Node {node.id} - x: {node.position.x.toFixed(2)}, y: {node.position.y.toFixed(2)}
        </div>
      ))} */}
      {/* <div className="selectall">
        <button onClick={selectAll}>select all nodes</button>
      </div> */}
    </aside>
  )
}

export default GraphDetails
