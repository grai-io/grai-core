/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: Login
// ====================================================

export interface Login_login_Profile {
  __typename: "Profile";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface Login_login_DeviceDataWrapper_data {
  __typename: "Device";
  id: string;
  name: string;
}

export interface Login_login_DeviceDataWrapper {
  __typename: "DeviceDataWrapper";
  data: Login_login_DeviceDataWrapper_data[];
}

export type Login_login = Login_login_Profile | Login_login_DeviceDataWrapper;

export interface Login {
  login: Login_login;
}

export interface LoginVariables {
  username: string;
  password: string;
}
