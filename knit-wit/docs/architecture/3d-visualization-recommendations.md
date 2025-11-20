# 3D Visualization: Architectural Recommendations & Decision Rationale

**Companion Document to:** 3d-visualization-design.md
**Date:** 2025-11-19
**Author:** Lead Architect

---

## Executive Summary of Recommendations

This document provides architectural recommendations and decision rationale for the 3D visualization feature. After analyzing the existing 2D polar visualization system and evaluating multiple approaches, the recommended strategy is:

**1. Extend existing endpoint** (not create a new one)
**2. Use isometric projection** for Phase 1 (SVG-based)
**3. Generate 3D coordinates in backend** using shape-aware geometric algorithms
**4. Implement painter's algorithm** for visibility handling
**5. Design for WebGL migration** in Phase 2

---

## Key Architectural Decisions

### 1. API Design: Extend vs. New Endpoint

**RECOMMENDATION: Extend existing `/visualization/frames` endpoint**

**Rationale:**

The current endpoint at `POST /api/v1/visualization/frames` accepts a `FrontendPatternDSL` and returns `VisualizationResponse`. The cleanest integration is to:

1. Add optional query parameter: `?mode=3d` (defaults to `2d`)
2. Extend `RenderNode` model with optional `position_3d` and `depth_order` fields
3. Add optional `projection` field to `VisualizationFrame`

**Advantages:**
- Single source of truth (no data sync issues)
- Backward compatible (existing clients unaffected)
- Simpler frontend state management (one API call, not two)
- Reduces API surface area and maintenance burden

**Alternatives Rejected:**

| Alternative | Reason for Rejection |
|-------------|---------------------|
| New `/visualization/frames3d` endpoint | Duplicates logic, requires state synchronization |
| Client-side 3D generation | Too complex, inconsistent across platforms, breaks server authority |
| WebSocket streaming | Overkill for MVP, adds infrastructure complexity |

**Implementation Note:**

```python
@router.post("/frames", response_model=VisualizationResponse)
async def generate_visualization_frames(
    pattern: FrontendPatternDSL,
    mode: Literal["2d", "3d"] = "2d"  # Backward compatible default
) -> VisualizationResponse:
    if mode == "3d":
        return visualization_service.pattern_to_visualization_3d(pattern)
    else:
        return visualization_service.pattern_to_visualization(pattern)
```

---

### 2. Projection Method: Isometric vs. Perspective

**RECOMMENDATION: Isometric projection (30° angle) for Phase 1**

**Rationale:**

Isometric projection provides the optimal balance of depth perception, simplicity, and performance for crochet pattern visualization:

1. **Parallel lines preserved:** Easier to count stitches and understand structure
2. **No perspective distortion:** Measurements appear accurate (critical for crafters)
3. **Mathematically simple:** Linear transformation, no camera matrix management
4. **Computationally cheap:** O(1) per vertex, no matrix multiplications
5. **Familiar to crafters:** Standard in knitting charts and technical diagrams

**Mathematical Simplicity:**

```typescript
// Isometric: Two multiplications per point
x_screen = x - z * 0.866
y_screen = y - z * 0.5

// vs. Perspective: Division, matrix ops, FOV calculations
const scale = fov / (fov + z);
x_screen = x * scale;
y_screen = y * scale;
```

**Visual Comparison:**

| Aspect | Isometric | Perspective |
|--------|-----------|-------------|
| Depth perception | Good (via size/opacity) | Excellent (natural) |
| Line parallelism | Preserved | Converge to vanishing point |
| Measurement accuracy | Accurate | Distorted at edges |
| Implementation | Simple | Complex (camera management) |
| Performance | Fast | Slower (matrix ops) |
| Familiarity | Technical diagrams | Video games |

**Fallback Option:**

If user testing reveals insufficient depth perception, switch to **dimetric projection** (35.26° angle) with minimal code change:

```typescript
const angle = 35.26 * (Math.PI / 180);  // Only change needed
```

Dimetric provides slightly exaggerated z-axis, improving depth at minimal cost.

---

### 3. 3D Coordinate Generation: Shape-Aware Algorithms

**RECOMMENDATION: Backend generates 3D coordinates using geometric formulas**

**Rationale:**

The backend already has shape knowledge through the pattern engine's sphere, cylinder, and cone generators. Reusing this knowledge for 3D coordinate generation:

1. **Ensures geometric consistency:** 3D coordinates match physical crochet structure
2. **Single source of truth:** Backend owns shape calculations
3. **Simplifies frontend:** Frontend only projects and renders, no geometry logic
4. **Enables validation:** Backend can verify coordinates lie on shape surface

**Algorithm Design:**

Each shape uses its natural coordinate system:

| Shape | Natural Coordinates | Formula |
|-------|---------------------|---------|
| **Sphere** | Spherical (θ, φ, r) | `x = r·sin(θ)·cos(φ)`, `y = r·sin(θ)·sin(φ)`, `z = r·cos(θ)` |
| **Cylinder** | Cylindrical (φ, z, r) | `x = r·cos(φ)`, `y = r·sin(φ)`, `z = height` |
| **Cone** | Tapered cylindrical | `r(z) = r_base·(1 - z/h)`, then cylindrical |

**Progressive Construction:**

For "show construction up to round N" feature:

```python
def generate_partial_visualization(
    pattern: PatternDSL,
    up_to_round: int
) -> VisualizationResponse:
    """
    Show progressive construction (e.g., hemisphere at round 10 of 20-round sphere).
    """
    frames = []
    for round_idx in range(up_to_round):
        frame = round_to_3d_frame(
            pattern.rounds[round_idx],
            round_idx,
            total_rounds=len(pattern.rounds),
            shape_type=pattern.shape.shape_type
        )
        frames.append(frame)

    return VisualizationResponse(frames=frames, ...)
```

This naturally shows a half-sphere at the midpoint, which is exactly what the user would see when crocheting!

**Extensibility to Complex Shapes (Phase 2):**

For arbitrary mesh shapes:

```python
class MeshBasedShape:
    """Phase 2: Arbitrary mesh support."""

    def map_stitches_to_vertices(
        self,
        pattern: PatternDSL,
        mesh: Mesh
    ) -> Dict[str, Tuple[float, float, float]]:
        """
        Map stitches to mesh vertices using one of:
        1. UV parameterization (rounds → u, stitches → v)
        2. Geodesic distance (equal spacing on surface)
        3. Vertex snapping (closest vertex to parameterized position)
        """
        # Implementation in Phase 2
        pass
```

---

### 4. Visibility Handling: Painter's Algorithm

**RECOMMENDATION: Painter's algorithm with backend depth sorting**

**Rationale:**

For simple geometric shapes (sphere, cylinder, cone), painter's algorithm provides sufficient occlusion handling:

1. **Simple to implement:** Sort by z-coordinate, render back-to-front
2. **Works well for spheres:** No complex overlap issues
3. **Backend computes once:** Frontend just renders in order
4. **Accessible:** Depth order enables screen reader announcements

**Algorithm:**

```python
def compute_depth_order(nodes: List[RenderNode]) -> List[RenderNode]:
    """
    Sort nodes by z-coordinate (ascending = back to front).

    Returns nodes with depth_order assigned (0 = farthest back).
    """
    sorted_nodes = sorted(
        nodes,
        key=lambda n: n.position_3d[2] if n.position_3d else 0
    )

    for idx, node in enumerate(sorted_nodes):
        node.depth_order = idx

    return sorted_nodes
```

**Limitations & Phase 2 Migration:**

Painter's algorithm fails for:
- Complex overlapping geometry (self-intersecting meshes)
- Transparent overlaps (semi-transparent stitches)

These issues are addressed in Phase 2 with WebGL:
- Z-buffer automatically handles occlusion
- Alpha blending handles transparency
- Keep `depth_order` for accessibility fallback

**Accessibility Benefit:**

```typescript
const getA11yLabel = (node: RenderNode) => {
  const total = frame.nodes.length;
  const depth_pct = (node.depth_order / total) * 100;

  const layer =
    depth_pct < 33 ? 'back' :
    depth_pct < 66 ? 'middle' : 'front';

  return `Stitch ${node.id}, ${node.stitch_type}, ${layer} layer`;
};
```

---

### 5. Visual Depth Encoding: Multi-Modal Cues

**RECOMMENDATION: Combine size scaling + opacity + z-index**

**Rationale:**

Relying on a single depth cue (e.g., only color) fails for accessibility and clarity. Multi-modal encoding:

1. **Size scaling:** Closer stitches appear larger (natural perspective)
2. **Opacity:** Farther stitches fade slightly (atmospheric depth)
3. **Z-index:** Correct overlap order (via `depth_order`)

**Parameters:**

```typescript
const depth_normalized = (z - z_min) / (z_max - z_min);

// Size: 60% → 100% based on depth
const radius = baseRadius * (0.6 + 0.4 * depth_normalized);

// Opacity: 70% → 100% based on depth
const opacity = 0.7 + 0.3 * depth_normalized;
```

**Accessibility Considerations:**

| User Need | Solution |
|-----------|----------|
| Colorblind users | Don't rely on color for depth (use size/opacity) |
| Low vision | Ensure 70% opacity meets contrast ratios |
| High contrast mode | Increase opacity range to 85% → 100% |
| Reduced motion | Disable depth animations, static encoding only |
| Screen readers | Announce "front/middle/back layer" based on depth_order |

**Alternatives Considered:**

| Encoding | Pros | Cons |
|----------|------|------|
| Color temperature (warm=front) | Subtle, artistic | Not colorblind-friendly, conflicts with highlight colors |
| Stroke width variation | No fill changes | Less noticeable, accessibility issues |
| Shadow/blur effects | Realistic | High performance cost, noisy visuals |

---

## Performance Analysis

### Backend Performance

**Target:** < 150ms for 3D frame generation (50% overhead vs. 2D)

**Breakdown:**

| Operation | 2D Time | 3D Time | Notes |
|-----------|---------|---------|-------|
| Coordinate generation | 30ms | 50ms | Trig functions (sin/cos) per stitch |
| Edge generation | 10ms | 10ms | Unchanged |
| Depth sorting | N/A | 20ms | O(n log n) sort |
| Bounds calculation | N/A | 5ms | Min/max of coordinates |
| Serialization | 20ms | 25ms | Larger payload |
| **Total** | **60ms** | **110ms** | **+83% overhead** |

**Optimizations:**

1. **Vectorize with NumPy:**
   ```python
   # Instead of loop:
   for i in range(n):
       x = r * cos(angle[i])  # Slow

   # Vectorized:
   x = r * np.cos(angles)  # 10x faster
   ```

2. **Lazy depth sorting:**
   ```python
   # Skip sorting for cylinders (z-coordinate already ordered by round)
   if shape_type == "cylinder":
       depth_order = list(range(len(nodes)))  # O(n) instead of O(n log n)
   ```

3. **Geometric bounds:**
   ```python
   # Don't iterate nodes for bounds (O(n) → O(1))
   def get_sphere_bounds(radius: float):
       return {'x_min': -radius, 'x_max': radius, ...}
   ```

**Estimated Optimized Performance:**

| Pattern Size | 2D Time | 3D Time (optimized) | Overhead |
|--------------|---------|---------------------|----------|
| Small (200 stitches) | 50ms | 70ms | +40% |
| Medium (1000 stitches) | 100ms | 140ms | +40% |
| Large (4000 stitches) | 200ms | 280ms | +40% |

---

### Frontend Performance

**Target:** 60 FPS (16.67ms per frame), no regression vs. 2D

**Breakdown:**

| Operation | 2D Time | 3D Time | Notes |
|-----------|---------|---------|-------|
| API fetch | 100ms | 140ms | Backend overhead |
| Projection calculation | N/A | 2ms | Simple arithmetic per node |
| Depth normalization | N/A | 1ms | One-time calculation |
| SVG rendering | 10ms | 12ms | Slightly more complex styles |
| **Total per render** | **10ms** | **15ms** | **Still 60 FPS** |

**Optimizations:**

1. **Memoize projection:**
   ```typescript
   const projectedNodes = useMemo(() =>
     nodes.map(n => ({
       ...n,
       screen: projectIsometric(n.position_3d)
     })),
     [nodes, projection.angle_deg]  // Only recalc if data changes
   );
   ```

2. **Viewport culling (3D-aware):**
   ```typescript
   // Cull nodes outside viewport AND behind camera
   const visibleNodes = projectedNodes.filter(n =>
     isInViewport(n.screen) && n.depth_order > cullingThreshold
   );
   ```

3. **LOD based on depth:**
   ```typescript
   // Reduce detail for distant stitches
   const lodLevel =
     depth_norm < 0.3 ? 'minimal' :   // Far: 4px circles, no stroke
     depth_norm < 0.7 ? 'reduced' :   // Mid: 6px circles, 1px stroke
                        'full';       // Close: 8px circles, 2px stroke
   ```

---

## Migration Path to WebGL (Phase 2)

### Why WebGL in Phase 2?

Phase 1 (SVG) handles simple geometric shapes well, but WebGL becomes necessary for:

1. **Complex shapes:** Arbitrary meshes (e.g., amigurumi animals, clothing)
2. **Large patterns:** 10,000+ stitches (SVG performance degrades)
3. **Interactive camera:** Rotate, zoom, pan (orbit controls)
4. **Advanced rendering:** Lighting, shadows, realistic materials
5. **Animation:** Smooth round-by-round construction with interpolation

### Progressive Enhancement Strategy

```typescript
// Capability detection
const useRenderer = (mode: '2d' | '3d', capabilities: Capabilities) => {
  if (mode === '2d') {
    return new SVGRenderer2D();
  }

  // Use WebGL for complex/large patterns if supported
  if (capabilities.webgl && (isComplex || nodeCount > 500)) {
    return new WebGLRenderer();
  }

  // Fallback to SVG for simple patterns or no WebGL
  return new SVGRenderer3DIsometric();
};
```

### WebGL Feature Roadmap

| Feature | Phase 1 (SVG) | Phase 2 (WebGL) |
|---------|---------------|-----------------|
| **Rendering** | | |
| Projection | Isometric (fixed) | Perspective (camera) |
| Occlusion | Painter's algorithm | Z-buffer |
| Lighting | Flat colors | Phong/PBR shading |
| Anti-aliasing | SVG native | MSAA/FXAA |
| **Interaction** | | |
| Camera rotation | No | Orbit controls |
| Zoom | SVG scale | Camera FOV |
| Pan | SVG translate | Camera position |
| **Geometry** | | |
| Shapes | Sphere, cylinder, cone | + Arbitrary meshes |
| Stitch placement | Geometric formulas | UV/geodesic mapping |
| Max stitches | ~500 (60 FPS) | 10,000+ (60 FPS) |
| **Visual Features** | | |
| Highlights | Color coding | + Glow effects |
| Depth | Size/opacity | + Shadows/AO |
| Animation | Frame stepping | Smooth interpolation |

### Data Model Extensibility

**Phase 1 (Geometric):**

```python
class RenderNode(BaseModel):
    position: Tuple[float, float]           # 2D (always)
    position_3d: Optional[Tuple[float, float, float]]  # 3D (geometric)
    depth_order: Optional[int]
```

**Phase 2 (Mesh-based):**

```python
class MeshMetadata(BaseModel):
    vertices: List[Tuple[float, float, float]]  # Mesh vertices
    faces: List[Tuple[int, int, int]]           # Triangle faces
    normals: List[Tuple[float, float, float]]   # Vertex normals

    # Map stitches to mesh vertices
    stitch_vertex_map: Dict[str, int]  # stitch_id → vertex_index

class VisualizationFrame(BaseModel):
    # ... existing fields ...
    mesh: Optional[MeshMetadata] = None  # For complex shapes
```

**Stitch Placement on Mesh (Phase 2):**

```python
def map_stitches_to_mesh(
    pattern: PatternDSL,
    mesh: Mesh
) -> Dict[str, int]:
    """
    Map stitches to mesh vertices.

    Algorithm options:
    1. UV Parameterization:
       - Map (round, stitch) → (u, v) texture coordinates
       - Find mesh vertex at (u, v)

    2. Geodesic Distance:
       - Place stitches at equal geodesic distances on surface
       - Ensures even distribution regardless of mesh shape

    3. Vertex Snapping:
       - Calculate ideal positions geometrically
       - Snap to nearest mesh vertices
    """
    # Phase 2 implementation
    pass
```

---

## Testing Strategy

### Backend Tests

**Unit Tests (80%+ coverage):**

```python
class TestSphere3DGeneration(unittest.TestCase):
    def test_coordinates_on_sphere_surface(self):
        """All 3D coordinates should lie on sphere surface."""
        service = VisualizationService()
        pattern = generate_test_sphere(diameter=10)
        frames = service.dsl_to_frames_3d(pattern)

        radius = 5.0
        for frame in frames:
            for node in frame.nodes:
                x, y, z = node.position_3d
                distance = math.sqrt(x**2 + y**2 + z**2)
                self.assertAlmostEqual(distance, radius, places=2)

    def test_depth_order_monotonic(self):
        """Depth order should increase with z-coordinate."""
        # ...

    def test_progressive_construction(self):
        """Partial rounds should show partial shape (e.g., hemisphere)."""
        pattern = generate_test_sphere(diameter=10)
        half_frames = service.dsl_to_frames_3d(
            pattern,
            up_to_round=len(pattern.rounds) // 2
        )

        # Verify all z-coordinates are positive (northern hemisphere)
        for frame in half_frames:
            for node in frame.nodes:
                self.assertGreaterEqual(node.position_3d[2], 0)
```

**Integration Tests:**

```python
class TestVisualizationAPI(TestCase):
    def test_3d_mode_includes_extended_fields(self):
        response = client.post(
            '/api/v1/visualization/frames?mode=3d',
            json=test_pattern
        )

        assert response.status_code == 200
        frame = response.json()['frames'][0]
        assert 'projection' in frame
        assert frame['projection']['type'] == 'isometric'

        node = frame['nodes'][0]
        assert 'position_3d' in node
        assert 'depth_order' in node

    def test_2d_mode_backward_compatible(self):
        """2D mode should not include 3D fields."""
        response = client.post(
            '/api/v1/visualization/frames',  # No mode param
            json=test_pattern
        )

        node = response.json()['frames'][0]['nodes'][0]
        assert 'position' in node
        assert 'position_3d' not in node
```

---

### Frontend Tests

**Unit Tests:**

```typescript
describe('projectIsometric', () => {
  it('projects origin correctly', () => {
    const [x, y] = projectIsometric(0, 0, 0);
    expect(x).toBe(0);
    expect(y).toBe(0);
  });

  it('projects points correctly (30° angle)', () => {
    const [x, y] = projectIsometric(100, 0, 50);
    const angle = 30 * (Math.PI / 180);

    expect(x).toBeCloseTo(100 - 50 * Math.cos(angle), 2);
    expect(y).toBeCloseTo(0 - 50 * Math.sin(angle), 2);
  });
});

describe('depth encoding', () => {
  it('applies size scaling based on depth', () => {
    const depth_norm = 0.5;
    const radius = 8 * (0.6 + 0.4 * depth_norm);
    expect(radius).toBe(6.4);  // 80% of base size at mid-depth
  });

  it('applies opacity scaling based on depth', () => {
    const depth_norm = 0.0;  // Farthest back
    const opacity = 0.7 + 0.3 * depth_norm;
    expect(opacity).toBe(0.7);  // 70% opacity at back
  });
});
```

**Accessibility Tests:**

```typescript
describe('3D Visualization Accessibility', () => {
  it('announces mode change to screen readers', async () => {
    const announceSpy = jest.spyOn(AccessibilityInfo, 'announceForAccessibility');

    const { rerender } = render(<VisualizationScreen mode="2d" />);
    rerender(<VisualizationScreen mode="3d" />);

    expect(announceSpy).toHaveBeenCalledWith(
      expect.stringContaining('Switched to 3D view')
    );
  });

  it('provides depth layer information in labels', () => {
    const { getByLabelText } = render(<SVGRenderer3D ... />);

    const frontStitch = getByLabelText(/front layer/);
    const backStitch = getByLabelText(/back layer/);

    expect(frontStitch).toBeDefined();
    expect(backStitch).toBeDefined();
  });
});
```

**Visual Regression Tests:**

```typescript
// Use Percy, Chromatic, or similar
describe('3D Visualization Visual Regression', () => {
  it('renders sphere in 3D mode', async () => {
    const { container } = render(
      <VisualizationScreen pattern={spherePattern} mode="3d" />
    );

    await waitForElement(() => getByTestId(container, 'svg-renderer'));
    await percySnapshot('sphere-3d-isometric-view');
  });

  it('renders cylinder in 3D mode', async () => {
    // ...
  });
});
```

---

## Risk Analysis

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Insufficient depth perception (isometric)** | Medium | Low | Fallback to dimetric (35°), add configurable angle |
| **Performance regression on low-end devices** | High | Medium | Aggressive viewport culling, LOD system |
| **Occlusion artifacts (painter's algorithm)** | Low | Low | Acceptable for geometric shapes, fixed in Phase 2 |
| **Complex shape support delayed** | Medium | Medium | Phase 2 WebGL already planned |
| **Accessibility issues** | High | Low | Multi-modal depth cues, screen reader support |

### User Experience Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Users prefer 2D view** | Low | Low | Keep 2D default, 3D opt-in via toggle |
| **Confusion with 3D controls** | Medium | Low | Minimal controls in Phase 1 (static view only) |
| **3D doesn't help understanding** | Medium | Low | User testing in beta, gather feedback |

---

## Recommendations Summary

### Immediate Actions (Before Implementation)

1. **Create prototype:** Build isometric projection spike in sandbox
2. **Performance benchmark:** Test coordinate generation on target patterns
3. **User testing:** Show mockups to crochet community, gather feedback
4. **Accessibility audit:** Review depth encoding with a11y experts

### Implementation Priorities

**Phase 1 (MVP):**
1. Backend 3D coordinate generation (sphere, cylinder, cone)
2. API extension with backward compatibility
3. Frontend isometric rendering
4. 2D/3D toggle UI
5. Accessibility features (screen reader, depth labels)

**Phase 2 (Future):**
1. WebGL renderer with camera controls
2. Mesh-based shape support
3. Advanced visual features (lighting, shadows)
4. Animations and interactions

### Success Criteria

| Metric | Target |
|--------|--------|
| Backend performance | < 150ms (3D frame generation) |
| Frontend performance | 60 FPS (no regression) |
| Accessibility | WCAG AA compliant |
| User satisfaction | 70%+ find 3D helpful (beta survey) |
| Backward compatibility | 100% (2D visualization unchanged) |

---

## Conclusion

The recommended architecture extends the existing 2D visualization system to support 3D rendering through:

1. **Minimal API changes:** Optional 3D fields, backward compatible
2. **Simple mathematics:** Isometric projection, geometric coordinate generation
3. **Progressive enhancement:** SVG Phase 1, WebGL Phase 2
4. **Accessibility-first:** Multi-modal depth cues, screen reader support

This approach balances simplicity (Phase 1 MVP), performance (SVG for < 500 nodes), and future extensibility (WebGL for complex shapes).

**Next Steps:**
1. Review this design with backend, frontend, and UX teams
2. Build prototype spike to validate isometric projection
3. Gather user feedback on 3D mockups
4. Proceed with Phase 1 implementation if approved
