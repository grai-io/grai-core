/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateSource
// ====================================================

export interface UpdateSource_updateSource {
  __typename: "Source";
  id: any;
  name: string;
  priority: number;
}

export interface UpdateSource {
  updateSource: UpdateSource_updateSource;
}

export interface UpdateSourceVariables {
  sourceId: string;
  name: string;
  priority: number;
}
