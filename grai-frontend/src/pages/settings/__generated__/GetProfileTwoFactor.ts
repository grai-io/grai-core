/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetProfileTwoFactor
// ====================================================

export interface GetProfileTwoFactor_profile_devices_data {
  __typename: "Device";
  id: string;
  name: string;
}

export interface GetProfileTwoFactor_profile_devices {
  __typename: "DeviceDataWrapper";
  data: GetProfileTwoFactor_profile_devices_data[];
}

export interface GetProfileTwoFactor_profile {
  __typename: "Profile";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
  devices: GetProfileTwoFactor_profile_devices;
}

export interface GetProfileTwoFactor {
  profile: GetProfileTwoFactor_profile;
}
