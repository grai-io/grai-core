/// <reference types="node" />
import type { IStructuredError } from "gatsby-cli/src/structured-errors/types";
import { IGatsbyPage } from "../redux/types";
export interface IPageData {
    componentChunkName: IGatsbyPage["componentChunkName"];
    matchPath?: IGatsbyPage["matchPath"];
    path: IGatsbyPage["path"];
    staticQueryHashes: Array<string>;
    getServerDataError?: IStructuredError | Array<IStructuredError> | null;
    manifestId?: string;
}
export declare function constructPageDataString({ componentChunkName, matchPath, path: pagePath, staticQueryHashes, manifestId, }: IPageData, result: string | Buffer): string;
export declare function reverseFixedPagePath(pageDataRequestPath: string): string;
export declare function getPagePathFromPageDataPath(pageDataPath: string): string | null;
