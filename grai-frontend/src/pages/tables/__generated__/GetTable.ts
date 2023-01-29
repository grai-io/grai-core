/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTable
// ====================================================

export interface GetTable_workspace_table_columns {
  __typename: "Column";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTable_workspace_table_source_tables {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTable_workspace_table_destination_tables {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTable_workspace_table {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  data_source: string;
  metadata: any;
  columns: GetTable_workspace_table_columns[];
  source_tables: GetTable_workspace_table_source_tables[];
  destination_tables: GetTable_workspace_table_destination_tables[];
}

export interface GetTable_workspace {
  __typename: "Workspace";
  id: any;
  table: GetTable_workspace_table;
}

export interface GetTable {
  workspace: GetTable_workspace;
}

export interface GetTableVariables {
  workspaceId: string;
  tableId: string;
}
