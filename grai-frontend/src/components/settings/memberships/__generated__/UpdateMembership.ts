/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateMembership
// ====================================================

export interface UpdateMembership_updateMembership {
  __typename: "Membership";
  id: any;
  role: string;
  is_active: boolean;
}

export interface UpdateMembership {
  updateMembership: UpdateMembership_updateMembership;
}

export interface UpdateMembershipVariables {
  id: string;
  role: string;
  is_active: boolean;
}
