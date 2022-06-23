/// <reference types="node" />
import { reverseFixedPagePath, IPageData } from "./page-data-helpers";
import { Span } from "opentracing";
export { reverseFixedPagePath };
import { IExecutionResult } from "../query/types";
export interface IPageDataWithQueryResult extends IPageData {
    result: IExecutionResult;
}
export declare function readPageData(publicDir: string, pagePath: string): Promise<IPageDataWithQueryResult>;
export declare function removePageData(publicDir: string, pagePath: string): Promise<void>;
export declare function pageDataExists(publicDir: string, pagePath: string): boolean;
export declare function waitUntilPageQueryResultsAreStored(): Promise<void>;
export declare function savePageQueryResult(programDir: string, pagePath: string, stringifiedResult: string): Promise<void>;
export declare function readPageQueryResult(publicDir: string, pagePath: string): Promise<string | Buffer>;
export declare function writePageData(publicDir: string, pageData: IPageData): Promise<string>;
export declare function isFlushEnqueued(): boolean;
export declare function flush(parentSpan?: Span): Promise<void>;
export declare function enqueueFlush(parentSpan?: Span): void;
export declare function handleStalePageData(parentSpan: Span): Promise<void>;
