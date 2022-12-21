/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdatePassword
// ====================================================

export interface UpdatePassword_updatePassword {
  __typename: "User";
  id: any;
}

export interface UpdatePassword {
  updatePassword: UpdatePassword_updatePassword;
}

export interface UpdatePasswordVariables {
  old_password: string;
  password: string;
}
