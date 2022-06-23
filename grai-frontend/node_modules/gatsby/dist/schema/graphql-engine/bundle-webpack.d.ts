import webpack from "webpack";
import reporter from "gatsby-cli/lib/reporter";
declare type Reporter = typeof reporter;
export declare function createGraphqlEngineBundle(rootDir: string, reporter: Reporter, isVerbose?: boolean): Promise<webpack.Compilation | undefined>;
export {};
