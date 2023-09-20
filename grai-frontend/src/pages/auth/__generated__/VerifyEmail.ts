/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: VerifyEmail
// ====================================================

export interface VerifyEmail_verifyEmail {
  __typename: "User";
  id: any;
}

export interface VerifyEmail {
  verifyEmail: VerifyEmail_verifyEmail;
}

export interface VerifyEmailVariables {
  uid: string;
  token: string;
}
