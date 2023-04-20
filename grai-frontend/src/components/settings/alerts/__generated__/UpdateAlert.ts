/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateAlert
// ====================================================

export interface UpdateAlert_updateAlert {
  __typename: "Alert";
  id: any;
  name: string;
  channel: string;
  channel_metadata: any;
  triggers: any;
  is_active: boolean;
}

export interface UpdateAlert {
  updateAlert: UpdateAlert_updateAlert;
}

export interface UpdateAlertVariables {
  id: string;
  name: string;
  channel_metadata: any;
  triggers: any;
  is_active: boolean;
}
