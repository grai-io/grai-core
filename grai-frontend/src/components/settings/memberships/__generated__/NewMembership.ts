/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL fragment: NewMembership
// ====================================================

export interface NewMembership_user {
  __typename: "User";
  id: any;
  username: string | null;
}

export interface NewMembership {
  __typename: "Membership";
  id: any;
  role: string;
  user: NewMembership_user;
}
