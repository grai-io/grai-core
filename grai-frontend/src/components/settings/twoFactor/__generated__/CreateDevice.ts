/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateDevice
// ====================================================

export interface CreateDevice_createDevice {
  __typename: "DeviceWithUrl";
  id: string;
  name: string;
  config_url: string;
}

export interface CreateDevice {
  createDevice: CreateDevice_createDevice;
}

export interface CreateDeviceVariables {
  name: string;
}
