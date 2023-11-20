/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: Verify
// ====================================================

export interface Verify_verifyEmail {
  __typename: "Profile";
  id: any;
}

export interface Verify {
  verifyEmail: Verify_verifyEmail;
}

export interface VerifyVariables {
  uid: string;
  token: string;
}
