/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: ConfirmDevice
// ====================================================

export interface ConfirmDevice_confirmDevice {
  __typename: "Device";
  id: string;
}

export interface ConfirmDevice {
  confirmDevice: ConfirmDevice_confirmDevice;
}

export interface ConfirmDeviceVariables {
  deviceId: string;
  token: string;
}
