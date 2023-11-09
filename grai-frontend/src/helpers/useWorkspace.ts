import { useContext } from "react"
import { WorkspaceContext } from "components/workspaces/WorkspaceProvider"

const useWorkspace = () => useContext(WorkspaceContext)

export default useWorkspace
