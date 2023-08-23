/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

//==============================================================
// START Enums and Input Objects
//==============================================================

export enum Ordering {
  ASC = "ASC",
  DESC = "DESC",
}

export enum RunAction {
  EVENTS = "EVENTS",
  EVENTS_ALL = "EVENTS_ALL",
  TESTS = "TESTS",
  UPDATE = "UPDATE",
  VALIDATE = "VALIDATE",
}

export interface GraphFilter {
  source_id?: string | null;
  table_id?: string | null;
  edge_id?: string | null;
  n?: number | null;
  filters?: string[] | null;
  inline_filters?: any[] | null;
  min_x?: number | null;
  max_x?: number | null;
  min_y?: number | null;
  max_y?: number | null;
}

export interface NodeOrder {
  id?: Ordering | null;
  namespace?: Ordering | null;
  name?: Ordering | null;
  display_name?: Ordering | null;
  metadata__grai__node_type?: Ordering | null;
  is_active?: Ordering | null;
  created_at?: Ordering | null;
  updated_at?: Ordering | null;
}

export interface StringFilter {
  equals?: string | null;
  contains?: string[] | null;
}

export interface WorkspaceEdgeFilter {
  edge_type?: StringFilter | null;
}

export interface WorkspaceNodeFilter {
  node_type?: StringFilter | null;
}

//==============================================================
// END Enums and Input Objects
//==============================================================
