'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

var foundations_sizes_dist_chakraUiThemeFoundationsSizes = require('../../dist/sizes-db4377aa.cjs.prod.js');
var foundations_borders_dist_chakraUiThemeFoundationsBorders = require('../borders/dist/chakra-ui-theme-foundations-borders.cjs.prod.js');
var foundations_breakpoints_dist_chakraUiThemeFoundationsBreakpoints = require('../breakpoints/dist/chakra-ui-theme-foundations-breakpoints.cjs.prod.js');
var foundations_colors_dist_chakraUiThemeFoundationsColors = require('../colors/dist/chakra-ui-theme-foundations-colors.cjs.prod.js');
var foundations_radius_dist_chakraUiThemeFoundationsRadius = require('../radius/dist/chakra-ui-theme-foundations-radius.cjs.prod.js');
var foundations_shadows_dist_chakraUiThemeFoundationsShadows = require('../shadows/dist/chakra-ui-theme-foundations-shadows.cjs.prod.js');
var foundations_spacing_dist_chakraUiThemeFoundationsSpacing = require('../spacing/dist/chakra-ui-theme-foundations-spacing.cjs.prod.js');
var foundations_transition_dist_chakraUiThemeFoundationsTransition = require('../transition/dist/chakra-ui-theme-foundations-transition.cjs.prod.js');
var foundations_typography_dist_chakraUiThemeFoundationsTypography = require('../typography/dist/chakra-ui-theme-foundations-typography.cjs.prod.js');
var foundations_zIndex_dist_chakraUiThemeFoundationsZIndex = require('../z-index/dist/chakra-ui-theme-foundations-z-index.cjs.prod.js');
var foundations_blur_dist_chakraUiThemeFoundationsBlur = require('../blur/dist/chakra-ui-theme-foundations-blur.cjs.prod.js');
require('@chakra-ui/theme-tools');

var foundations = foundations_sizes_dist_chakraUiThemeFoundationsSizes._extends({
  breakpoints: foundations_breakpoints_dist_chakraUiThemeFoundationsBreakpoints["default"],
  zIndices: foundations_zIndex_dist_chakraUiThemeFoundationsZIndex["default"],
  radii: foundations_radius_dist_chakraUiThemeFoundationsRadius["default"],
  blur: foundations_blur_dist_chakraUiThemeFoundationsBlur["default"],
  colors: foundations_colors_dist_chakraUiThemeFoundationsColors["default"]
}, foundations_typography_dist_chakraUiThemeFoundationsTypography["default"], {
  sizes: foundations_sizes_dist_chakraUiThemeFoundationsSizes.sizes,
  shadows: foundations_shadows_dist_chakraUiThemeFoundationsShadows["default"],
  space: foundations_spacing_dist_chakraUiThemeFoundationsSpacing.spacing,
  borders: foundations_borders_dist_chakraUiThemeFoundationsBorders["default"],
  transition: foundations_transition_dist_chakraUiThemeFoundationsTransition["default"]
});

exports["default"] = foundations;
