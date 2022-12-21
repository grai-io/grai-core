import React from "react"
import { Routes as BrowerRoutes, Route } from "react-router-dom"
import GuestRoute from "./components/auth/GuestRoute"
import PrivateRoute from "./components/auth/PrivateRoute"
import Login from "./pages/auth/Login"
import Home from "./pages/Home"
import Nodes from "./pages/nodes/Nodes"
import Node from "./pages/nodes/Node"
import NotFound from "./pages/NotFound"
import Connections from "./pages/connections/Connections"
import ConnectionCreate from "./pages/connections/ConnectionCreate"
import Connection from "./pages/connections/Connection"
import Graph from "./pages/Graph"
import Index from "./pages/Index"
import Workspaces from "./pages/workspaces/Workspaces"
import Settings from "./pages/settings/Settings"
import ApiKeys from "./pages/settings/ApiKeys"
import WorkspaceSettings from "pages/settings/WorkspaceSettings"
import Memberships from "pages/settings/Memberships"

const Routes: React.FC = () => (
  <BrowerRoutes>
    <Route element={<PrivateRoute />}>
      <Route index element={<Index />} />
      <Route path="workspaces">
        <Route index element={<Workspaces />} />
        <Route path=":workspaceId">
          <Route index element={<Home />} />
          <Route path="graph" element={<Graph />} />
          <Route path="nodes">
            <Route index element={<Nodes />} />
            <Route path=":nodeId" element={<Node />} />
          </Route>
          <Route path="connections">
            <Route index element={<Connections />} />
            <Route path="create" element={<ConnectionCreate />} />
            <Route path=":connectionId" element={<Connection />} />
          </Route>
          <Route path="settings">
            <Route index element={<Settings />} />
            <Route path="api-keys" element={<ApiKeys />} />
            <Route path="workspace" element={<WorkspaceSettings />} />
            <Route path="memberships" element={<Memberships />} />
          </Route>
        </Route>
      </Route>
    </Route>

    <Route element={<GuestRoute />}>
      <Route path="/login" element={<Login />} />
    </Route>

    <Route path="*" element={<NotFound />} />
  </BrowerRoutes>
)

export default Routes
