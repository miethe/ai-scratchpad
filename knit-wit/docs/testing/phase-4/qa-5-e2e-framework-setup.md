# QA-5: E2E Test Framework Setup - Phase 4 Sprint 10

**Story**: QA-5 - E2E Test Framework Setup (Detox for React Native)
**Sprint**: Sprint 10 (Weeks 14-15)
**Effort**: 13 story points
**Owner**: QA Lead / Senior QA Engineer
**Status**: Framework Documentation
**Created**: 2025-11-14

---

## Executive Summary

This document provides comprehensive guidance for implementing automated E2E testing for the Knit-Wit MVP using Detox (for React Native mobile app) and Playwright (for web testing). This framework enables continuous integration testing without physical device access, allowing automated validation of critical user flows across platforms.

**Scope:**
- Framework selection rationale (Detox vs alternatives)
- Complete Detox installation and configuration
- Environment setup (simulators, CI/CD integration)
- Test structure and best practices
- Example implementation of critical flows
- CI/CD pipeline integration
- Test execution and reporting

**Success Criteria:**
- Framework fully configured and operational
- At least one complete E2E test suite working
- CI/CD pipeline can execute automated tests
- Clear documentation for QA team to extend tests
- Performance baseline established

---

## Part 1: Framework Selection & Comparison

### Detox vs Playwright vs Other Frameworks

| Framework | Mobile Native | React Native | Web | Simulator Support | CI/CD Ready | Learning Curve | Best For |
|-----------|---------------|--------------|-----|-------------------|-------------|----------------|----------|
| **Detox** | iOS/Android | ✓ Excellent | ✗ | ✓ Excellent | ✓ Excellent | Medium | React Native apps |
| **Playwright** | ✗ | Partial (Electron) | ✓ Excellent | ✓ Good | ✓ Excellent | Low | Web & cross-browser |
| **Appium** | ✓ Good | ✓ Good | ✗ | ✓ Fair | ✓ Fair | High | Multi-platform |
| **Cypress** | ✗ | ✗ | ✓ Excellent | ✓ Excellent | ✓ Excellent | Low | Web only |
| **Expo Testing Library** | ✗ | ✓ Good | ✗ | Partial | Fair | Low | Component/unit |

### Recommendation: Detox

**Primary Choice: Detox for React Native/Expo**

**Rationale:**
1. **Native Integration**: Detox runs tests in real iOS/Android simulators with synchronization to React Native bridge
2. **Flake-Free**: Automatic waiting for network requests, animations, and animations completion (no arbitrary waits)
3. **Developer Experience**: Declarative test syntax, excellent debugging
4. **CI/CD Ready**: Designed for headless CI execution; works perfectly in GitHub Actions
5. **Performance**: Significantly faster than Appium; can run parallel test suites
6. **Community**: Strong React Native community support; active maintenance

**Detox Advantages for Knit-Wit:**
- Specialized for Expo/React Native
- Can test all 5 critical flows reliably
- Synchronizes with JavaScript thread automatically
- Works perfectly in GitHub Actions CI/CD
- Can capture screenshots/videos of failures
- Excellent debugging when tests fail

**Secondary Choice: Playwright for Web (if needed)**
- For web version testing (future)
- Lighter weight than Detox
- Excellent cross-browser support

---

## Part 2: Detox Installation & Configuration

### Prerequisites

- **Node.js**: 16+ (18+ recommended)
- **Xcode**: 14+ (for iOS simulator testing)
- **Android Studio**: 2021.2+ (for Android emulator testing)
- **Expo CLI**: Latest version
- **Detox CLI**: Latest version

### Installation Steps

#### 1. Install Detox CLI Globally

```bash
npm install -g detox-cli
```

#### 2. Install Detox in Project

Navigate to the mobile app directory and install:

```bash
cd apps/mobile
npm install --save-dev detox detox-cli detox-config
npm install --save-dev detox-test-utils
npm install --save-dev jest@29
```

#### 3. Configure Jest

Create `apps/mobile/e2e/config.json`:

```json
{
  "testRunner": "jest",
  "testEnvironment": "node",
  "testRegex": "\\.e2e\\.js$",
  "reporters": ["detox/runners/jest/streamlineReporter"],
  "verbose": true
}
```

#### 4. Add Detox Build Configuration

Update `apps/mobile/app.json` (Expo config):

```json
{
  "expo": {
    "plugins": [
      [
        "detox/plugin",
        {
          "ios": true,
          "android": false
        }
      ]
    ]
  }
}
```

#### 5. Initialize Detox Configuration

Create `apps/mobile/.detoxrc.json`:

```json
{
  "testRunner": "jest",
  "apps": {
    "ios.release": {
      "type": "ios.app",
      "binaryPath": "ios/build/Build/Products/Release-iphonesimulator/KnitWit.app",
      "build": "xcodebuild -workspace ios/KnitWit.xcworkspace -scheme KnitWit -configuration Release -sdk iphonesimulator -derivedDataPath ios/build -quiet"
    },
    "ios.debug": {
      "type": "ios.app",
      "binaryPath": "ios/build/Build/Products/Debug-iphonesimulator/KnitWit.app",
      "build": "xcodebuild -workspace ios/KnitWit.xcworkspace -scheme KnitWit -configuration Debug -sdk iphonesimulator -derivedDataPath ios/build -quiet"
    },
    "android.emu.release": {
      "type": "android.emu",
      "binaryPath": "android/app/build/outputs/apk/release/app-release.apk",
      "build": "cd android && ./gradlew assembleRelease assembleAndroidTest -DtestBuildType=release && cd .."
    },
    "android.emu.debug": {
      "type": "android.emu",
      "binaryPath": "android/app/build/outputs/apk/debug/app-debug.apk",
      "build": "cd android && ./gradlew assembleDebug assembleAndroidTest && cd .."
    }
  },
  "devices": {
    "simulator": {
      "type": "iPhone14",
      "device": {
        "type": "iPhone 14"
      }
    },
    "simulator.se": {
      "type": "iPhoneSE3rd",
      "device": {
        "type": "iPhone SE (3rd generation)"
      }
    },
    "emulator": {
      "type": "android.emu",
      "device": {
        "avdName": "Pixel_5_API_31"
      }
    }
  },
  "testSuites": {
    "default": {
      "app": "ios.release",
      "testRunner": "jest"
    },
    "ios.debug": {
      "app": "ios.debug",
      "testRunner": "jest"
    },
    "android": {
      "app": "android.emu.release",
      "testRunner": "jest"
    }
  }
}
```

#### 6. Update Package.json Scripts

Add to `apps/mobile/package.json`:

```json
{
  "scripts": {
    "test": "jest",
    "test:e2e:build": "detox build-framework-cache && detox build --configuration ios.release",
    "test:e2e:test": "detox test --configuration ios.release --cleanup",
    "test:e2e:build:android": "detox build --configuration android.emu.release",
    "test:e2e:test:android": "detox test --configuration android.emu.release --cleanup",
    "test:e2e:debug": "detox test --configuration ios.debug --record logs --recordLogs all",
    "test:e2e": "npm run test:e2e:build && npm run test:e2e:test"
  }
}
```

---

## Part 3: Environment Setup

### iOS Simulator Setup

#### 1. Install Xcode Command Line Tools

```bash
xcode-select --install
```

#### 2. Accept Xcode License

```bash
sudo xcode-select --reset
sudo xcodebuild -license accept
```

#### 3. Create Simulator Device

```bash
# List available simulator types
xcrun simctl list devicetypes

# Create iPhone 14 simulator
xcrun simctl create "iPhone 14" "com.apple.CoreSimulator.SimDeviceType.iPhone-14" "com.apple.CoreSimulator.SimRuntime.iOS-17-0"

# Create iPhone SE simulator
xcrun simctl create "iPhone SE" "com.apple.CoreSimulator.SimDeviceType.iPhone-SE-3rd-generation" "com.apple.CoreSimulator.SimRuntime.iOS-17-0"
```

#### 4. Boot Simulator

```bash
xcrun simctl boot "iPhone 14"
```

#### 5. List Running Simulators

```bash
xcrun simctl list devices
```

### Android Emulator Setup

#### 1. Create AVD (Android Virtual Device)

Use Android Studio's AVD Manager or command line:

```bash
# List available images
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --list

# Create Pixel 5 API 31 emulator
$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager \
  -s Pixel_5_API_31 \
  -k "system-images;android-31;google_apis;x86_64" \
  -d "Pixel 5" \
  -g "WVGA800cellphone" \
  -n "Pixel_5_API_31"
```

#### 2. Boot Emulator

```bash
$ANDROID_HOME/emulator/emulator -avd Pixel_5_API_31 &
```

#### 3. Verify Device Connection

```bash
adb devices
```

### CI/CD Environment Setup (GitHub Actions)

Create `.github/workflows/e2e-tests.yml`:

```yaml
name: E2E Tests

on:
  push:
    branches: [main, develop]
    paths:
      - 'apps/mobile/**'
      - '.github/workflows/e2e-tests.yml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'apps/mobile/**'

jobs:
  e2e-ios:
    runs-on: macos-latest
    timeout-minutes: 60

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: |
          cd apps/mobile
          npm ci

      - name: Install Detox CLI
        run: npm install -g detox-cli

      - name: Detox build framework cache
        run: detox build-framework-cache

      - name: Build Detox for iOS
        run: |
          cd apps/mobile
          detox build --configuration ios.release

      - name: Run E2E tests
        run: |
          cd apps/mobile
          detox test --configuration ios.release --cleanup --record logs

      - name: Upload test logs
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-logs-ios
          path: apps/mobile/artifacts/

      - name: Upload test recordings
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-recordings-ios
          path: apps/mobile/recordings/

  test-report:
    needs: e2e-ios
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Download all artifacts
        uses: actions/download-artifact@v3

      - name: Publish test report
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: E2E Test Results
          path: 'e2e-logs-ios/**/*.json'
          reporter: 'jest-junit'
```

---

## Part 4: Test Structure & Best Practices

### Directory Structure

```
apps/mobile/
├── e2e/
│   ├── helpers/
│   │   ├── device.helper.js       # Device interaction helpers
│   │   ├── navigation.helper.js    # Navigation helpers
│   │   ├── assertions.helper.js    # Custom assertions
│   │   └── matchers.helper.js      # Custom matchers
│   ├── screens/
│   │   ├── homeScreen.js           # Home screen page object
│   │   ├── generateScreen.js       # Generator screen page object
│   │   ├── visualizeScreen.js      # Visualization screen page object
│   │   ├── exportScreen.js         # Export screen page object
│   │   └── settingsScreen.js       # Settings screen page object
│   ├── flows/
│   │   ├── generateFlow.test.e2e.js
│   │   ├── visualizeFlow.test.e2e.js
│   │   ├── exportFlow.test.e2e.js
│   │   ├── kidModeFlow.test.e2e.js
│   │   └── settingsFlow.test.e2e.js
│   ├── config.json
│   └── testRunnerConfig.js
├── .detoxrc.json
└── package.json
```

### Page Object Pattern

Create reusable screen objects. Example: `apps/mobile/e2e/screens/homeScreen.js`

```javascript
class HomeScreen {
  // Matchers (element identifiers)
  generateButton = element(by.id('home-generate-btn'));
  settingsButton = element(by.id('home-settings-btn'));
  appTitle = element(by.text('Knit Wit'));

  // Actions
  async tapGenerate() {
    await waitFor(this.generateButton)
      .toBeVisible()
      .withTimeout(5000);
    await this.generateButton.tap();
  }

  async tapSettings() {
    await waitFor(this.settingsButton)
      .toBeVisible()
      .withTimeout(5000);
    await this.settingsButton.tap();
  }

  // Assertions
  async verifyVisible() {
    await expect(this.appTitle).toBeVisible();
  }

  async verifyGenreateButtonVisible() {
    await expect(this.generateButton).toBeVisible();
  }
}

module.exports = new HomeScreen();
```

### Test Naming Convention

- File: `{feature}Flow.test.e2e.js`
- Suite: `describe('Flow: Generate Sphere Pattern', () => { ... })`
- Test: `it('should generate sphere with default gauge', async () => { ... })`

### Synchronization Strategy

Detox automatically handles:
- Network request completion
- React Native JavaScript thread synchronization
- Animation completion
- Gesture acknowledgment

Use explicit waits only for edge cases:

```javascript
// Automatic synchronization (preferred)
await element(by.id('submit-btn')).tap();
await expect(element(by.text('Pattern Generated'))).toBeVisible();

// Explicit wait (only if automatic fails)
await waitFor(element(by.id('loading-spinner')))
  .not.toBeVisible()
  .withTimeout(5000);
```

### Error Handling & Screenshots

```javascript
beforeEach(async () => {
  // Start fresh for each test
  await device.reloadReactNative();
});

afterEach(async () => {
  // Capture screenshot on failure
  if (testFailed) {
    await device.takeScreenshot('failure');
  }
});

afterAll(async () => {
  // Cleanup
  await device.sendUserAction(userAction.back);
});
```

---

## Part 5: Example Test Implementation

### Test 1: Generate Sphere Pattern (Complete Flow)

Create `apps/mobile/e2e/flows/generateFlow.test.e2e.js`:

```javascript
const { device, element, by, expect, waitFor } = require('detox');
const homeScreen = require('../screens/homeScreen');
const generateScreen = require('../screens/generateScreen');
const visualizeScreen = require('../screens/visualizeScreen');

describe('Flow: Generate Sphere Pattern', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should generate sphere with default gauge', async () => {
    // Step 1: Open app and verify home screen
    await homeScreen.verifyVisible();
    console.log('✓ Home screen visible');

    // Step 2: Navigate to generator
    await homeScreen.tapGenerate();
    await generateScreen.verifyVisible();
    console.log('✓ Generator screen opened');

    // Step 3: Verify default parameters
    await generateScreen.verifyShapeSelected('Sphere');
    await generateScreen.verifyDiameter('10');
    await generateScreen.verifyGauge('14/16');
    console.log('✓ Default parameters verified');

    // Step 4: Generate pattern
    await generateScreen.tapGenerate();

    // Wait for loading and visualization
    await waitFor(element(by.id('loading-spinner')))
      .not.toBeVisible()
      .withTimeout(10000); // Allow up to 10s for generation + visualization

    console.log('✓ Generation complete');

    // Step 5: Verify visualization loaded
    await visualizeScreen.verifyVisible();
    await visualizeScreen.verifyRoundDisplayed(1);
    await visualizeScreen.verifyStitchCount(6); // First round should have 6 stitches
    console.log('✓ Visualization displayed correctly');

    // Step 6: Navigate rounds
    await visualizeScreen.tapNextRound();
    await visualizeScreen.verifyRoundDisplayed(2);
    console.log('✓ Round navigation works');
  });

  it('should generate cylinder pattern with custom gauge', async () => {
    // Step 1: Navigate to generator
    await homeScreen.tapGenerate();

    // Step 2: Change shape to cylinder
    await generateScreen.selectShape('Cylinder');
    await generateScreen.verifyShapeSelected('Cylinder');

    // Step 3: Set custom gauge
    await generateScreen.setGauge('12/14');

    // Step 4: Generate pattern
    await generateScreen.tapGenerate();

    // Step 5: Verify cylinder generated
    await waitFor(element(by.id('loading-spinner')))
      .not.toBeVisible()
      .withTimeout(10000);

    await visualizeScreen.verifyVisible();
    console.log('✓ Cylinder pattern generated with custom gauge');
  });

  it('should handle invalid gauge gracefully', async () => {
    // Step 1: Navigate to generator
    await homeScreen.tapGenerate();

    // Step 2: Set invalid gauge (too high)
    await generateScreen.setGauge('100/100');

    // Step 3: Try to generate
    await generateScreen.tapGenerate();

    // Step 4: Verify error message
    await expect(
      element(by.text('Invalid gauge parameters'))
    ).toBeVisible();

    console.log('✓ Invalid gauge rejected with error message');
  });
});
```

### Screen Object: generateScreen.js

```javascript
class GenerateScreen {
  shapeSelector = element(by.id('shape-selector'));
  diameterInput = element(by.id('diameter-input'));
  gaugeInput = element(by.id('gauge-input'));
  generateButton = element(by.id('generate-button'));
  backButton = element(by.text('Back'));

  async verifyVisible() {
    await expect(element(by.text('Generate Pattern'))).toBeVisible();
  }

  async selectShape(shapeName) {
    await this.shapeSelector.tap();
    await element(by.text(shapeName)).tap();
  }

  async verifyShapeSelected(expectedShape) {
    await expect(
      element(by.id(`shape-${expectedShape.toLowerCase()}`))
    ).toBeVisible();
  }

  async setDiameter(diameter) {
    await this.diameterInput.clearText();
    await this.diameterInput.typeText(diameter);
  }

  async verifyDiameter(expected) {
    await expect(this.diameterInput).toHaveToggleValue(
      parseInt(expected)
    );
  }

  async setGauge(gauge) {
    await this.gaugeInput.clearText();
    await this.gaugeInput.typeText(gauge);
  }

  async verifyGauge(expected) {
    await expect(this.gaugeInput).toHaveText(expected);
  }

  async tapGenerate() {
    await waitFor(this.generateButton)
      .toBeVisible()
      .withTimeout(5000);
    await this.generateButton.tap();
  }

  async tapBack() {
    await this.backButton.tap();
  }
}

module.exports = new GenerateScreen();
```

### Screen Object: visualizeScreen.js

```javascript
class VisualizeScreen {
  roundDisplay = element(by.id('round-display'));
  stitchCountDisplay = element(by.id('stitch-count'));
  nextButton = element(by.id('next-round-btn'));
  previousButton = element(by.id('previous-round-btn'));
  exportButton = element(by.id('export-btn'));
  roundScrubber = element(by.id('round-scrubber'));

  async verifyVisible() {
    await expect(this.roundDisplay).toBeVisible();
    await expect(this.roundScrubber).toBeVisible();
  }

  async verifyRoundDisplayed(expectedRound) {
    await expect(this.roundDisplay).toHaveText(`Round ${expectedRound}`);
  }

  async verifyStitchCount(expectedCount) {
    await expect(this.stitchCountDisplay).toHaveText(
      expectedCount.toString()
    );
  }

  async tapNextRound() {
    await this.nextButton.tap();
    // Wait for visualization update
    await waitFor(element(by.id('svg-visualization')))
      .toBeVisible()
      .withTimeout(2000);
  }

  async tapPreviousRound() {
    await this.previousButton.tap();
    await waitFor(element(by.id('svg-visualization')))
      .toBeVisible()
      .withTimeout(2000);
  }

  async navigateToRound(roundNumber) {
    // Calculate position on scrubber
    const scrubberBounds = await this.roundScrubber.getAttributes();
    const position = (roundNumber - 1) / 100; // Approximate position
    await this.roundScrubber.multiTap(position);
  }

  async tapExport() {
    await this.exportButton.tap();
  }
}

module.exports = new VisualizeScreen();
```

---

## Part 6: Running Tests Locally

### Prerequisites Check

```bash
# Verify Xcode command line tools
xcode-select -p

# Verify Android SDK
echo $ANDROID_HOME

# Verify Detox CLI
detox --version

# Verify Node/npm
node --version
npm --version
```

### Local Test Execution

#### iOS

```bash
# Build app once
cd apps/mobile
npm run test:e2e:build

# Run tests
npm run test:e2e:test

# Run with debug output
npm run test:e2e:debug

# Run specific test file
detox test e2e/flows/generateFlow.test.e2e.js --configuration ios.release

# Run tests matching pattern
detox test --configuration ios.release --match "should generate sphere"
```

#### Android

```bash
cd apps/mobile
npm run test:e2e:build:android
npm run test:e2e:test:android
```

### Debugging Failed Tests

#### 1. Enable Logging

```javascript
// In test file
beforeAll(async () => {
  await device.launchApp({
    newInstance: true,
    launchArgs: { detoxPrintBusyIdleResources: 'YES' }
  });
});
```

#### 2. Inspect Element at Failure

```bash
# When test fails, Detox captures screenshots and logs
# Check artifacts/ directory for:
# - failure_[timestamp].png  (screenshot)
# - detox.log (detailed logs)
```

#### 3. Increase Timeouts for Debugging

```javascript
// Temporarily increase timeouts for slow network/device
await waitFor(element(by.id('submit-btn')))
  .toBeVisible()
  .withTimeout(30000); // 30 seconds
```

#### 4. Capture Element Hierarchy

```bash
# Print element tree during test
detox test --configuration ios.release \
  --record logs \
  --recordLogs all \
  -vv # Very verbose output
```

---

## Part 7: CI/CD Integration

### GitHub Actions Workflow

See `github/workflows/e2e-tests.yml` (from Part 3) for complete workflow.

**Key Features:**
- Runs on push to main/develop and on PRs
- Builds iOS and Android variants in parallel
- Uploads test artifacts (screenshots, logs) on failure
- Publishes test report to workflow summary
- Automatically runs only if mobile code changed

### Running Tests in CI

Tests run automatically on:
1. **Push to main**: Full test suite required to pass
2. **Push to develop**: Full test suite required to pass
3. **Pull Request**: Tests run on PR; must pass for merge
4. **Manual Trigger**: Can run from Actions tab

### Expected CI Output

```
✓ Flow: Generate Sphere Pattern
  ✓ should generate sphere with default gauge (2.3s)
  ✓ should generate cylinder with custom gauge (2.1s)
  ✓ should handle invalid gauge gracefully (1.8s)

✓ Flow: Visualize Pattern
  ✓ should navigate rounds smoothly (1.5s)
  ✓ should update stitch count correctly (1.2s)

✓ Flow: Export Pattern
  ✓ should export PDF successfully (3.2s)
  ✓ should export JSON format (1.1s)

Test Suites: 5 passed, 5 total
Tests: 15 passed, 15 total
Time: 24.8s
```

---

## Part 8: Extending the Framework

### Adding a New Test

1. **Create screen object** (if new screen):
   ```javascript
   // e2e/screens/newScreen.js
   class NewScreen { ... }
   module.exports = new NewScreen();
   ```

2. **Create test file**:
   ```javascript
   // e2e/flows/newFlow.test.e2e.js
   const newScreen = require('../screens/newScreen');
   describe('Flow: New Feature', () => {
     it('should do something', async () => { ... });
   });
   ```

3. **Run test**:
   ```bash
   npm run test:e2e:test
   ```

### Custom Matchers

Create `e2e/helpers/matchers.helper.js`:

```javascript
expect.extend({
  toBeWithinBounds(received, min, max) {
    const pass = received >= min && received <= max;
    return {
      pass,
      message: () =>
        `expected ${received} to be within ${min}-${max}`
    };
  }
});
```

### Accessibility Testing with Detox

```javascript
// Enable accessibility testing
await device.launchApp({
  newInstance: true,
  launchArgs: {
    detoxEnableAccessibilityInfo: 'YES'
  }
});

// Test VoiceOver labels (iOS)
await expect(element(by.text('Generate'))).toHaveAccessibilityLabel(
  'Generate a new pattern'
);
```

---

## Part 9: Performance Benchmarking

### Measuring Test Execution Time

```javascript
describe('Performance: Generation', () => {
  it('should generate sphere in < 200ms', async () => {
    const startTime = Date.now();

    await homeScreen.tapGenerate();
    await generateScreen.tapGenerate();

    await waitFor(element(by.id('loading-spinner')))
      .not.toBeVisible()
      .withTimeout(10000);

    const executionTime = Date.now() - startTime;

    expect(executionTime).toBeLessThan(200);
    console.log(`✓ Generation completed in ${executionTime}ms`);
  });
});
```

### Baseline Metrics (from Sprint 8 QA tests)

| Operation | Target | Acceptable |
|-----------|--------|-----------|
| App launch | < 2s | < 3s |
| Pattern generation | < 200ms | < 300ms |
| Round navigation | < 50ms | < 100ms |
| PDF export | < 3s | < 5s |
| Settings persistence | < 100ms | < 200ms |

---

## Part 10: Troubleshooting

### Common Issues & Solutions

#### Issue: Simulator won't boot
```bash
# Solution: Reset simulator
xcrun simctl erase all
xcrun simctl create "iPhone 14" "com.apple.CoreSimulator.SimDeviceType.iPhone-14" "com.apple.CoreSimulator.SimRuntime.iOS-17-0"
xcrun simctl boot "iPhone 14"
```

#### Issue: "Element not found" errors
```javascript
// Solution: Increase visibility timeout
await waitFor(element(by.id('element-id')))
  .toBeVisible()
  .withTimeout(10000); // 10 seconds instead of 5
```

#### Issue: Tests pass locally but fail in CI
```bash
# Solution: Build for CI environment
detox build --configuration ios.release --buildType Release

# Use release build in CI (faster, fewer edge cases)
detox test --configuration ios.release --cleanup
```

#### Issue: "waitFor timeout" on animations
```javascript
// Solution: Detox auto-synchronizes, but use explicit wait for custom animations
await waitFor(element(by.id('animation-complete')))
  .toBeVisible()
  .withTimeout(5000);
```

#### Issue: Screenshots not captured on failure
```bash
# Solution: Enable artifact capture in config
detox test --configuration ios.release \
  --record logs \
  --recordLogs all
```

---

## Part 11: Best Practices Summary

### Do's ✓
- Use page objects for screen abstraction
- Wait for elements explicitly (don't assume timing)
- Test critical user flows end-to-end
- Run tests in CI for every PR
- Capture screenshots/videos of failures
- Keep tests focused (one flow per describe block)
- Use meaningful element IDs in React components

### Don'ts ✗
- Don't use arbitrary `sleep()` calls
- Don't test implementation details (test user behavior)
- Don't make tests interdependent (each should be self-contained)
- Don't commit tests with hardcoded timeouts > 10 seconds
- Don't test 3rd party libraries (assume they work)
- Don't mix multiple flows in one test

### Maintenance
- Review and update tests with each feature change
- Keep page objects synchronized with UI changes
- Monitor test execution time (should stay < 30s per suite)
- Archive failed test artifacts for debugging
- Update CI/CD scripts when adding new test suites

---

## Related Documentation

- [Detox Official Docs](https://wix.github.io/Detox/)
- [Expo Testing Guide](https://docs.expo.dev/build-reference/how-tos/)
- [Knit-Wit CLAUDE.md](../../../CLAUDE.md)
- [Phase 4 Sprint 8 Test Plans](./sprint-8-qa1-ios-test-plan.md)
- [Testing Strategy](../../../project_plans/mvp/supporting-docs/testing-strategy.md)

---

**Framework Version**: Detox 20.x+, Jest 29+
**Last Updated**: 2025-11-14
**Next Review**: Sprint 11 (performance optimization)
