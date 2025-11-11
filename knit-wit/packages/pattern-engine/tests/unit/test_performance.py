"""
Performance Benchmarks for Pattern Engine

Comprehensive performance tests for all shape compilers with statistical analysis.
Tests ensure pattern generation meets the < 200ms target for typical inputs.

Benchmark Approach:
- Multiple iterations (100 for typical, 50 for large patterns)
- Statistical analysis (mean, median, max, stdev)
- Clear pass/fail criteria
- Console output for documentation

Test Coverage:
- Sphere: 10cm standard, 25cm large
- Cylinder: 8cm x 12cm with caps
- Cone: 6cm→2cm x 8cm tapered

Performance Targets:
- Typical patterns: < 200ms average, < 300ms worst case
- Large patterns: < 500ms average

Run with: pytest -v -m benchmark tests/unit/test_performance.py
"""

import pytest
import time
from statistics import mean, median, stdev
from knit_wit_engine.shapes import SphereCompiler, CylinderCompiler, ConeCompiler
from knit_wit_engine.models.requests import Gauge


@pytest.mark.benchmark
class TestSpherePerformance:
    """Performance benchmarks for sphere generation."""

    def test_benchmark_sphere_10cm(self):
        """Benchmark sphere generation (100 iterations)."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        times = []
        for _ in range(100):
            start = time.perf_counter()
            pattern = compiler.generate(diameter_cm=10, gauge=gauge)
            elapsed = time.perf_counter() - start
            times.append(elapsed * 1000)  # Convert to milliseconds

        avg_time = mean(times)
        median_time = median(times)
        max_time = max(times)
        std_time = stdev(times)

        print(f"\n--- Sphere 10cm Benchmark ---")
        print(f"  Iterations: 100")
        print(f"  Average: {avg_time:.2f} ms")
        print(f"  Median: {median_time:.2f} ms")
        print(f"  Max: {max_time:.2f} ms")
        print(f"  Std Dev: {std_time:.2f} ms")
        print(f"  Target: < 200 ms")

        assert avg_time < 200, f"Average time {avg_time:.2f}ms exceeds 200ms target"
        assert max_time < 300, f"Max time {max_time:.2f}ms exceeds 300ms worst case"


@pytest.mark.benchmark
class TestCylinderPerformance:
    """Performance benchmarks for cylinder generation."""

    def test_benchmark_cylinder_8cm(self):
        """Benchmark cylinder generation (100 iterations)."""
        compiler = CylinderCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        times = []
        for _ in range(100):
            start = time.perf_counter()
            pattern = compiler.generate(
                diameter_cm=8,
                height_cm=12,
                gauge=gauge,
                has_caps=True
            )
            elapsed = time.perf_counter() - start
            times.append(elapsed * 1000)

        avg_time = mean(times)
        median_time = median(times)
        max_time = max(times)
        std_time = stdev(times)

        print(f"\n--- Cylinder 8cm × 12cm Benchmark ---")
        print(f"  Iterations: 100")
        print(f"  Average: {avg_time:.2f} ms")
        print(f"  Median: {median_time:.2f} ms")
        print(f"  Max: {max_time:.2f} ms")
        print(f"  Std Dev: {std_time:.2f} ms")
        print(f"  Target: < 200 ms")

        assert avg_time < 200, f"Average time {avg_time:.2f}ms exceeds 200ms target"
        assert max_time < 300, f"Max time {max_time:.2f}ms exceeds 300ms worst case"


@pytest.mark.benchmark
class TestConePerformance:
    """Performance benchmarks for cone generation."""

    def test_benchmark_cone_8cm(self):
        """Benchmark cone generation (100 iterations)."""
        compiler = ConeCompiler()
        gauge = Gauge(sts_per_10cm=14, rows_per_10cm=16)

        times = []
        for _ in range(100):
            start = time.perf_counter()
            pattern = compiler.generate(
                diameter_start_cm=6,
                diameter_end_cm=2,
                height_cm=8,
                gauge=gauge
            )
            elapsed = time.perf_counter() - start
            times.append(elapsed * 1000)

        avg_time = mean(times)
        median_time = median(times)
        max_time = max(times)
        std_time = stdev(times)

        print(f"\n--- Cone 6cm→2cm × 8cm Benchmark ---")
        print(f"  Iterations: 100")
        print(f"  Average: {avg_time:.2f} ms")
        print(f"  Median: {median_time:.2f} ms")
        print(f"  Max: {max_time:.2f} ms")
        print(f"  Std Dev: {std_time:.2f} ms")
        print(f"  Target: < 200 ms")

        assert avg_time < 200, f"Average time {avg_time:.2f}ms exceeds 200ms target"
        assert max_time < 300, f"Max time {max_time:.2f}ms exceeds 300ms worst case"


@pytest.mark.benchmark
class TestLargePatternPerformance:
    """Performance benchmarks for large patterns."""

    def test_benchmark_large_sphere_25cm(self):
        """Benchmark large sphere (25cm with fine gauge)."""
        compiler = SphereCompiler()
        gauge = Gauge(sts_per_10cm=18, rows_per_10cm=20)  # Fine gauge

        times = []
        for _ in range(50):  # Fewer iterations for large patterns
            start = time.perf_counter()
            pattern = compiler.generate(diameter_cm=25, gauge=gauge)
            elapsed = time.perf_counter() - start
            times.append(elapsed * 1000)

        avg_time = mean(times)
        median_time = median(times)
        max_time = max(times)
        std_time = stdev(times)

        print(f"\n--- Large Sphere 25cm (Fine Gauge) Benchmark ---")
        print(f"  Iterations: 50")
        print(f"  Average: {avg_time:.2f} ms")
        print(f"  Median: {median_time:.2f} ms")
        print(f"  Max: {max_time:.2f} ms")
        print(f"  Std Dev: {std_time:.2f} ms")
        print(f"  Rounds: {len(pattern.rounds)}")
        print(f"  Max stitches: {max(r.total_stitches for r in pattern.rounds)}")
        print(f"  Target: < 500 ms")

        assert avg_time < 500, f"Average time {avg_time:.2f}ms exceeds 500ms target for large patterns"
        assert max_time < 750, f"Max time {max_time:.2f}ms exceeds 750ms worst case for large patterns"
