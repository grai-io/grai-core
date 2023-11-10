/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CompleteSignup
// ====================================================

export interface CompleteSignup_completeSignup {
  __typename: "Profile";
  id: any;
}

export interface CompleteSignup {
  completeSignup: CompleteSignup_completeSignup;
}

export interface CompleteSignupVariables {
  token: string;
  uid: string;
  first_name: string;
  last_name: string;
  password: string;
}
