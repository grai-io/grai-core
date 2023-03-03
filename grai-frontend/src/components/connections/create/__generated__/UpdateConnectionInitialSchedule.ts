/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateConnectionInitialSchedule
// ====================================================

export interface UpdateConnectionInitialSchedule_updateConnection {
  __typename: "Connection";
  id: any;
  schedules: any | null;
  is_active: boolean;
}

export interface UpdateConnectionInitialSchedule {
  updateConnection: UpdateConnectionInitialSchedule_updateConnection;
}

export interface UpdateConnectionInitialScheduleVariables {
  id: string;
  schedules?: any | null;
  is_active: boolean;
}
