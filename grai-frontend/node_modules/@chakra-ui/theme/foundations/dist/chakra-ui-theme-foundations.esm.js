import { _ as _extends, s as sizes } from '../../dist/sizes-6d76cdc8.esm.js';
import borders from '../borders/dist/chakra-ui-theme-foundations-borders.esm.js';
import breakpoints from '../breakpoints/dist/chakra-ui-theme-foundations-breakpoints.esm.js';
import colors from '../colors/dist/chakra-ui-theme-foundations-colors.esm.js';
import radii from '../radius/dist/chakra-ui-theme-foundations-radius.esm.js';
import shadows from '../shadows/dist/chakra-ui-theme-foundations-shadows.esm.js';
import { spacing } from '../spacing/dist/chakra-ui-theme-foundations-spacing.esm.js';
import transition from '../transition/dist/chakra-ui-theme-foundations-transition.esm.js';
import typography from '../typography/dist/chakra-ui-theme-foundations-typography.esm.js';
import zIndices from '../z-index/dist/chakra-ui-theme-foundations-z-index.esm.js';
import blur from '../blur/dist/chakra-ui-theme-foundations-blur.esm.js';
import '@chakra-ui/theme-tools';

var foundations = _extends({
  breakpoints: breakpoints,
  zIndices: zIndices,
  radii: radii,
  blur: blur,
  colors: colors
}, typography, {
  sizes: sizes,
  shadows: shadows,
  space: spacing,
  borders: borders,
  transition: transition
});

export { foundations as default };
