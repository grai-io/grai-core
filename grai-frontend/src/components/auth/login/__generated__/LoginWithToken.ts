/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: LoginWithToken
// ====================================================

export interface LoginWithToken_loginWithToken {
  __typename: "User";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface LoginWithToken {
  loginWithToken: LoginWithToken_loginWithToken;
}

export interface LoginWithTokenVariables {
  username: string;
  password: string;
  deviceId: string;
  token: string;
}
