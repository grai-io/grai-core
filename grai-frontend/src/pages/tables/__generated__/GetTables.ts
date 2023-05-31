/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTables
// ====================================================

export interface GetTables_workspace_tables_data {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  metadata: any;
}

export interface GetTables_workspace_tables_meta {
  __typename: "PaginationResult";
  filtered: number;
  total: number;
}

export interface GetTables_workspace_tables {
  __typename: "TablePagination";
  data: GetTables_workspace_tables_data[];
  meta: GetTables_workspace_tables_meta;
}

export interface GetTables_workspace {
  __typename: "Workspace";
  id: any;
  tables: GetTables_workspace_tables;
}

export interface GetTables {
  workspace: GetTables_workspace;
}

export interface GetTablesVariables {
  organisationName: string;
  workspaceName: string;
  offset?: number | null;
  search?: string | null;
}
