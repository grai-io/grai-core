import { useContext } from "react"
import { WorkspaceContext } from "components/utils/WorkspaceProvider"

const useWorkspace = () => useContext(WorkspaceContext)

export default useWorkspace
