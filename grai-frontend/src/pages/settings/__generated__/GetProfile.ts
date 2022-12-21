/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetProfile
// ====================================================

export interface GetProfile_profile {
  __typename: "User";
  id: any;
  username: string | null;
  firstName: string;
  lastName: string;
}

export interface GetProfile {
  profile: GetProfile_profile;
}
