/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnectors
// ====================================================

export interface GetConnectors_connectors {
  __typename: "ConnectorType";
  id: any;
  name: string;
  metadata: any;
}

export interface GetConnectors {
  connectors: GetConnectors_connectors[];
}
