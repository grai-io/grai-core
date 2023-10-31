/* istanbul ignore file */
import React, { ReactElement, ReactNode } from "react"
import { MockedResponse } from "@apollo/client/testing"
import { Theme, ThemeProvider } from "@mui/material"
import { LocalizationProvider } from "@mui/x-date-pickers"
import { AdapterLuxon } from "@mui/x-date-pickers/AdapterLuxon"
import { render, RenderOptions } from "@testing-library/react"
import casual from "casual"
import { cache } from "client"
import { ConfirmProvider } from "material-ui-confirm"
import { SnackbarProvider } from "notistack"
import { HelmetProvider } from "react-helmet-async"
import { MemoryRouter, Route, Routes, Location } from "react-router-dom"
import defaultTheme from "theme"
import GuestRoute from "components/auth/GuestRoute"
import WorkspaceProvider from "components/utils/WorkspaceProvider"
import AuthMock from "./AuthMock"
import AutoMockedProvider from "./AutoMockedProvider"

const mockResolvers = {
  Date: () => "2019-12-31",
  DateTime: () => "2019-07-24 11:14:37",
  PaginatorInfo: () => ({ currentPage: 1, total: 20 }),
  JSON: () => ({}),
  UUID: () => casual.uuid,
  ID: () => casual.uuid,
  Alert: () => ({
    id: casual.uuid,
  }),
  WorkspaceAPIKey: () => ({
    id: casual.uuid,
  }),
  BaseTable: () => ({
    id: casual.uuid,
  }),
  Column: () => ({
    id: casual.uuid,
  }),
  Connection: () => ({
    id: casual.uuid,
    name: "Connection 1",
  }),
  Connector: () => ({
    id: casual.uuid,
  }),
  Edge: () => ({
    id: casual.uuid,
  }),
  Event: () => ({
    id: casual.uuid,
  }),
  Node: () => ({
    id: casual.uuid,
    metadata: {
      grai: {
        node_type: "Table",
      },
    },
  }),
  Repository: () => ({
    id: casual.uuid,
    repo: casual.word,
  }),
  PullRequest: () => ({
    id: casual.uuid,
    reference: casual.integer(1, 100),
  }),
  Branch: () => ({
    id: casual.uuid,
    reference: casual.integer(1, 100),
  }),
  Commit: () => ({
    id: casual.uuid,
    reference: casual.integer(1, 100),
  }),
  Filter: () => ({
    id: casual.uuid,
    metadata: [],
  }),
  GraphColumn: () => ({
    id: casual.uuid,
  }),
  GraphTable: () => ({
    id: casual.uuid,
  }),
  Membership: () => ({
    id: casual.uuid,
  }),
  Organisation: () => ({
    id: casual.uuid,
  }),
  Run: () => ({
    id: casual.uuid,
  }),
  Source: () => ({
    id: casual.uuid,
  }),
  StrDataWrapper: () => ({
    data: ["tag1", "tag2"],
  }),
  Table: () => ({
    id: casual.uuid,
  }),
  User: () => ({
    id: casual.uuid,
  }),
  Workspace: () => ({
    id: casual.uuid,
    source_graph: [],
  }),
}

type RouteType =
  | string
  | {
      path: string
      element: ReactNode
    }

type CustomRenderOptions = RenderOptions & {
  path?: string
  withRouter?: boolean
  route?: string | Partial<Location>
  routes?: RouteType[]
  initialEntries?: (string | Partial<Location>)[] | null
  loggedIn?: boolean
  guestRoute?: boolean
  mocks?: readonly MockedResponse<Record<string, any>>[]
  theme?: Theme
}

const customRender = (ui: ReactElement, options?: CustomRenderOptions) => {
  if (options?.withRouter || options?.path || options?.route || options?.routes)
    return renderWithRouter(ui, options)

  return basicRender(ui, options)
}

const basicRender = (
  ui: ReactElement,
  { loggedIn = true, mocks, theme }: CustomRenderOptions = {},
) =>
  render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <SnackbarProvider>
          <ConfirmProvider>
            <ThemeProvider theme={theme ?? defaultTheme}>
              <LocalizationProvider dateAdapter={AdapterLuxon}>
                <AuthMock initialLoggedIn={loggedIn}>
                  <AutoMockedProvider
                    mockResolvers={mockResolvers}
                    mocks={mocks}
                    cache={cache}
                  >
                    {props.children}
                  </AutoMockedProvider>
                </AuthMock>
              </LocalizationProvider>
            </ThemeProvider>
          </ConfirmProvider>
        </SnackbarProvider>
      </HelmetProvider>
    ),
  })

const renderWithRouter = (
  ui: ReactElement,
  {
    path = "/",
    route = "/",
    routes = [],
    initialEntries = null,
    loggedIn = true,
    guestRoute = false,
    mocks,
    theme,
  }: CustomRenderOptions = {},
) => {
  return render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <ThemeProvider theme={theme ?? defaultTheme}>
          <LocalizationProvider dateAdapter={AdapterLuxon}>
            <AutoMockedProvider
              mockResolvers={mockResolvers}
              mocks={mocks}
              cache={cache}
            >
              <MemoryRouter initialEntries={initialEntries ?? [route]}>
                <AuthMock initialLoggedIn={loggedIn}>
                  <SnackbarProvider maxSnack={3} hideIconVariant>
                    <ConfirmProvider>
                      <Routes>
                        <Route element={<WorkspaceProvider />}>
                          {guestRoute ? (
                            <Route element={<GuestRoute />}>
                              <Route path={path} element={props.children} />
                            </Route>
                          ) : (
                            <Route path={path} element={props.children} />
                          )}
                          {routes.map(route =>
                            typeof route === "string" ? (
                              <Route
                                key={route}
                                path={route}
                                element={<>New Page</>}
                              />
                            ) : (
                              <Route
                                key={route.path}
                                path={route.path}
                                element={route.element}
                              />
                            ),
                          )}
                        </Route>
                      </Routes>
                    </ConfirmProvider>
                  </SnackbarProvider>
                </AuthMock>
              </MemoryRouter>
            </AutoMockedProvider>
          </LocalizationProvider>
        </ThemeProvider>
      </HelmetProvider>
    ),
  })
}

export * from "@testing-library/react"
export { customRender as render }
