/* istanbul ignore file */
import { WorkspaceContext } from "components/utils/WorkspaceProvider"
import React, { ReactNode, useState } from "react"
import { Outlet, useNavigate } from "react-router-dom"

const AuthMock: React.FC = () => {
  const navigate = useNavigate()

  return (
    <WorkspaceContext.Provider
      value={{
        workspaceName: "workspace",
        organisationName: "organisation",
        routePrefix: "/organisation/workspace",
        workspaceNavigate: (route?: string | null) =>
          navigate(`/organisation/workspace/${route}`),
      }}
    >
      <Outlet />
    </WorkspaceContext.Provider>
  )
}

export default AuthMock
