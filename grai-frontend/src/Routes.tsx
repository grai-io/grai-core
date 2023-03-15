/* istanbul ignore file */
import React, { lazy, Suspense } from "react"
import * as Sentry from "@sentry/react"
import { Routes as BrowerRoutes, Route } from "react-router-dom"
import WorkspaceRedirect from "pages/workspaces/WorkspaceRedirect"
import Loading from "components/layout/Loading"
import PageLayout from "components/layout/PageLayout"
import SettingsLayout from "components/settings/SettingsLayout"
import SuspenseOutlet from "components/utils/SuspenseOutlet"
import WorkspaceProvider from "components/utils/WorkspaceProvider"
import GuestRoute from "./components/auth/GuestRoute"
import PrivateRoute from "./components/auth/PrivateRoute"
import NotFound from "./pages/NotFound"

const Index = lazy(() => import("./pages/Index"))
const Workspaces = lazy(() => import("./pages/workspaces/Workspaces"))
const Home = lazy(() => import("./pages/Home"))
const Graph = lazy(() => import("./pages/Graph"))
const Tables = lazy(() => import("./pages/tables/Tables"))
const Table = lazy(() => import("./pages/tables/Table"))
const Runs = lazy(() => import("./pages/runs/Runs"))
const Run = lazy(() => import("./pages/runs/Run"))

const Reports = lazy(() => import("./pages/reports/Reports"))
const Report = lazy(() => import("./pages/reports/Report"))
const Repositories = lazy(() => import("./pages/reports/Repositories"))
const Commits = lazy(() => import("./pages/reports/Commits"))
const PullRequests = lazy(() => import("./pages/reports/PullRequests"))
const PullRequest = lazy(() => import("./pages/reports/PullRequest"))
const Commit = lazy(() => import("./pages/reports/Commit"))

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
const PostInstall = lazy(() => import("./pages/PostInstall"))

const Login = lazy(() => import("./pages/auth/Login"))
const Register = lazy(() => import("./pages/auth/Register"))
const ForgotPassword = lazy(() => import("./pages/auth/ForgotPassword"))
const PasswordReset = lazy(() => import("./pages/auth/PasswordReset"))
const CompleteSignup = lazy(() => import("./pages/auth/CompleteSignup"))

const SentryRoutes = Sentry.withSentryReactRouterV6Routing(BrowerRoutes)

const Routes: React.FC = () => (
  <Suspense fallback={<Loading />}>
    <SentryRoutes>
      <Route element={<PrivateRoute />}>
        <Route element={<SuspenseOutlet fallback={<PageLayout loading />} />}>
          <Route index element={<Index />} />
          <Route path="/workspaces">
            <Route index element={<Workspaces />} />
            <Route path=":workspaceId" element={<WorkspaceRedirect />} />
            <Route path=":workspaceId/:rest*" element={<WorkspaceRedirect />} />
          </Route>
          <Route
            path=":organisationName/:workspaceName"
            element={<WorkspaceProvider />}
          >
            <Route index element={<Home />} />
            <Route path="graph" element={<Graph />} />
            <Route path="tables">
              <Route index element={<Tables />} />
              <Route path=":tableId" element={<Table />} />
            </Route>
            <Route path="runs">
              <Route index element={<Runs />} />
              <Route path=":runId" element={<Run />} />
            </Route>
            <Route path="reports">
              <Route index element={<Reports />} />
              <Route path=":type/:owner">
                <Route index element={<Repositories />} />
                <Route path=":repo">
                  <Route index element={<Commits />} />
                  <Route path=":reportId" element={<Report />} />
                  <Route path="pulls">
                    <Route index element={<PullRequests />} />
                    <Route path=":reference" element={<PullRequest />} />
                  </Route>
                  <Route path="commits">
                    <Route index element={<Commits />} />
                    <Route path=":reference" element={<Commit />} />
                  </Route>
                  <Route path="*" element={<NotFound />} />
                </Route>
              </Route>
              <Route path=":reportId" element={<Report />} />
              <Route path="*" element={<NotFound />} />
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
              <Route path="*" element={<NotFound />} />
            </Route>
            <Route path="*" element={<NotFound />} />
          </Route>
          <Route path="post-install" element={<PostInstall />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Route>

      <Route element={<GuestRoute />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<PasswordReset />} />
        <Route path="/complete-signup" element={<CompleteSignup />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </SentryRoutes>
  </Suspense>
)

export default Routes
