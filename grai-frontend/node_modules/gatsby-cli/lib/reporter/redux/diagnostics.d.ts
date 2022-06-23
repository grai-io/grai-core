import { ActionsUnion } from "./types";
import type { GatsbyCLIStore } from "./";
declare type DiagnosticsMiddleware = (action: ActionsUnion) => void;
export declare type AdditionalDiagnosticsOutputHandler = () => string;
export declare function registerAdditionalDiagnosticOutputHandler(handler: AdditionalDiagnosticsOutputHandler): void;
export declare function createStructuredLoggingDiagnosticsMiddleware(getStore: () => GatsbyCLIStore): DiagnosticsMiddleware;
export {};
