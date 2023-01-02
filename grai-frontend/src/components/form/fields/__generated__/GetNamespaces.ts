/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNamespaces
// ====================================================

export interface GetNamespaces_workspace_namespaces {
  __typename: "NamespaceType";
  id: string;
  name: string;
}

export interface GetNamespaces_workspace {
  __typename: "WorkspaceType";
  id: any;
  namespaces: GetNamespaces_workspace_namespaces[];
}

export interface GetNamespaces {
  workspace: GetNamespaces_workspace;
}

export interface GetNamespacesVariables {
  workspaceId: string;
}
