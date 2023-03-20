/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateMemberships
// ====================================================

export interface CreateMemberships_createMemberships_user {
  __typename: "User";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface CreateMemberships_createMemberships {
  __typename: "Membership";
  id: any;
  role: string;
  user: CreateMemberships_createMemberships_user;
  is_active: boolean;
  created_at: any;
}

export interface CreateMemberships {
  createMemberships: CreateMemberships_createMemberships[];
}

export interface CreateMembershipsVariables {
  role: string;
  emails: string[];
  workspaceId: string;
}
