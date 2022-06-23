import { GraphQLSchema } from "graphql";
import { ESLint } from "eslint";
export declare const eslintRequiredConfig: ESLint.Options;
export declare const eslintConfig: (schema: GraphQLSchema, usingAutomaticJsxRuntime: boolean) => ESLint.Options;
