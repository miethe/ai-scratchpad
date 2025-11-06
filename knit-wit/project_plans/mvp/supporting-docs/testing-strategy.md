# Testing Strategy

**Project:** Knit-Wit MVP
**Document Version:** 1.0
**Last Updated:** 2025-11-05
**Owner:** QA/Testing Lead

> **Note:** This document provides comprehensive testing strategy details. See [Implementation Plan](../implementation-plan.md) for overall project structure and development workflow.

---

## Table of Contents

1. [Overview](#overview)
2. [Testing Pyramid](#testing-pyramid)
3. [Unit Testing Strategy](#unit-testing-strategy)
4. [Integration Testing Strategy](#integration-testing-strategy)
5. [End-to-End Testing Strategy](#end-to-end-testing-strategy)
6. [Accessibility Testing](#accessibility-testing)
7. [Performance Testing](#performance-testing)
8. [Visual Regression Testing](#visual-regression-testing)
9. [Test Data & Fixtures](#test-data--fixtures)
10. [CI/CD Integration](#cicd-integration)
11. [Testing Schedule](#testing-schedule)
12. [Tools & Technologies](#tools--technologies)

---

## Overview

### Testing Philosophy

Knit-Wit follows a **test-driven quality approach** with emphasis on:

- **Early Testing:** Unit tests written during development (TDD where appropriate)
- **Automated First:** Prefer automated tests over manual for repeatability
- **Risk-Based:** Focus testing effort on critical paths (pattern generation, visualization)
- **Accessibility Built-In:** Accessibility testing integrated from day one
- **Performance as Quality:** Performance benchmarks enforced in CI

### Quality Goals

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Unit Test Coverage** | 80%+ (backend), 60%+ (frontend) | Coverage reports in CI |
| **Pattern Generation Time** | < 200ms per pattern | Benchmark tests |
| **API Response Time** | < 500ms under load | Load testing |
| **Frame Rendering** | < 50ms per frame | React DevTools Profiler |
| **Accessibility** | WCAG AA compliance | Automated + manual audits |
| **Bug Escape Rate** | < 5% (Phase 4+) | Bugs found post-deployment / total |

### Testing Scope

**In Scope for MVP:**
- Pattern generation algorithms (sphere, cylinder, cone)
- API endpoints (generate, visualize, export)
- Mobile app UI components (React Native)
- Visualization rendering (SVG frames)
- Accessibility (WCAG AA critical items)
- Performance (generation < 200ms)
- Cross-platform (iOS 14+, Android 10+)

**Out of Scope for MVP:**
- User authentication flows (auth stubs only)
- Multi-user collaboration
- Payment processing
- Social sharing features
- Advanced pattern types (cables, lace)

---

## Testing Pyramid

```
        /\
       /  \        E2E Tests (Detox)
      /----\       10% of tests, 4 weeks before launch
     /      \      Focus: Critical user flows
    /________\
   /          \    Integration Tests (pytest, Jest)
  /            \   20% of tests, throughout development
 /              \  Focus: API contracts, full pipeline
/________________\
                   Unit Tests (pytest, Jest)
                   70% of tests, during development
                   Focus: Business logic, algorithms
```

### Rationale

**70% Unit Tests:**
- Fast execution (< 5 minutes)
- Isolate bugs to specific functions
- Pattern algorithm correctness is critical
- Easy to write during development

**20% Integration Tests:**
- Verify component interactions
- API contract validation
- Database integration
- Full pipeline (generate → visualize → export)

**10% E2E Tests:**
- Slow, brittle, expensive to maintain
- Focus on critical paths only
- Run before releases and nightly
- Catch UI/UX regressions

---

## Unit Testing Strategy

### Backend (Python — pytest)

**Framework:** pytest 7+
**Coverage Tool:** pytest-cov
**Mocking:** pytest-mock, unittest.mock

#### Coverage Targets

- **Pattern Engine:** 80%+ line coverage
- **API Routes:** 75%+ coverage
- **Services/Utilities:** 80%+ coverage

#### Testing Approach

**1. Algorithm Testing (Critical)**

Test pattern generation algorithms with multiple gauges, sizes, and edge cases.

```python
# packages/pattern-engine/tests/unit/test_sphere.py
import pytest
from pattern_engine.compilers.sphere import SphereCompiler
from pattern_engine.models import GenerateRequest, Gauge

def test_sphere_10cm_sc_spiral_gauge_14_16():
    """Test sphere generation with standard single crochet gauge."""
    compiler = SphereCompiler()
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=Gauge(sts_per_10cm=14, rows_per_10cm=16),
        stitch='sc',
        round_mode='spiral',
        terms='US'
    )

    dsl = compiler.generate(request)

    # Verify equator stitches match gauge calculation
    expected_equator = compute_expected_equator(10, 14)
    actual_equator = find_max_stitches(dsl.rounds)
    assert actual_equator == pytest.approx(expected_equator, rel=0.05)

    # Verify increases are evenly distributed
    increase_positions = extract_increase_positions(dsl)
    assert are_evenly_spaced(increase_positions, tolerance=1)

    # Verify symmetry: increases mirror decreases
    inc_rounds = count_increase_rounds(dsl)
    dec_rounds = count_decrease_rounds(dsl)
    assert inc_rounds == dec_rounds


def test_sphere_edge_cases():
    """Test edge cases: tiny diameter, large diameter, unusual gauges."""
    compiler = SphereCompiler()

    # Very small sphere (3cm)
    small_request = GenerateRequest(shape='sphere', diameter=3, ...)
    small_dsl = compiler.generate(small_request)
    assert len(small_dsl.rounds) >= 6  # Minimum viable sphere

    # Large sphere (30cm)
    large_request = GenerateRequest(shape='sphere', diameter=30, ...)
    large_dsl = compiler.generate(large_request)
    assert len(large_dsl.rounds) <= 100  # Reasonable upper limit

    # Unusual gauge (very loose)
    loose_request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge=Gauge(sts_per_10cm=8, rows_per_10cm=10)
    )
    loose_dsl = compiler.generate(loose_request)
    assert loose_dsl is not None
```

**2. Distribution Algorithm Testing**

```python
# packages/pattern-engine/tests/unit/test_distribution.py
def test_even_distribution_6_changes_36_stitches():
    """Test even spacing of increases/decreases."""
    from pattern_engine.algorithms import even_distribution

    indices = even_distribution(36, 6)

    # Verify positions
    assert indices == [6, 12, 18, 24, 30, 36]

    # Verify spacing
    assert all(indices[i+1] - indices[i] == 6 for i in range(len(indices)-1))


def test_even_distribution_edge_cases():
    """Test edge cases: 1 change, more changes than stitches, prime numbers."""
    # Single change
    assert even_distribution(10, 1) == [10]

    # More changes than stitches (impossible, should raise)
    with pytest.raises(ValueError):
        even_distribution(5, 10)

    # Prime number of stitches
    result = even_distribution(37, 7)
    assert len(result) == 7
    assert max_spacing_difference(result) <= 1  # As even as possible
```

**3. Mocking External Dependencies**

```python
# apps/api/tests/unit/test_pattern_service.py
from unittest.mock import Mock, patch
from services.pattern_service import PatternService

def test_generate_pattern_success(mocker):
    """Test pattern service calls compiler and saves to DB."""
    # Mock dependencies
    mock_compiler = mocker.patch('services.pattern_service.PatternCompiler')
    mock_db = mocker.patch('services.pattern_service.db_session')

    mock_compiler.return_value.compile.return_value = mock_dsl()

    # Execute
    service = PatternService()
    result = service.generate_pattern(sphere_request, user_id='user123')

    # Verify
    assert result.pattern_id is not None
    mock_db.add.assert_called_once()
    mock_compiler.return_value.compile.assert_called_once()
```

#### Running Unit Tests

```bash
# Run all unit tests
cd packages/pattern-engine
pytest tests/unit/

# Run with coverage
pytest --cov=pattern_engine --cov-report=html tests/unit/

# Run specific test file
pytest tests/unit/test_sphere.py

# Run specific test
pytest tests/unit/test_sphere.py::test_sphere_10cm_sc_spiral_gauge_14_16

# Run with verbose output
pytest -v tests/unit/
```

---

### Frontend (JavaScript/TypeScript — Jest)

**Framework:** Jest + React Testing Library
**Coverage Tool:** jest --coverage
**Component Testing:** @testing-library/react-native

#### Coverage Targets

- **UI Components:** 60%+ coverage (integration tests cover rest)
- **Utilities/Helpers:** 80%+ coverage
- **State Management:** 70%+ coverage

#### Testing Approach

**1. Component Testing**

```typescript
// apps/mobile/__tests__/components/RoundScrubber.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { RoundScrubber } from '../../components/RoundScrubber';

describe('RoundScrubber', () => {
  it('should call onRoundChange when Next is pressed', () => {
    const onRoundChange = jest.fn();
    const { getByText } = render(
      <RoundScrubber
        currentRound={5}
        maxRound={20}
        onRoundChange={onRoundChange}
      />
    );

    fireEvent.press(getByText('Next >'));
    expect(onRoundChange).toHaveBeenCalledWith(6);
  });

  it('should disable Next button on last round', () => {
    const { getByText } = render(
      <RoundScrubber currentRound={20} maxRound={20} onRoundChange={jest.fn()} />
    );

    const nextButton = getByText('Next >');
    expect(nextButton.props.accessibilityState.disabled).toBe(true);
  });

  it('should update slider value when scrubbed', () => {
    const onRoundChange = jest.fn();
    const { getByTestId } = render(
      <RoundScrubber currentRound={5} maxRound={20} onRoundChange={onRoundChange} />
    );

    const slider = getByTestId('round-slider');
    fireEvent(slider, 'onValueChange', 12);

    expect(onRoundChange).toHaveBeenCalledWith(12);
  });
});
```

**2. Snapshot Testing**

```typescript
// apps/mobile/__tests__/components/PatternFrame.test.tsx
import { render } from '@testing-library/react-native';
import { PatternFrame } from '../../components/PatternFrame';
import { mockFrameData } from '../fixtures/frames';

describe('PatternFrame', () => {
  it('should match snapshot for sphere frame', () => {
    const { toJSON } = render(
      <PatternFrame frame={mockFrameData.sphere_round_5} />
    );

    expect(toJSON()).toMatchSnapshot();
  });
});
```

**3. Utility Function Testing**

```typescript
// apps/mobile/__tests__/utils/gauge-converter.test.ts
import { convertGauge, inchesToCm, cmToInches } from '../../utils/gauge-converter';

describe('gauge-converter', () => {
  it('should convert inches to cm', () => {
    expect(inchesToCm(4)).toBeCloseTo(10.16, 1);
  });

  it('should convert cm to inches', () => {
    expect(cmToInches(10)).toBeCloseTo(3.94, 1);
  });

  it('should convert gauge from imperial to metric', () => {
    const imperial = { sts_per_4in: 14, rows_per_4in: 16 };
    const metric = convertGauge(imperial, 'metric');

    expect(metric.sts_per_10cm).toBeCloseTo(14 * 2.54 / 10, 1);
    expect(metric.rows_per_10cm).toBeCloseTo(16 * 2.54 / 10, 1);
  });
});
```

#### Running Frontend Tests

```bash
# Run all tests
cd apps/mobile
pnpm test

# Run with coverage
pnpm test --coverage

# Update snapshots
pnpm test --updateSnapshot

# Watch mode (for TDD)
pnpm test --watch

# Run specific test file
pnpm test RoundScrubber
```

---

## Integration Testing Strategy

Integration tests verify that multiple components work together correctly.

### API Integration Tests (pytest + FastAPI TestClient)

```python
# apps/api/tests/integration/test_generate_endpoint.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_post_patterns_generate_sphere():
    """Test POST /api/v1/patterns/generate with sphere request."""
    response = client.post('/api/v1/patterns/generate', json={
        'shape': 'sphere',
        'diameter': 10,
        'gauge': {
            'sts_per_10cm': 14,
            'rows_per_10cm': 16
        },
        'stitch': 'sc',
        'round_mode': 'spiral',
        'terms': 'US'
    })

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert 'pattern_id' in data
    assert 'dsl' in data
    assert 'assets' in data

    # Verify DSL content
    assert len(data['dsl']['rounds']) > 0
    assert data['dsl']['metadata']['shape'] == 'sphere'

    # Verify assets
    assert 'pdf_url' in data['assets']


def test_generate_endpoint_validation_errors():
    """Test validation errors for invalid requests."""
    # Missing required field
    response = client.post('/api/v1/patterns/generate', json={
        'shape': 'sphere',
        # Missing diameter
    })
    assert response.status_code == 422

    # Invalid shape
    response = client.post('/api/v1/patterns/generate', json={
        'shape': 'dodecahedron',  # Not supported
        'diameter': 10,
    })
    assert response.status_code == 400
    assert 'error' in response.json()
```

### Full Pipeline Integration Tests

```python
# packages/pattern-engine/tests/integration/test_full_pipeline.py
def test_generate_visualize_export_pipeline():
    """Test complete flow: generate → visualize → export."""
    # 1. Generate pattern DSL
    compiler = PatternCompiler()
    request = GenerateRequest(shape='sphere', diameter=10, ...)
    dsl = compiler.compile(request)

    assert dsl is not None
    assert len(dsl.rounds) > 0

    # 2. Visualize pattern
    visualizer = PatternVisualizer()
    frames = visualizer.dsl_to_frames(dsl, render_options={
        'width': 300,
        'height': 300,
        'show_annotations': True
    })

    assert len(frames) == len(dsl.rounds)
    assert all(frame.svg is not None for frame in frames)

    # 3. Export to PDF
    exporter = PDFExporter()
    pdf_bytes = exporter.to_pdf(dsl, include_diagrams=True)

    assert pdf_bytes is not None
    assert len(pdf_bytes) > 1000  # Sanity check: PDF has content

    # Verify PDF structure (using PyPDF2)
    pdf = PdfReader(BytesIO(pdf_bytes))
    assert len(pdf.pages) >= 2  # At least title + rounds
```

### React Native Component Integration

```typescript
// apps/mobile/__tests__/integration/GenerateVisualize.test.tsx
import { render, waitFor, fireEvent } from '@testing-library/react-native';
import { GenerateScreen } from '../../screens/GenerateScreen';
import { server } from '../mocks/server';

describe('Generate → Visualize Integration', () => {
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  it('should generate pattern and navigate to visualization', async () => {
    const { getByText, getByTestId } = render(<GenerateScreen />);

    // Fill form
    fireEvent.press(getByText('Sphere'));
    fireEvent.changeText(getByTestId('diameter-input'), '10');
    fireEvent.changeText(getByTestId('gauge-sts-input'), '14');
    fireEvent.changeText(getByTestId('gauge-rows-input'), '16');

    // Submit
    fireEvent.press(getByText('Generate Pattern'));

    // Wait for API call and navigation
    await waitFor(() => {
      expect(getByText('Round 1')).toBeTruthy();
    });

    // Verify visualization loaded
    expect(getByTestId('pattern-frame')).toBeTruthy();
  });
});
```

---

## End-to-End Testing Strategy

### Critical User Flows

E2E tests focus on **3 critical flows** that represent 80% of user value:

1. **Generate → Visualize**
2. **Export to PDF**
3. **Settings → Regenerate with new units**

### Tool Selection: Detox for React Native

**Why Detox:**
- Native React Native support
- Gray box testing (access to app internals)
- Fast, reliable synchronization
- Works on iOS and Android simulators/devices

**Setup:**

```bash
# Install Detox
cd apps/mobile
pnpm add -D detox

# Configure Detox
detox init
```

```javascript
// apps/mobile/.detoxrc.js
module.exports = {
  testRunner: 'jest',
  runnerConfig: 'e2e/config.json',
  apps: {
    'ios.debug': {
      type: 'ios.app',
      binaryPath: 'ios/build/Build/Products/Debug-iphonesimulator/KnitWit.app',
      build: 'xcodebuild -workspace ios/KnitWit.xcworkspace -scheme KnitWit -configuration Debug -sdk iphonesimulator'
    },
    'android.debug': {
      type: 'android.apk',
      binaryPath: 'android/app/build/outputs/apk/debug/app-debug.apk',
      build: 'cd android && ./gradlew assembleDebug'
    }
  },
  devices: {
    simulator: {
      type: 'ios.simulator',
      device: { type: 'iPhone 14' }
    },
    emulator: {
      type: 'android.emulator',
      device: { avdName: 'Pixel_5_API_31' }
    }
  }
};
```

### E2E Test Examples

**Flow 1: Generate → Visualize**

```typescript
// apps/mobile/e2e/generate-visualize.e2e.ts
describe('Generate and Visualize Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should generate a sphere pattern and visualize it', async () => {
    // Navigate to Generate screen
    await element(by.text('Generate')).tap();

    // Select shape
    await element(by.id('shape-sphere')).tap();

    // Enter dimensions
    await element(by.id('diameter-input')).typeText('10');
    await element(by.id('diameter-input')).tapReturnKey();

    // Enter gauge
    await element(by.id('gauge-sts-input')).typeText('14');
    await element(by.id('gauge-rows-input')).typeText('16');

    // Submit
    await element(by.text('Generate Pattern')).tap();

    // Wait for visualization screen
    await waitFor(element(by.id('pattern-frame')))
      .toBeVisible()
      .withTimeout(5000);

    // Verify first round is shown
    await expect(element(by.text('Round 1'))).toBeVisible();
    await expect(element(by.id('pattern-frame'))).toBeVisible();

    // Test navigation
    await element(by.text('Next >')).tap();
    await expect(element(by.text('Round 2'))).toBeVisible();
  });

  it('should handle validation errors gracefully', async () => {
    await element(by.text('Generate')).tap();
    await element(by.id('shape-sphere')).tap();

    // Submit without diameter
    await element(by.text('Generate Pattern')).tap();

    // Expect error message
    await expect(element(by.text('Diameter is required'))).toBeVisible();
  });
});
```

**Flow 2: Export to PDF**

```typescript
// apps/mobile/e2e/export.e2e.ts
describe('Export Flow', () => {
  beforeEach(async () => {
    await device.reloadReactNative();

    // Generate a pattern first
    await generateTestPattern();
  });

  it('should export pattern to PDF', async () => {
    // Navigate to visualization (already there from setup)
    await element(by.id('export-button')).tap();

    // Select PDF format
    await element(by.text('PDF')).tap();

    // Tap Download
    await element(by.text('Download')).tap();

    // Verify success toast
    await waitFor(element(by.text('Pattern downloaded')))
      .toBeVisible()
      .withTimeout(3000);

    // TODO: Verify file exists (requires native module)
  });
});
```

### E2E Test Environment

**Mock Backend:**
```typescript
// apps/mobile/e2e/mocks/api.ts
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

export const handlers = [
  http.post('/api/v1/patterns/generate', () => {
    return HttpResponse.json({
      pattern_id: 'test-pattern-123',
      dsl: mockSpherePattern,
      assets: {
        pdf_url: 'https://test.com/pattern.pdf'
      }
    });
  })
];

export const server = setupServer(...handlers);
```

---

## Accessibility Testing

Accessibility is a **first-class quality requirement** for Knit-Wit.

### Automated Testing

**Tools:**
- **axe-core** (via jest-axe for React Native)
- **React Native Accessibility** built-in checks
- **Lighthouse** (for web fallback)

```typescript
// apps/mobile/__tests__/accessibility/GenerateScreen.a11y.test.tsx
import { render } from '@testing-library/react-native';
import { axe, toHaveNoViolations } from 'jest-axe';
import { GenerateScreen } from '../../screens/GenerateScreen';

expect.extend(toHaveNoViolations);

describe('GenerateScreen Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<GenerateScreen />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have accessible labels for all inputs', () => {
    const { getByLabelText } = render(<GenerateScreen />);

    expect(getByLabelText('Diameter (cm)')).toBeTruthy();
    expect(getByLabelText('Gauge: Stitches per 10cm')).toBeTruthy();
    expect(getByLabelText('Gauge: Rows per 10cm')).toBeTruthy();
  });

  it('should have sufficient color contrast', async () => {
    // Verify contrast ratios meet WCAG AA
    const { getByText } = render(<GenerateScreen />);
    const button = getByText('Generate Pattern');

    // Check button has sufficient contrast (4.5:1 for normal text)
    const styles = button.props.style;
    expect(getColorContrast(styles.color, styles.backgroundColor)).toBeGreaterThan(4.5);
  });
});
```

### Manual Testing Procedures

**Weekly Accessibility Audit Checklist:**

- [ ] **Keyboard Navigation**
  - Tab through all interactive elements
  - Shift+Tab navigates backward
  - Enter/Space activates buttons
  - Esc dismisses modals

- [ ] **Screen Reader (VoiceOver/TalkBack)**
  - All buttons announced with labels
  - Form inputs have associated labels
  - Error messages are announced
  - Loading states are announced
  - Images have alt text or are marked decorative

- [ ] **Color Contrast (Colour Contrast Analyzer)**
  - Normal text: 4.5:1 minimum
  - Large text (18pt+): 3:1 minimum
  - UI components: 3:1 minimum

- [ ] **Zoom & Text Scaling**
  - Test at 200% zoom (iOS Settings → Display)
  - Layout does not break
  - Text remains readable
  - No content truncated

- [ ] **Focus Indicators**
  - Visible focus ring on all interactive elements
  - Focus order is logical

- [ ] **Forms**
  - All inputs have labels
  - Error messages are descriptive
  - Required fields are indicated

### Screen Reader Testing

**iOS VoiceOver:**
```bash
# Enable VoiceOver
Settings → Accessibility → VoiceOver → ON

# Test pattern:
1. Navigate through Generate form
2. Fill in inputs (double-tap to edit)
3. Submit form
4. Navigate visualization controls
5. Export pattern
```

**Android TalkBack:**
```bash
# Enable TalkBack
Settings → Accessibility → TalkBack → ON

# Test same pattern as iOS
```

### WCAG AA Compliance Checklist

| Criterion | Requirement | Status |
|-----------|-------------|--------|
| **1.1.1 Non-text Content** | All images have alt text | ✓ |
| **1.3.1 Info and Relationships** | Semantic structure (headings, labels) | ✓ |
| **1.4.3 Contrast (Minimum)** | 4.5:1 for normal text, 3:1 for large | ✓ |
| **1.4.4 Resize Text** | Text scales to 200% | ✓ |
| **2.1.1 Keyboard** | All functionality via keyboard | ✓ |
| **2.4.7 Focus Visible** | Focus indicators present | ✓ |
| **3.1.1 Language of Page** | Language specified | ✓ |
| **3.3.1 Error Identification** | Errors described in text | ✓ |
| **3.3.2 Labels or Instructions** | All inputs labeled | ✓ |
| **4.1.2 Name, Role, Value** | ARIA roles correct | ✓ |

---

## Performance Testing

### Backend Benchmarks

**Target:** < 200ms generation time for all shapes

```python
# packages/pattern-engine/tests/performance/test_benchmarks.py
import pytest
from pattern_engine.compilers import PatternCompiler
from pattern_engine.models import GenerateRequest

def test_sphere_generation_benchmark(benchmark):
    """Benchmark sphere pattern generation."""
    compiler = PatternCompiler()
    request = GenerateRequest(
        shape='sphere',
        diameter=10,
        gauge={'sts_per_10cm': 14, 'rows_per_10cm': 16},
        stitch='sc',
        round_mode='spiral',
        terms='US'
    )

    result = benchmark(compiler.compile, request)

    # Assert < 200ms (0.2 seconds)
    assert benchmark.stats.mean < 0.2
    assert result is not None


@pytest.mark.parametrize('diameter', [3, 10, 20, 30])
def test_sphere_scaling(benchmark, diameter):
    """Test performance scales linearly with diameter."""
    compiler = PatternCompiler()
    request = GenerateRequest(shape='sphere', diameter=diameter, ...)

    result = benchmark(compiler.compile, request)

    # All sizes should be under 200ms
    assert benchmark.stats.mean < 0.2
```

**Running Benchmarks:**
```bash
cd packages/pattern-engine
pytest tests/performance/ --benchmark-only
pytest tests/performance/ --benchmark-compare
```

### Frontend Performance

**Frame Rendering Target:** < 50ms per frame (60 fps → 16.67ms ideal)

```typescript
// apps/mobile/__tests__/performance/frame-rendering.perf.test.tsx
import { renderHook } from '@testing-library/react-hooks';
import { usePatternFrames } from '../../hooks/usePatternFrames';
import { mockSpherePattern } from '../fixtures/patterns';

describe('Frame Rendering Performance', () => {
  it('should render frames in under 50ms', () => {
    const { result } = renderHook(() => usePatternFrames(mockSpherePattern));

    const start = performance.now();
    result.current.renderFrame(5);
    const elapsed = performance.now() - start;

    expect(elapsed).toBeLessThan(50);
  });
});
```

**Profiling with React DevTools:**
```bash
# Start app in profiling mode
EXPO_PUBLIC_PROFILING=true pnpm start

# 1. Open React DevTools
# 2. Click "Profiler" tab
# 3. Click record
# 4. Navigate through pattern frames
# 5. Stop recording
# 6. Analyze flame graph for slow renders
```

### Load Testing

**Tool:** k6 (lightweight, scriptable load testing)

```javascript
// tests/load/generate-pattern.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // <1% error rate
  },
};

export default function () {
  const payload = JSON.stringify({
    shape: 'sphere',
    diameter: 10,
    gauge: { sts_per_10cm: 14, rows_per_10cm: 16 },
    stitch: 'sc',
    round_mode: 'spiral',
    terms: 'US',
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post('https://api.knitwit.app/api/v1/patterns/generate', payload, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'has pattern_id': (r) => r.json('pattern_id') !== undefined,
  });

  sleep(1);
}
```

**Running Load Tests:**
```bash
k6 run tests/load/generate-pattern.js
```

---

## Visual Regression Testing

Visual regression tests catch unintended UI changes.

### Screenshot Comparison

**Tool:** `jest-image-snapshot` (for React Native)

```typescript
// apps/mobile/__tests__/visual/PatternFrame.visual.test.tsx
import { render } from '@testing-library/react-native';
import { toMatchImageSnapshot } from 'jest-image-snapshot';
import { PatternFrame } from '../../components/PatternFrame';
import { mockSphereFrame } from '../fixtures/frames';

expect.extend({ toMatchImageSnapshot });

describe('PatternFrame Visual Regression', () => {
  it('should match snapshot for sphere round 5', () => {
    const { toJSON } = render(<PatternFrame frame={mockSphereFrame} />);

    expect(toJSON()).toMatchImageSnapshot({
      failureThreshold: 0.01,  // 1% pixel difference allowed
      failureThresholdType: 'percent',
    });
  });
});
```

### SVG Rendering Verification

```typescript
// Verify SVG output is correct
it('should render SVG with correct structure', () => {
  const { getByTestId } = render(<PatternFrame frame={mockSphereFrame} />);
  const svg = getByTestId('pattern-svg');

  // Check SVG has expected elements
  expect(svg.findByType('Circle')).toHaveLength(mockSphereFrame.stitches.length);
  expect(svg.findByType('Path')).toBeTruthy();  // Round indicator
});
```

### Cross-Device Testing

Test visual consistency across:
- **iOS:** iPhone 12 (6.1"), iPhone SE (4.7"), iPad Air (10.9")
- **Android:** Pixel 5a (6.34"), Samsung Galaxy A10 (6.2"), Galaxy Tab (10.4")

```bash
# Detox multi-device test
detox test --configuration ios.sim.iphone12
detox test --configuration ios.sim.iphoneSE
detox test --configuration android.emu.pixel5
```

---

## Test Data & Fixtures

### Pattern DSL Fixtures

```python
# packages/pattern-engine/tests/fixtures/patterns.py
SPHERE_10CM_SC = {
    'metadata': {
        'shape': 'sphere',
        'diameter': 10,
        'gauge': {'sts_per_10cm': 14, 'rows_per_10cm': 16},
        'stitch': 'sc',
        'round_mode': 'spiral',
        'terms': 'US'
    },
    'rounds': [
        {'round': 1, 'operations': [{'type': 'magic_ring', 'stitches': 6}]},
        {'round': 2, 'operations': [{'type': 'inc', 'count': 6}]},
        # ... more rounds
    ]
}

CYLINDER_6X8_DC = {
    'metadata': {
        'shape': 'cylinder',
        'diameter': 6,
        'height': 8,
        'gauge': {'sts_per_10cm': 12, 'rows_per_10cm': 14},
        'stitch': 'dc',
        'caps': 'both',
        'terms': 'US'
    },
    'rounds': [
        # ... cylinder pattern
    ]
}
```

### Test Gauge Data

```python
# Common gauge values for testing
GAUGES = {
    'sc_tight': {'sts_per_10cm': 16, 'rows_per_10cm': 18},
    'sc_standard': {'sts_per_10cm': 14, 'rows_per_10cm': 16},
    'sc_loose': {'sts_per_10cm': 12, 'rows_per_10cm': 14},
    'dc_standard': {'sts_per_10cm': 10, 'rows_per_10cm': 12},
    'hdc_standard': {'sts_per_10cm': 12, 'rows_per_10cm': 14},
}
```

### Mock API Responses

```typescript
// apps/mobile/__tests__/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.post('/api/v1/patterns/generate', () => {
    return HttpResponse.json({
      pattern_id: 'mock-pattern-123',
      dsl: SPHERE_10CM_SC,
      assets: {
        pdf_url: 'https://mock.com/pattern.pdf',
        svg_frames: Array(20).fill(null).map((_, i) => ({
          round: i + 1,
          svg: '<svg>...</svg>'
        }))
      }
    });
  }),

  http.get('/api/v1/patterns/:id', ({ params }) => {
    return HttpResponse.json({
      pattern_id: params.id,
      dsl: SPHERE_10CM_SC,
      created_at: '2025-11-05T10:00:00Z'
    });
  })
];
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          pip install -r apps/api/requirements.txt
          cd apps/mobile && pnpm install

      - name: Lint Backend
        run: cd apps/api && black --check . && isort --check .

      - name: Lint Frontend
        run: cd apps/mobile && pnpm lint

  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r apps/api/requirements.txt

      - name: Run unit tests
        run: cd packages/pattern-engine && pytest tests/unit/ --cov --cov-report=xml

      - name: Run integration tests
        run: cd apps/api && pytest tests/integration/

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: backend

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: cd apps/mobile && pnpm install

      - name: Run tests
        run: cd apps/mobile && pnpm test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./apps/mobile/coverage/lcov.info
          flags: frontend

  e2e:
    runs-on: macos-latest
    strategy:
      matrix:
        platform: [ios, android]
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: cd apps/mobile && pnpm install

      - name: Build app
        run: cd apps/mobile && detox build --configuration ${{ matrix.platform }}.sim.debug

      - name: Run E2E tests
        run: cd apps/mobile && detox test --configuration ${{ matrix.platform }}.sim.debug

      - name: Upload E2E artifacts
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-screenshots-${{ matrix.platform }}
          path: apps/mobile/e2e/screenshots/

  quality-gate:
    needs: [lint, test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - name: Check coverage threshold
        run: |
          # Fail if coverage < 70%
          if [ $(curl -s https://codecov.io/api/gh/${{ github.repository }}/coverage | jq '.commit.totals.c') -lt 70 ]; then
            echo "Coverage below 70%"
            exit 1
          fi
```

### Quality Gates

Tests must pass before merging:

- ✅ Lint (ESLint, Black)
- ✅ Unit tests (80%+ coverage backend, 60%+ frontend)
- ✅ Integration tests (all pass)
- ✅ E2E tests (critical flows pass)
- ✅ No new accessibility violations

---

## Testing Schedule

### Pre-Commit (Local)

**Run Time:** < 1 minute

```bash
# Git pre-commit hook (.git/hooks/pre-commit)
#!/bin/bash
pnpm lint-staged
```

### Pull Request (CI)

**Run Time:** ~15 minutes

- Lint (2 min)
- Unit tests (5 min)
- Integration tests (5 min)
- Build verification (3 min)

### Nightly (Scheduled)

**Run Time:** ~45 minutes
**Schedule:** 2 AM UTC daily

- Full test suite (unit + integration + E2E)
- Performance benchmarks
- Visual regression tests
- Load testing (staging environment)
- Accessibility audits

### Pre-Release

**Run Time:** ~2 hours
**Trigger:** Manual before release candidate

- Full E2E suite on real devices (iOS 14-17, Android 10-14)
- Cross-device visual regression
- Manual accessibility audit
- Performance profiling
- Load testing (production-like environment)

---

## Tools & Technologies

### Testing Frameworks

| Tool | Purpose | Version |
|------|---------|---------|
| **pytest** | Python unit/integration testing | 7+ |
| **Jest** | JavaScript/TypeScript testing | 29+ |
| **React Testing Library** | React Native component testing | Latest |
| **Detox** | E2E testing for React Native | 20+ |

### Coverage & Reporting

| Tool | Purpose |
|------|---------|
| **pytest-cov** | Python coverage |
| **jest --coverage** | JavaScript coverage |
| **Codecov** | Coverage reporting & tracking |

### Performance Testing

| Tool | Purpose |
|------|---------|
| **pytest-benchmark** | Python performance benchmarking |
| **React DevTools Profiler** | Frontend performance profiling |
| **k6** | Load testing |

### Accessibility Testing

| Tool | Purpose |
|------|---------|
| **axe-core** | Automated accessibility testing |
| **jest-axe** | Accessibility testing for React |
| **VoiceOver** | iOS screen reader testing |
| **TalkBack** | Android screen reader testing |
| **Colour Contrast Analyzer** | Manual contrast checking |

### Visual Regression

| Tool | Purpose |
|------|---------|
| **jest-image-snapshot** | Screenshot comparison |

### Mocking & Fixtures

| Tool | Purpose |
|------|---------|
| **pytest-mock** | Python mocking |
| **msw** (Mock Service Worker) | API mocking for frontend |
| **@testing-library/react-native** | Component rendering |

### Setup Instructions

```bash
# Backend testing setup
cd apps/api
pip install pytest pytest-cov pytest-mock pytest-benchmark

# Frontend testing setup
cd apps/mobile
pnpm add -D jest @testing-library/react-native @testing-library/jest-native
pnpm add -D detox jest-image-snapshot msw

# Initialize Detox
detox init

# Run tests
pnpm test          # Frontend
pytest --cov       # Backend
detox test         # E2E
```

---

## Summary

This testing strategy ensures **high quality, accessibility, and performance** for Knit-Wit MVP:

- **70% unit tests** for fast feedback and algorithm correctness
- **20% integration tests** for API contracts and full pipeline validation
- **10% E2E tests** for critical user flows
- **Automated accessibility testing** with manual audits weekly
- **Performance benchmarks** enforced in CI (< 200ms generation, < 50ms rendering)
- **Visual regression testing** to catch UI breakages
- **Comprehensive CI/CD integration** with quality gates

**Key Success Metrics:**
- 80%+ backend coverage, 60%+ frontend coverage
- < 200ms pattern generation
- WCAG AA compliance
- < 5% bug escape rate (Phase 4+)

For overall project context, see [Implementation Plan](../implementation-plan.md).
