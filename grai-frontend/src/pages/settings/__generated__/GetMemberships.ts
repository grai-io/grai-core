/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetMemberships
// ====================================================

export interface GetMemberships_workspace_memberships_user {
  __typename: "User";
  id: any;
  username: string | null;
}

export interface GetMemberships_workspace_memberships {
  __typename: "Membership";
  id: any;
  role: string;
  user: GetMemberships_workspace_memberships_user;
  createdAt: any;
}

export interface GetMemberships_workspace {
  __typename: "Workspace";
  id: any;
  memberships: GetMemberships_workspace_memberships[];
}

export interface GetMemberships {
  workspace: GetMemberships_workspace;
}

export interface GetMembershipsVariables {
  workspaceId: string;
}
