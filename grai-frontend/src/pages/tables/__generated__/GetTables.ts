/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTables
// ====================================================

export interface GetTables_workspace_tables {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  data_source: string;
  metadata: any;
}

export interface GetTables_workspace {
  __typename: "Workspace";
  id: any;
  tables: GetTables_workspace_tables[];
}

export interface GetTables {
  workspace: GetTables_workspace;
}

export interface GetTablesVariables {
  organisationName: string;
  workspaceName: string;
}
