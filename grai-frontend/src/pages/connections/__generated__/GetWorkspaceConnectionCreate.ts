/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceConnectionCreate
// ====================================================

export interface GetWorkspaceConnectionCreate_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
}

export interface GetWorkspaceConnectionCreate_connectors {
  __typename: "Connector";
  id: any;
  priority: number | null;
  name: string;
  metadata: any;
  icon: string | null;
  category: string | null;
  status: string;
}

export interface GetWorkspaceConnectionCreate {
  workspace: GetWorkspaceConnectionCreate_workspace;
  connectors: GetWorkspaceConnectionCreate_connectors[];
}

export interface GetWorkspaceConnectionCreateVariables {
  organisationName: string;
  workspaceName: string;
}
