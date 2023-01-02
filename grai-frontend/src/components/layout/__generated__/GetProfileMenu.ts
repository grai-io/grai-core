/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetProfileMenu
// ====================================================

export interface GetProfileMenu_profile {
  __typename: "User";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface GetProfileMenu {
  profile: GetProfileMenu_profile;
}
