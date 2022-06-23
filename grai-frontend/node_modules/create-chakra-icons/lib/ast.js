/**
 * @module ast
 * @requires module:utils
 */
const t = require("@babel/types");
const toBabelAST = require("@svgr/hast-util-to-babel-ast").default;
const {
  pairToObject,
  pairsToObject,
  objectToPairs,
  compose,
} = require("./utils");
/**
 * @memberof ast
 * @name pairToObjectProperty
 * @param {[String, String]}
 * @returns {Object}
 * @example
 * const pair = ["hey", "jude"]
 *
 * pairToObjectProperty(value)
 * // output:
 * // {
 * //   type: 'ObjectProperty',
 * //   key: { type: 'Identifier', name: 'hey' },
 * //   value: { type: 'StringLiteral', value: 'jude' },
 * //   computed: false,
 * //   shorthand: false,
 * //   decorators: null
 * // }
 *
 *
 */
const pairToObjectProperty = ([key, value]) =>
  t.objectProperty(
    t.identifier(key),
    // TODO check when value is not string
    t.stringLiteral(value)
  );
/**
 * @memberof ast
 * @name objectPropertyToPair
 * @param {Object}
 * @returns {[String, String]}
 * @example
 * const objectProperty = {
 *   type: 'ObjectProperty',
 *   key: { type: 'Identifier', name: 'hey' },
 *   value: { type: 'StringLiteral', value: 'jude' },
 *   computed: false,
 *   shorthand: false,
 *   decorators: null
 * }
 *
 * objectPropertyToPair(objectProperty)
 * // output: ["hey", "jude"]
 */
const objectPropertyToPair = ({ key: { name: key }, value: { value } }) => [
  key,
  value,
];
/**
 * @todo
 *
 * const objectPropertyToObject = compose(pairToObject, objectPropertyToPair);
 */
/**
 * @memberof ast
 * @name objectToObjectExpression
 * @param {Object}
 * @returns {Object}
 * @example
 * let object = { hey: "jude" }
 * // output:
 * objectToObjectExpression(object)
 * // {
 * //   type: 'ObjectExpression',
 * //   properties: [
 * //     {
 * //       type: 'ObjectProperty',
 * //       key: [Object],
 * //       value: [Object],
 * //       computed: false,
 * //       shorthand: false,
 * //       decorators: null
 * //     }
 * //   ]
 * // }
 */
const objectToObjectExpression = (object) =>
  t.objectExpression(
    objectToPairs(object).reduce(
      (acc, cur) => [...acc, pairToObjectProperty(cur)],
      []
    )
  );
/**
 * @memberof ast
 * @name objectExpressionToObject
 * @param {Object}
 * @returns {Object}
 * @example
 * let objectExpression = {
 *   type: 'ObjectExpression',
 *   properties: [
 *     {
 *       type: 'ObjectProperty',
 *       key: [Object],
 *       value: [Object],
 *       computed: false,
 *       shorthand: false,
 *       decorators: null
 *     }
 *   ]
 * }
 * objectExpressionToObject(objectExpression)
 * // output:
 * // let object = { hey: "jude" }
 */
const objectExpressionToObject = ({ properties }) =>
  pairsToObject(properties.map(objectPropertyToPair));
/**
 * @memberof ast
 * @name toImportDeclaration
 * @param {String} from
 * @param {String[]} imports
 * @returns {Object}
 * @see {https://babeljs.io/docs/en/babel-types#importdeclaration}
 */
const toImportDeclaration = (from, ...imports) =>
  t.importDeclaration(
    [...imports].map((name) =>
      // @see {https://babeljs.io/docs/en/babel-types#importspecifier}
      t.importSpecifier(t.identifier(name), t.identifier(name))
    ),
    t.stringLiteral(from)
  );
/**
 * @memberof ast
 * @name toExportNamedDeclaration
 * @param {Object}
 * @property {String} displayName
 * @property {Object} objectExpression
 * @returns {Object}
 * @example
 * let object = {
 *  displayName: "MyModule",
 *  objectExpression: {...} // you can make with function objectToObjectExpression
 * }
 * toExportNamedDeclaration(object)
 */
const toExportNamedDeclaration = ({ displayName, objectExpression }) => {
  // @see {https://babeljs.io/docs/en/babel-types#callexpression}
  const createIcon = t.callExpression(
    t.identifier("createIcon"),
    objectExpression
  );
  // @see {https://babeljs.io/docs/en/babel-types#variabledeclarator}
  const variableDeclarator = t.variableDeclarator(
    t.identifier(displayName),
    createIcon
  );
  // @see {https://babeljs.io/docs/en/babel-types#variabledeclaration}
  const variableDeclaration = t.variableDeclaration("const", [
    variableDeclarator,
  ]);
  // @see {https://babeljs.io/docs/en/babel-types#exportnameddeclaration}
  const exportNamedDeclaration = t.exportNamedDeclaration(variableDeclaration);
  return exportNamedDeclaration;
};
/**
 * @memberof ast
 * @name toSource
 * @param {Array}
 * @returns {Object}
 */
const toSource = (...statements) => t.program([...statements]);
/**
 * @memberof ast
 * @name hastToProperties
 * @param {Object}
 * @returns {Object}
 */
const hastToProperties = ({
  children: [
    {
      properties: { viewBox },
      children: [
        {
          properties: { d },
        },
      ],
    },
  ],
}) => ({
  viewBox,
  d,
});

/**
 * @memberof ast
 * @name hastChildrenLength
 * @param {Object}
 * @returns {Number}
 */
const hastChildrenLength = ({ children: [{ children }] }) => children.length;
/**
 * @memberof ast
 * @name hastToJSXProperties
 * @param {Object}
 * @returns {Object}
 */
const hastToJSXProperties = ({
  children: [
    {
      children,
      properties: { viewBox },
    },
  ],
}) => ({
  viewBox,
  children,
});
/**
 * @memberof ast
 * @name jsxPropertiesToComponent
 * @param {Object} hast
 * @param {Object} options
 * @param {Boolean} options.isTypescript
 * @param {String} options.displayName
 * @returns {Object}
 */
const hastToComponent = (hast, { displayName, isTypescript }) => {
  const svgTagToIcon = ({ properties: { viewBox }, ...others }) => ({
    ...others,
    properties: { viewBox },
    tagName: "Icon",
  });
  const addOpeningAttributes = ({ expression }, attribute) => ({
    ...expression,
    openingElement: {
      ...expression.openingElement,
      attributes: [...expression.openingElement.attributes, attribute],
    },
  });
  const {
    body: [expressionStatement],
  } = toBabelAST({
    ...hast,
    children: hast.children.map(svgTagToIcon),
  });

  const propsIdentifier = t.identifier("props");

  if (isTypescript) {
    propsIdentifier.typeAnnotation = t.tsTypeAnnotation(
      t.tsTypeReference(t.identifier("IconProps"))
    );
  }

  const iconElement = addOpeningAttributes(
    expressionStatement,
    t.jsxSpreadAttribute(propsIdentifier)
  );

  const arrowFunctionIcon = t.arrowFunctionExpression(
    [propsIdentifier],
    iconElement
  );
  // @see {https://babeljs.io/docs/en/babel-types#variabledeclarator}
  const variableIdentifier = t.identifier(displayName);

  const variableDeclarator = t.variableDeclarator(
    variableIdentifier,
    arrowFunctionIcon
  );
  // @see {https://babeljs.io/docs/en/babel-types#variabledeclaration}
  const variableDeclaration = t.variableDeclaration("const", [
    variableDeclarator,
  ]);
  // @see {https://babeljs.io/docs/en/babel-types#exportnameddeclaration}
  const exportNamedDeclaration = t.exportNamedDeclaration(variableDeclaration);
  return exportNamedDeclaration;
};

module.exports = {
  pairToObjectProperty,
  objectPropertyToPair,
  // objectPropertyToObject,
  objectToObjectExpression,
  objectExpressionToObject,
  toImportDeclaration,
  toExportNamedDeclaration,
  toSource,
  hastToProperties,
  hastToJSXProperties,
  hastChildrenLength,
  hastToComponent,
};
