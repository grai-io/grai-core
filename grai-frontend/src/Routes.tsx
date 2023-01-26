import React, { lazy, Suspense } from "react"
import { Routes as BrowerRoutes, Route } from "react-router-dom"
import GuestRoute from "./components/auth/GuestRoute"
import PrivateRoute from "./components/auth/PrivateRoute"
import NotFound from "./pages/NotFound"
import PageLayout from "components/layout/PageLayout"
import Loading from "components/layout/Loading"
import SuspenseOutlet from "components/utils/SuspenseOutlet"
import SettingsLayout from "components/settings/SettingsLayout"

const Index = lazy(() => import("./pages/Index"))
const Workspaces = lazy(() => import("./pages/workspaces/Workspaces"))
const Home = lazy(() => import("./pages/Home"))
const Graph = lazy(() => import("./pages/Graph"))
const Nodes = lazy(() => import("./pages/nodes/Nodes"))
const Node = lazy(() => import("./pages/nodes/Node"))
const Run = lazy(() => import("./pages/runs/Run"))
const Connections = lazy(() => import("./pages/connections/Connections"))
const ConnectionCreate = lazy(
  () => import("./pages/connections/ConnectionCreate")
)
const Connection = lazy(() => import("./pages/connections/Connection"))

const Settings = lazy(() => import("./pages/settings/Settings"))
const ProfileSettings = lazy(() => import("./pages/settings/ProfileSettings"))
const PasswordSettings = lazy(() => import("./pages/settings/PasswordSettings"))
const ApiKeys = lazy(() => import("./pages/settings/ApiKeys"))
const WorkspaceSettings = lazy(
  () => import("./pages/settings/WorkspaceSettings")
)
const Memberships = lazy(() => import("./pages/settings/Memberships"))

const Login = lazy(() => import("./pages/auth/Login"))
const ForgotPassword = lazy(() => import("./pages/auth/ForgotPassword"))
const PasswordReset = lazy(() => import("./pages/auth/PasswordReset"))
const CompleteSignup = lazy(() => import("./pages/auth/CompleteSignup"))

const Routes: React.FC = () => (
  <Suspense fallback={<Loading />}>
    <BrowerRoutes>
      <Route element={<PrivateRoute />}>
        <Route element={<SuspenseOutlet fallback={<PageLayout loading />} />}>
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
              <Route path="runs">
                <Route path=":runId" element={<Run />} />
              </Route>
              <Route path="connections">
                <Route index element={<Connections />} />
                <Route path="create" element={<ConnectionCreate />} />
                <Route path=":connectionId" element={<Connection />} />
              </Route>
              <Route
                path="settings"
                element={
                  <SuspenseOutlet
                    fallback={
                      <SettingsLayout>
                        <Loading />
                      </SettingsLayout>
                    }
                  />
                }
              >
                <Route index element={<Settings />} />
                <Route path="profile" element={<ProfileSettings />} />
                <Route path="password" element={<PasswordSettings />} />
                <Route path="api-keys" element={<ApiKeys />} />
                <Route path="workspace" element={<WorkspaceSettings />} />
                <Route path="memberships" element={<Memberships />} />
              </Route>
            </Route>
          </Route>
        </Route>
      </Route>

      <Route element={<GuestRoute />}>
        <Route path="/login" element={<Login />} />
        <Route path="/forgot" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<PasswordReset />} />
        <Route path="/complete-signup" element={<CompleteSignup />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </BrowerRoutes>
  </Suspense>
)

export default Routes
