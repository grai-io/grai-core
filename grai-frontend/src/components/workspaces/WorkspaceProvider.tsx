/* istanbul ignore file */
import React, { createContext } from "react"
import { Outlet, useNavigate, useParams } from "react-router-dom"

type WorkspaceContextType = {
  workspaceName: string
  organisationName: string
  routePrefix: string
  workspaceNavigate: (route?: string | null) => void
}

export const WorkspaceContext = createContext<WorkspaceContextType>({
  workspaceName: "",
  organisationName: "",
  routePrefix: "",
  workspaceNavigate: () => {},
})

type WorkspaceProviderProps = {
  children?: React.ReactNode
}

const WorkspaceProvider: React.FC<WorkspaceProviderProps> = ({ children }) => {
  const { organisationName, workspaceName } = useParams()
  const navigate = useNavigate()

  const workspaceNavigate = (route?: string | null) =>
    navigate(`/${organisationName}/${workspaceName}/${route}`)

  const value = {
    workspaceName: workspaceName ?? "",
    organisationName: organisationName ?? "",
    routePrefix: `/${organisationName}/${workspaceName}`,
    workspaceNavigate,
  }

  return (
    <WorkspaceContext.Provider value={value}>
      {children ?? <Outlet />}
    </WorkspaceContext.Provider>
  )
}

export default WorkspaceProvider
