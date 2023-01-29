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
  first_name: string;
  last_name: string;
}

export interface GetMemberships_workspace_memberships {
  __typename: "Membership";
  id: any;
  role: string;
  user: GetMemberships_workspace_memberships_user;
  is_active: boolean;
  created_at: any;
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
  organisationName: string;
  workspaceName: string;
}
