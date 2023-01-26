import React, { ReactNode, Suspense } from "react"
import { Outlet } from "react-router-dom"

type SuspenseOutletProps = {
  fallback?: ReactNode
}

const SuspenseOutlet: React.FC<SuspenseOutletProps> = ({ fallback }) => (
  <Suspense fallback={fallback}>
    <Outlet />
  </Suspense>
)

export default SuspenseOutlet
