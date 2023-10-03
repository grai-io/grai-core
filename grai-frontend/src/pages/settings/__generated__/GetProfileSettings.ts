/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetProfileSettings
// ====================================================

export interface GetProfileSettings_profile {
  __typename: "Profile";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface GetProfileSettings {
  profile: GetProfileSettings_profile;
}
