/**
 * Performance utilities for React Native optimization
 * Used for debouncing, throttling, and performance monitoring
 */

/**
 * Debounce a function call
 * Delays execution until after wait time has elapsed since last call
 *
 * @param func - Function to debounce
 * @param wait - Milliseconds to wait
 * @returns Debounced function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null;
      func(...args);
    };

    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle a function call
 * Ensures function is called at most once per limit interval
 *
 * @param func - Function to throttle
 * @param limit - Milliseconds between allowed calls
 * @returns Throttled function
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * FPS counter for performance monitoring
 * Tracks frames per second in real-time
 */
export class FPSCounter {
  private frameCount = 0;
  private lastTime = performance.now();
  private fps = 60;

  tick() {
    this.frameCount++;
    const now = performance.now();

    if (now - this.lastTime >= 1000) {
      this.fps = this.frameCount;
      this.frameCount = 0;
      this.lastTime = now;
    }

    return this.fps;
  }

  getFPS() {
    return this.fps;
  }
}
