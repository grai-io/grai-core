import { WorkspaceContext } from "components/utils/WorkspaceProvider"
import { useContext } from "react"

const useWorkspace = () => useContext(WorkspaceContext)

export default useWorkspace
