/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnectors
// ====================================================

export interface GetConnectors_connectors {
  __typename: "Connector";
  id: any;
  priority: number | null;
  name: string;
  metadata: any;
  icon: string | null;
  category: string | null;
  status: string;
}

export interface GetConnectors {
  connectors: GetConnectors_connectors[];
}
