import { lazy } from 'react';

/**
 * Kid Mode Components
 *
 * Simplified, child-friendly UI components optimized for young learners.
 * These components are lazy-loaded to reduce initial bundle size.
 */

// Eager exports for type safety
export type {
  SimplifiedButtonProps,
  SimplifiedCardProps,
  SimplifiedInputProps,
} from './SimplifiedUI';

export type {
  AnimatedTooltipProps,
  TooltipType,
} from './AnimatedTooltip';

export type {
  IncreaseAnimationProps,
  DecreaseAnimationProps,
  MagicRingAnimationProps,
} from './animations/StitchAnimations';

/**
 * Lazy-loaded components
 * These are loaded on-demand when Kid Mode is enabled to reduce bundle size
 */

// Lazy load SimplifiedUI components
export const SimplifiedButton = lazy(() =>
  import('./SimplifiedUI').then(module => ({
    default: module.SimplifiedButton,
  }))
);

export const SimplifiedCard = lazy(() =>
  import('./SimplifiedUI').then(module => ({
    default: module.SimplifiedCard,
  }))
);

export const SimplifiedInput = lazy(() =>
  import('./SimplifiedUI').then(module => ({
    default: module.SimplifiedInput,
  }))
);

// Lazy load AnimatedTooltip
export const AnimatedTooltip = lazy(() =>
  import('./AnimatedTooltip').then(module => ({
    default: module.AnimatedTooltip,
  }))
);

// Lazy load Stitch Animations
export const IncreaseAnimation = lazy(() =>
  import('./animations/StitchAnimations').then(module => ({
    default: module.IncreaseAnimation,
  }))
);

export const DecreaseAnimation = lazy(() =>
  import('./animations/StitchAnimations').then(module => ({
    default: module.DecreaseAnimation,
  }))
);

export const MagicRingAnimation = lazy(() =>
  import('./animations/StitchAnimations').then(module => ({
    default: module.MagicRingAnimation,
  }))
);

/**
 * Eager loading helper (for when you need non-lazy components)
 * Use this sparingly - prefer lazy loading for Kid Mode components
 */
export async function preloadKidModeComponents(): Promise<void> {
  await Promise.all([
    import('./SimplifiedUI'),
    import('./AnimatedTooltip'),
    import('./animations/StitchAnimations'),
  ]);
}
