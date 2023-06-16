/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

export enum RunAction {
  EVENTS = "EVENTS",
  EVENTS_ALL = "EVENTS_ALL",
  TESTS = "TESTS",
  UPDATE = "UPDATE",
  VALIDATE = "VALIDATE",
}

export interface GraphFilter {
  table_id?: string | null;
  edge_id?: string | null;
  n?: number | null;
  filter?: string | null;
  min_x?: number | null;
  max_x?: number | null;
  min_y?: number | null;
  max_y?: number | null;
}

//==============================================================
// END Enums and Input Objects
//==============================================================
