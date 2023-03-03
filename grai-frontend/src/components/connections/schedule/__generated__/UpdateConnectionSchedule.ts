/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateConnectionSchedule
// ====================================================

export interface UpdateConnectionSchedule_updateConnection {
  __typename: "Connection";
  id: any;
  namespace: string;
  name: string;
  metadata: any;
  schedules: any | null;
  is_active: boolean;
  created_at: any;
  updated_at: any;
}

export interface UpdateConnectionSchedule {
  updateConnection: UpdateConnectionSchedule_updateConnection;
}

export interface UpdateConnectionScheduleVariables {
  id: string;
  namespace: string;
  name: string;
  metadata: any;
  secrets?: any | null;
  schedules?: any | null;
  is_active: boolean;
}
