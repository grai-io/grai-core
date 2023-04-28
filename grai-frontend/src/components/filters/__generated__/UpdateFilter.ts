/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateFilter
// ====================================================

export interface UpdateFilter_updateFilter {
  __typename: "Filter";
  id: any;
  name: string | null;
  metadata: any;
  created_at: any;
}

export interface UpdateFilter {
  updateFilter: UpdateFilter_updateFilter;
}

export interface UpdateFilterVariables {
  id: string;
  name: string;
  metadata: any;
}
