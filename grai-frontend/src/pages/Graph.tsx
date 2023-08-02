import React, { useCallback, useEffect, useRef, useState } from "react"
import { gql, useLazyQuery } from "@apollo/client"
import { useSearchParams } from "react-router-dom"
import { Viewport } from "reactflow"
import theme from "theme"
import useWorkspace from "helpers/useWorkspace"
import GraphComponent, {
  ResultError,
  Table,
} from "components/graph/GraphComponent"
import useFilters from "components/graph/useFilters"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"
import {
  GetTablesAndEdges,
  GetTablesAndEdgesVariables,
} from "./__generated__/GetTablesAndEdges"

export const GET_TABLES_AND_EDGES = gql`
  query GetTablesAndEdges(
    $organisationName: String!
    $workspaceName: String!
    $filters: GraphFilter
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      graph(filters: $filters) {
        id
        name
        display_name
        namespace
        data_source
        x
        y
        columns {
          id
          name
          display_name
          destinations
        }
        destinations
      }
    }
  }
`

type GraphProps = {
  alwaysShow?: boolean
}

const Graph: React.FC<GraphProps> = ({ alwaysShow }) => {
  const { organisationName, workspaceName } = useWorkspace()
  const [searchParams] = useSearchParams()
  const [tables, setTables] = useState<Table[]>([])
  const ref = useRef<HTMLDivElement>(null)

  const { filters, setFilters } = useFilters()

  const [loadGraph, { loading, error, refetch }] = useLazyQuery<
    GetTablesAndEdges,
    GetTablesAndEdgesVariables
  >(GET_TABLES_AND_EDGES)

  const handleMove = useCallback(
    (viewport: Viewport) =>
      loadGraph({
        variables: {
          organisationName,
          workspaceName,
          filters: {
            filters,
            min_x: Math.round((-viewport.x - 500) / viewport.zoom),
            max_x: Math.round(
              (-viewport.x + (ref.current?.clientWidth ?? 0)) / viewport.zoom,
            ),
            min_y: Math.round(-viewport.y / viewport.zoom),
            max_y: Math.round(
              (-viewport.y + (ref.current?.clientHeight ?? 0)) / viewport.zoom,
            ),
          },
        },
      }).then(res => setTables(res.data?.workspace.graph ?? [])),
    [filters, loadGraph, organisationName, workspaceName],
  )

  useEffect(() => {
    handleMove({
      x: 0,
      y: 0,
      zoom: 1,
    })
  }, [handleMove])

  if (error) return <GraphError error={error} />

  const errorsQS = searchParams.get("errors")
  const errors: ResultError[] | null = errorsQS ? JSON.parse(errorsQS) : null
  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && !!errors

  const handleRefresh = () => refetch()

  return (
    <PageLayout>
      <div
        ref={ref}
        style={{
          height: "100vh",
          width: "100%",
          backgroundColor: theme.palette.grey[100],
        }}
      >
        <GraphComponent
          tables={tables}
          errors={errors}
          limitGraph={limitGraph}
          alwaysShow={alwaysShow}
          onMove={handleMove}
          onRefresh={handleRefresh}
          refreshLoading={loading}
          filters={filters ?? []}
          setFilters={setFilters}
        />
      </div>
    </PageLayout>
  )
}

export default Graph
