import webpack from "webpack";
import reporter from "gatsby-cli/lib/reporter";
import { IGatsbyState } from "../../redux/types";
declare type Reporter = typeof reporter;
export declare function writeQueryContext({ staticQueriesByTemplate, components, }: {
    staticQueriesByTemplate: IGatsbyState["staticQueriesByTemplate"];
    components: IGatsbyState["components"];
}): Promise<void>;
export declare function createPageSSRBundle({ rootDir, components, staticQueriesByTemplate, webpackCompilationHash, reporter, isVerbose, }: {
    rootDir: string;
    components: IGatsbyState["components"];
    staticQueriesByTemplate: IGatsbyState["staticQueriesByTemplate"];
    webpackCompilationHash: IGatsbyState["webpackCompilationHash"];
    reporter: Reporter;
    isVerbose?: boolean;
}): Promise<webpack.Compilation | undefined>;
export {};
