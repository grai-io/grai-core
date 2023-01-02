/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateMembership
// ====================================================

export interface CreateMembership_createMembership_user {
  __typename: "User";
  id: any;
  username: string | null;
}

export interface CreateMembership_createMembership {
  __typename: "Membership";
  id: any;
  role: string;
  user: CreateMembership_createMembership_user;
}

export interface CreateMembership {
  createMembership: CreateMembership_createMembership;
}

export interface CreateMembershipVariables {
  role: string;
  email: string;
  workspaceId: string;
}
