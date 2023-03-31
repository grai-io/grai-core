/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetMemberships
// ====================================================

export interface GetMemberships_workspace_memberships_data_user {
  __typename: "User";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface GetMemberships_workspace_memberships_data {
  __typename: "Membership";
  id: any;
  role: string;
  user: GetMemberships_workspace_memberships_data_user;
  is_active: boolean;
  created_at: any;
}

export interface GetMemberships_workspace_memberships_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetMemberships_workspace_memberships {
  __typename: "MembershipPagination";
  data: GetMemberships_workspace_memberships_data[];
  meta: GetMemberships_workspace_memberships_meta;
}

export interface GetMemberships_workspace {
  __typename: "Workspace";
  id: any;
  memberships: GetMemberships_workspace_memberships;
}

export interface GetMemberships {
  workspace: GetMemberships_workspace;
}

export interface GetMembershipsVariables {
  organisationName: string;
  workspaceName: string;
}
