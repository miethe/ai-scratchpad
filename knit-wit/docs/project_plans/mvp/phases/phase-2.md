# Phase 2: Visualization Foundation



**Duration:** Weeks 5-7 (Sprints 3-4)

**Team:** 2 BE, 2 FE, 1 QA

**Capacity:** 120-140 story points

**Status:** Planned



---



## Phase Overview



Phase 2 establishes the visualization foundation for interactive pattern rendering. This phase bridges the pattern engine (Phase 1) with the user interface, enabling step-by-step visual guidance through crochet patterns.



**Core Deliverables:**

- Backend: DSL → visualization frames conversion

- Frontend: RN/Expo app shell with navigation

- Frontend: SVG rendering engine (react-native-svg)

- Frontend: Round scrubber and step controls

- Frontend: Basic stitch highlighting and tooltips

- Frontend: WCAG AA accessibility baseline



**Key Technologies:**

- Backend: Pattern DSL → RenderPrimitive models

- Frontend: react-native-svg, React Navigation, Zustand

- Testing: Jest (FE), pytest (BE), accessibility audits



### Phase Context



**Preceding Phase:**

- Phase 1: Core Pattern Engine complete (sphere, cylinder, cone compilers functional, 93% coverage, sub-millisecond generation)



**Following Phase:**

- Phase 3: Advanced visualization features (animations, Kid Mode, advanced tooltips)



**Critical Path:**

Yes. Visualization foundation blocks all downstream UI features. Frontend app shell is required for Phase 3-4 feature development.



---



## Goals & Deliverables



### Primary Goals



1. **Backend Visualization Engine**

   - Convert PatternDSL to frame-by-frame render primitives

   - Compute node positions (2D circular layout)

   - Identify highlights (increases, decreases)

   - API endpoint: `POST /api/v1/patterns/visualize`



2. **Frontend App Shell**

   - RN/Expo navigation stack operational

   - Zustand state management configured

   - Screen structure: Home, Generate, Visualize, Settings

   - HTTP client with error handling



3. **SVG Rendering Engine**

   - Render PatternDSL rounds as interactive SVG

   - Per-round visualization with node/edge graph

   - Color-coded stitches (green=inc, red=dec, gray=normal)

   - Smooth 60 FPS rendering on mid-range devices



4. **Navigation Controls**

   - Round scrubber (horizontal slider)

   - Previous/Next buttons (48×48 dp tap targets)

   - Round jump input (keyboard accessible)

   - Current round indicator



5. **Basic Interactivity**

   - Tap stitch → show tooltip (stitch type, name)

   - Legend overlay (color key)

   - Basic accessibility labels (WCAG AA)



6. **Performance**

   - Frame compilation: < 100ms

   - SVG render: 60 FPS on iPhone 11+, Pixel 4+

   - Pattern load: < 500ms end-to-end



### Key Deliverables



**Backend:**

- [ ] `app/services/visualization_service.py` - DSL → frames converter

- [ ] `app/models/visualization.py` - RenderPrimitive, VisualizationFrame models

- [ ] `app/api/routes/visualization.py` - POST /visualize endpoint

- [ ] `tests/unit/test_visualization_service.py` - Unit tests

- [ ] `tests/integration/test_visualization_api.py` - API contract tests



**Frontend:**

- [ ] `src/navigation/RootNavigator.tsx` - Navigation stack + tabs

- [ ] `src/screens/VisualizationScreen.tsx` - Main visualization UI

- [ ] `src/components/visualization/SVGRenderer.tsx` - SVG rendering engine

- [ ] `src/components/visualization/RoundScrubber.tsx` - Navigation controls

- [ ] `src/components/visualization/StitchTooltip.tsx` - Tooltip component

- [ ] `src/components/visualization/Legend.tsx` - Color key overlay

- [ ] `src/context/visualizationStore.ts` - Zustand store

- [ ] `src/services/apiClient.ts` - HTTP client

- [ ] `__tests__/components/SVGRenderer.test.tsx` - Component tests



### Success Metrics



| Metric | Target | Measurement |

|--------|--------|-------------|

| Backend frame compilation | < 100ms | pytest-benchmark |

| Frontend SVG render FPS | 60 FPS | React DevTools Profiler |

| Pattern load (E2E) | < 500ms | Manual testing |

| Touch target size | ≥ 48×48 dp | Design review |

| Accessibility score | WCAG AA | axe-core audit |

| Test coverage (BE) | > 80% | pytest-cov |

| Test coverage (FE) | > 60% | Jest coverage |



---



## Epic Breakdown



### EPIC B: Visualization (Backend + Frontend)



**Owner:** Backend Lead + Frontend Lead

**Duration:** Weeks 5-7 (Sprints 3-4)

**Total Effort:** 90 story points

**Priority:** P0 (Critical Path)



**Epic Overview:**

Implement the visualization pipeline from pattern DSL to interactive SVG rendering. Backend converts DSL to frame-by-frame render primitives; frontend renders these as interactive diagrams with navigation controls.



**Epic Goals:**

- Every PatternDSL round compiles to VisualizationFrame

- SVG renders smoothly at 60 FPS on mid-range devices

- Navigation controls are intuitive and accessible

- Stitch highlighting visually clear (colorblind-friendly)



#### Stories



| ID | Title | Effort | Priority | Dependencies | Owner |

|----|-------|--------|----------|--------------|-------|

| **B1** | DSL → RenderPrimitive converter (BE) | 13 pt | P0 | Phase 1 | BE Lead |

| **B2** | Visualization API endpoint (BE) | 8 pt | P0 | B1 | BE Eng |

| **B3** | SVG rendering engine (FE) | 13 pt | P0 | B2, D1 | FE Lead |

| **B4** | Round scrubber component (FE) | 8 pt | P0 | B3 | FE Eng |

| **B5** | Stitch highlighting (FE) | 8 pt | P0 | B3 | FE Eng |

| **B6** | Tooltip component (FE) | 5 pt | P1 | B3 | FE Eng |

| **B7** | Legend overlay (FE) | 3 pt | P1 | B5 | FE Eng |

| **B8** | Accessibility labels (FE) | 8 pt | P0 | B3 | FE Lead + QA |



**Total:** 66 story points



---



### EPIC D: App Shell & Settings (Foundation)



**Owner:** Frontend Lead

**Duration:** Weeks 5-6 (Sprint 3)

**Total Effort:** 32 story points

**Priority:** P0 (Critical Path)



**Epic Overview:**

Establish the React Native/Expo application structure with navigation, global state management, and HTTP client configuration. This epic provides the foundation for all frontend feature development.



**Epic Goals:**

- RN/Expo app runs on iOS/Android simulators

- Navigation stack operational (tabs + modal screens)

- Zustand state management configured

- HTTP client with error handling

- Basic settings screen functional



#### Stories



| ID | Title | Effort | Priority | Dependencies | Owner |

|----|-------|--------|----------|--------------|-------|

| **D1** | RN/Expo navigation setup | 8 pt | P0 | Phase 1 | FE Lead |

| **D2** | Zustand store configuration | 5 pt | P0 | D1 | FE Lead |

| **D3** | HTTP client & error handling | 8 pt | P0 | D1 | FE Eng |

| **D4** | Settings screen (foundation) | 5 pt | P1 | D1, D2 | FE Eng |

| **D5** | Theme system (colors, fonts) | 3 pt | P1 | D1 | FE Eng |

| **D6** | Loading states & error UI | 3 pt | P1 | D3 | FE Eng |



**Total:** 32 story points



---



## Sprint Plans



### Sprint 3 (Weeks 5-6)



**Sprint Goal:** Backend visualization pipeline + Frontend app shell operational



**Total Capacity:** 60-70 story points

**Team Focus:**

- Backend: DSL → frames conversion + API endpoint

- Frontend: Navigation + HTTP client + basic screens



**Stories Planned:**



| Story | Title | Effort | Owner | Status |

|-------|-------|--------|-------|--------|

| B1 | DSL → RenderPrimitive converter | 13 pt | BE Lead | Planned |

| B2 | Visualization API endpoint | 8 pt | BE Eng | Planned |

| D1 | RN/Expo navigation setup | 8 pt | FE Lead | Planned |

| D2 | Zustand store configuration | 5 pt | FE Lead | Planned |

| D3 | HTTP client & error handling | 8 pt | FE Eng | Planned |

| D4 | Settings screen (foundation) | 5 pt | FE Eng | Planned |

| D5 | Theme system (colors, fonts) | 3 pt | FE Eng | Planned |

| D6 | Loading states & error UI | 3 pt | FE Eng | Planned |



**Total Committed:** 53 story points



**Daily Breakdown:**



**Week 5:**

- **Day 1-2:** B1 (BE Lead), D1 (FE Lead), D3 start (FE Eng)

- **Day 3-4:** B1 completion, B2 start (BE Eng), D2 (FE Lead), D3 completion

- **Day 5:** B2 completion, D4 start (FE Eng), D5 start (FE Eng)



**Week 6:**

- **Day 1-2:** D4 completion, D5 completion, D6 (FE Eng)

- **Day 3-4:** Integration testing, bug fixes

- **Day 5:** Sprint review prep, demo walkthrough



**Sprint Demo:**

- Backend: Live API call showing PatternDSL → VisualizationFrame conversion

- Frontend: Navigation between Home → Generate → Visualize screens

- Frontend: Settings screen with theme toggle

- Frontend: HTTP client calling backend /visualize endpoint



**Definition of Done (Sprint 3):**

- [ ] Backend visualization endpoint returns valid frames (tested)

- [ ] Frontend app runs on iOS simulator and Android emulator

- [ ] Navigation between screens functional

- [ ] HTTP client successfully calls backend API

- [ ] Unit tests pass (BE: 80%+, FE: 60%+)

- [ ] Code reviewed and merged to main



---



### Sprint 4 (Week 7)



**Sprint Goal:** Interactive SVG rendering with navigation controls



**Total Capacity:** 65-75 story points

**Team Focus:**

- Frontend: SVG rendering engine + controls

- Backend: API optimization and error handling

- QA: Accessibility baseline audit



**Stories Planned:**



| Story | Title | Effort | Owner | Status |

|-------|-------|--------|-------|--------|

| B3 | SVG rendering engine | 13 pt | FE Lead | Planned |

| B4 | Round scrubber component | 8 pt | FE Eng | Planned |

| B5 | Stitch highlighting | 8 pt | FE Eng | Planned |

| B6 | Tooltip component | 5 pt | FE Eng | Planned |

| B7 | Legend overlay | 3 pt | FE Eng | Planned |

| B8 | Accessibility labels | 8 pt | FE Lead + QA | Planned |



**Total Committed:** 45 story points



**Daily Breakdown:**



**Week 7:**

- **Day 1-2:** B3 start (FE Lead), B4 start (FE Eng), B5 start (FE Eng)

- **Day 3:** B3 core rendering complete, B4 basic scrubber working

- **Day 4:** B5 highlighting complete, B6 tooltip start, B7 legend start

- **Day 5:** B6 complete, B7 complete, B8 accessibility audit

- **Day 6-7 (weekend buffer):** B8 fixes, integration testing



**Sprint Demo:**

- Live demo: Generate sphere pattern → Visualize with SVG rendering

- Navigate rounds using scrubber (smooth transitions)

- Tap stitch → tooltip appears (stitch type, name)

- Show increase/decrease highlighting (green/red)

- Legend overlay explains color coding

- Screen reader demo (basic accessibility)



**Definition of Done (Sprint 4):**

- [ ] SVG renders all pattern rounds without errors

- [ ] Round scrubber navigates forward/backward smoothly

- [ ] Stitch highlighting visually clear (increases green, decreases red)

- [ ] Tooltips show on tap/hover

- [ ] Legend overlay functional

- [ ] Accessibility labels present on all interactive elements

- [ ] 60 FPS rendering verified on test devices

- [ ] Unit tests pass (FE: 60%+)

- [ ] Code reviewed and merged to main



---



## Technical Implementation



### Backend: DSL to Visualization Frames



**Algorithm: PatternDSL → VisualizationFrame[]**



```python

# app/models/visualization.py

from pydantic import BaseModel

from typing import List, Literal



class RenderNode(BaseModel):

    """Represents a single stitch in visualization."""

    id: str                          # Unique node ID (e.g., "r3s12")

    stitch_type: str                 # "sc", "inc", "dec"

    position: tuple[float, float]    # (x, y) coordinates

    highlight: Literal["normal", "increase", "decrease"]



class RenderEdge(BaseModel):

    """Connection between consecutive stitches."""

    source: str                      # Node ID

    target: str                      # Node ID



class VisualizationFrame(BaseModel):

    """Single round visualization frame."""

    round_number: int

    nodes: List[RenderNode]

    edges: List[RenderEdge]

    stitch_count: int

    highlights: List[str]            # Node IDs with special highlighting



class VisualizationResponse(BaseModel):

    """Complete visualization data."""

    frames: List[VisualizationFrame]

    total_rounds: int

    shape_type: str

```



**Conversion Algorithm:**



```python

# app/services/visualization_service.py

import math

from knit_wit_engine.dsl import PatternDSL, RoundDSL



class VisualizationService:

    def dsl_to_frames(self, pattern: PatternDSL) -> List[VisualizationFrame]:

        """Convert PatternDSL to visualization frames."""

        frames = []

        for round_dsl in pattern.rounds:

            frame = self._round_to_frame(round_dsl, pattern.meta.stitch)

            frames.append(frame)

        return frames



    def _round_to_frame(self, round_dsl: RoundDSL, stitch_type: str) -> VisualizationFrame:

        """Convert single round to visualization frame."""

        nodes = []

        edges = []

        highlights = []



        # Compute circular layout (evenly spaced around circle)

        radius = 100.0  # Base radius in arbitrary units

        stitch_count = round_dsl.stitches

        angle_step = (2 * math.pi) / stitch_count



        # Generate nodes

        stitch_idx = 0

        for op in round_dsl.ops:

            if op.op in ["sc", "inc", "dec"]:

                for _ in range(op.count):

                    angle = stitch_idx * angle_step

                    x = radius * math.cos(angle)

                    y = radius * math.sin(angle)



                    node = RenderNode(

                        id=f"r{round_dsl.r}s{stitch_idx}",

                        stitch_type=op.op,

                        position=(x, y),

                        highlight="increase" if op.op == "inc" else "decrease" if op.op == "dec" else "normal"

                    )

                    nodes.append(node)



                    if node.highlight != "normal":

                        highlights.append(node.id)



                    stitch_idx += 1



        # Generate edges (connect consecutive stitches)

        for i in range(len(nodes) - 1):

            edges.append(RenderEdge(source=nodes[i].id, target=nodes[i+1].id))



        # Close the circle (last → first)

        if nodes:

            edges.append(RenderEdge(source=nodes[-1].id, target=nodes[0].id))



        return VisualizationFrame(

            round_number=round_dsl.r,

            nodes=nodes,

            edges=edges,

            stitch_count=stitch_count,

            highlights=highlights

        )

```



**API Endpoint:**



```python

# app/api/routes/visualization.py

from fastapi import APIRouter, HTTPException

from app.models.visualization import VisualizationResponse

from app.services.visualization_service import VisualizationService

from knit_wit_engine.dsl import PatternDSL



router = APIRouter(prefix="/api/v1/visualization", tags=["visualization"])

visualization_service = VisualizationService()



@router.post("/frames", response_model=VisualizationResponse)

async def generate_frames(pattern: PatternDSL):

    """

    Convert PatternDSL to visualization frames.



    **Performance:** < 100ms for typical patterns (< 50 rounds)

    """

    try:

        frames = visualization_service.dsl_to_frames(pattern)

        return VisualizationResponse(

            frames=frames,

            total_rounds=len(frames),

            shape_type=pattern.object.type

        )

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Visualization error: {str(e)}")

```



**Unit Test Example:**



```python

# tests/unit/test_visualization_service.py

import pytest

from app.services.visualization_service import VisualizationService

from knit_wit_engine.dsl import PatternDSL, RoundDSL, OpDSL



def test_simple_round_conversion():

    """Test single round conversion to frame."""

    service = VisualizationService()



    round_dsl = RoundDSL(

        r=1,

        ops=[OpDSL(op="sc", count=6)],

        stitches=6

    )



    frame = service._round_to_frame(round_dsl, "sc")



    assert frame.round_number == 1

    assert frame.stitch_count == 6

    assert len(frame.nodes) == 6

    assert len(frame.edges) == 6  # 5 consecutive + 1 closing

    assert all(node.highlight == "normal" for node in frame.nodes)



def test_increase_highlighting():

    """Test increases are highlighted correctly."""

    service = VisualizationService()



    round_dsl = RoundDSL(

        r=2,

        ops=[OpDSL(op="inc", count=6)],

        stitches=12

    )



    frame = service._round_to_frame(round_dsl, "sc")



    # All nodes should be increases

    assert all(node.highlight == "increase" for node in frame.nodes)

    assert len(frame.highlights) == 12

```



---



### Frontend: SVG Rendering Engine



**Component Architecture:**



```typescript

// src/components/visualization/SVGRenderer.tsx

import React from 'react';

import { Svg, Circle, Line, G } from 'react-native-svg';

import { StyleSheet, View } from 'react-native';

import type { VisualizationFrame } from '../../types/visualization';



interface SVGRendererProps {

  frame: VisualizationFrame;

  width: number;

  height: number;

  onStitchTap: (nodeId: string) => void;

}



export const SVGRenderer: React.FC<SVGRendererProps> = ({

  frame,

  width,

  height,

  onStitchTap

}) => {

  const centerX = width / 2;

  const centerY = height / 2;

  const scale = Math.min(width, height) / 250; // Scale to fit viewport



  // Color mapping for stitch types

  const getStitchColor = (highlight: string): string => {

    switch (highlight) {

      case 'increase': return '#10B981'; // Green

      case 'decrease': return '#EF4444'; // Red

      default: return '#6B7280'; // Gray

    }

  };



  return (

    <View style={styles.container}>

      <Svg width={width} height={height}>

        <G transform={`translate(${centerX}, ${centerY}) scale(${scale})`}>

          {/* Render edges first (behind nodes) */}

          {frame.edges.map((edge, idx) => {

            const source = frame.nodes.find(n => n.id === edge.source);

            const target = frame.nodes.find(n => n.id === edge.target);

            if (!source || !target) return null;



            return (

              <Line

                key={`edge-${idx}`}

                x1={source.position[0]}

                y1={source.position[1]}

                x2={target.position[0]}

                y2={target.position[1]}

                stroke="#D1D5DB"

                strokeWidth={1.5}

              />

            );

          })}



          {/* Render nodes */}

          {frame.nodes.map((node) => (

            <Circle

              key={node.id}

              cx={node.position[0]}

              cy={node.position[1]}

              r={8}

              fill={getStitchColor(node.highlight)}

              stroke="#FFFFFF"

              strokeWidth={2}

              onPress={() => onStitchTap(node.id)}

            />

          ))}

        </G>

      </Svg>

    </View>

  );

};



const styles = StyleSheet.create({

  container: {

    flex: 1,

    alignItems: 'center',

    justifyContent: 'center',

  },

});

```



**Zustand Store:**



```typescript

// src/context/visualizationStore.ts

import create from 'zustand';

import type { VisualizationFrame } from '../types/visualization';



interface VisualizationState {

  frames: VisualizationFrame[];

  currentRound: number;

  totalRounds: number;

  loading: boolean;

  error: string | null;



  setFrames: (frames: VisualizationFrame[]) => void;

  setCurrentRound: (round: number) => void;

  nextRound: () => void;

  prevRound: () => void;

  jumpToRound: (round: number) => void;

  setLoading: (loading: boolean) => void;

  setError: (error: string | null) => void;

}



export const useVisualizationStore = create<VisualizationState>((set, get) => ({

  frames: [],

  currentRound: 1,

  totalRounds: 0,

  loading: false,

  error: null,



  setFrames: (frames) => set({

    frames,

    totalRounds: frames.length,

    currentRound: frames.length > 0 ? 1 : 0

  }),



  setCurrentRound: (round) => {

    const { totalRounds } = get();

    if (round >= 1 && round <= totalRounds) {

      set({ currentRound: round });

    }

  },



  nextRound: () => {

    const { currentRound, totalRounds } = get();

    if (currentRound < totalRounds) {

      set({ currentRound: currentRound + 1 });

    }

  },



  prevRound: () => {

    const { currentRound } = get();

    if (currentRound > 1) {

      set({ currentRound: currentRound - 1 });

    }

  },



  jumpToRound: (round) => {

    const { totalRounds } = get();

    const boundedRound = Math.max(1, Math.min(round, totalRounds));

    set({ currentRound: boundedRound });

  },



  setLoading: (loading) => set({ loading }),

  setError: (error) => set({ error }),

}));

```



**Round Scrubber Component:**



```typescript

// src/components/visualization/RoundScrubber.tsx

import React from 'react';

import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

import Slider from '@react-native-community/slider';

import { useVisualizationStore } from '../../context/visualizationStore';



export const RoundScrubber: React.FC = () => {

  const { currentRound, totalRounds, prevRound, nextRound, jumpToRound } =

    useVisualizationStore();



  return (

    <View style={styles.container}>

      {/* Previous button */}

      <TouchableOpacity

        onPress={prevRound}

        disabled={currentRound === 1}

        style={[styles.button, currentRound === 1 && styles.buttonDisabled]}

        accessibilityLabel="Previous round"

        accessibilityRole="button"

      >

        <Text style={styles.buttonText}>←</Text>

      </TouchableOpacity>



      {/* Slider */}

      <View style={styles.sliderContainer}>

        <Slider

          style={styles.slider}

          minimumValue={1}

          maximumValue={totalRounds}

          step={1}

          value={currentRound}

          onValueChange={jumpToRound}

          minimumTrackTintColor="#3B82F6"

          maximumTrackTintColor="#D1D5DB"

          thumbTintColor="#3B82F6"

          accessibilityLabel={`Round ${currentRound} of ${totalRounds}`}

        />

        <Text style={styles.label}>

          Round {currentRound} of {totalRounds}

        </Text>

      </View>



      {/* Next button */}

      <TouchableOpacity

        onPress={nextRound}

        disabled={currentRound === totalRounds}

        style={[styles.button, currentRound === totalRounds && styles.buttonDisabled]}

        accessibilityLabel="Next round"

        accessibilityRole="button"

      >

        <Text style={styles.buttonText}>→</Text>

      </TouchableOpacity>

    </View>

  );

};



const styles = StyleSheet.create({

  container: {

    flexDirection: 'row',

    alignItems: 'center',

    paddingHorizontal: 16,

    paddingVertical: 12,

    backgroundColor: '#FFFFFF',

    borderTopWidth: 1,

    borderTopColor: '#E5E7EB',

  },

  button: {

    width: 48,

    height: 48,

    borderRadius: 24,

    backgroundColor: '#3B82F6',

    alignItems: 'center',

    justifyContent: 'center',

  },

  buttonDisabled: {

    backgroundColor: '#D1D5DB',

  },

  buttonText: {

    color: '#FFFFFF',

    fontSize: 24,

    fontWeight: 'bold',

  },

  sliderContainer: {

    flex: 1,

    marginHorizontal: 16,

  },

  slider: {

    width: '100%',

    height: 40,

  },

  label: {

    textAlign: 'center',

    fontSize: 14,

    color: '#6B7280',

    marginTop: 4,

  },

});

```



**Tooltip Component:**



```typescript

// src/components/visualization/StitchTooltip.tsx

import React from 'react';

import { View, Text, StyleSheet, Modal, TouchableOpacity } from 'react-native';



interface StitchTooltipProps {

  visible: boolean;

  nodeId: string | null;

  stitchType: string;

  stitchName: string;

  onClose: () => void;

}



export const StitchTooltip: React.FC<StitchTooltipProps> = ({

  visible,

  nodeId,

  stitchType,

  stitchName,

  onClose

}) => {

  if (!visible || !nodeId) return null;



  return (

    <Modal

      visible={visible}

      transparent

      animationType="fade"

      onRequestClose={onClose}

    >

      <TouchableOpacity

        style={styles.overlay}

        activeOpacity={1}

        onPress={onClose}

      >

        <View style={styles.tooltip}>

          <Text style={styles.stitchType}>{stitchType.toUpperCase()}</Text>

          <Text style={styles.stitchName}>{stitchName}</Text>

          <Text style={styles.nodeId}>{nodeId}</Text>

        </View>

      </TouchableOpacity>

    </Modal>

  );

};



const styles = StyleSheet.create({

  overlay: {

    flex: 1,

    backgroundColor: 'rgba(0, 0, 0, 0.4)',

    justifyContent: 'center',

    alignItems: 'center',

  },

  tooltip: {

    backgroundColor: '#FFFFFF',

    borderRadius: 8,

    padding: 16,

    minWidth: 200,

    shadowColor: '#000',

    shadowOffset: { width: 0, height: 2 },

    shadowOpacity: 0.25,

    shadowRadius: 4,

    elevation: 5,

  },

  stitchType: {

    fontSize: 18,

    fontWeight: 'bold',

    color: '#111827',

    marginBottom: 4,

  },

  stitchName: {

    fontSize: 16,

    color: '#6B7280',

    marginBottom: 8,

  },

  nodeId: {

    fontSize: 12,

    color: '#9CA3AF',

  },

});

```



---



### Navigation Controls



**Screen Integration:**



```typescript

// src/screens/VisualizationScreen.tsx

import React, { useEffect, useState } from 'react';

import { View, StyleSheet, ActivityIndicator } from 'react-native';

import { SVGRenderer } from '../components/visualization/SVGRenderer';

import { RoundScrubber } from '../components/visualization/RoundScrubber';

import { StitchTooltip } from '../components/visualization/StitchTooltip';

import { Legend } from '../components/visualization/Legend';

import { useVisualizationStore } from '../context/visualizationStore';

import { apiClient } from '../services/apiClient';

import type { PatternDSL } from '../types/dsl';



export const VisualizationScreen: React.FC = ({ route }) => {

  const { pattern } = route.params as { pattern: PatternDSL };

  const { frames, currentRound, loading, setFrames, setLoading, setError } =

    useVisualizationStore();



  const [tooltipVisible, setTooltipVisible] = useState(false);

  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);



  useEffect(() => {

    loadVisualization();

  }, [pattern]);



  const loadVisualization = async () => {

    setLoading(true);

    try {

      const response = await apiClient.post('/visualization/frames', pattern);

      setFrames(response.data.frames);

    } catch (error) {

      setError('Failed to load visualization');

    } finally {

      setLoading(false);

    }

  };



  const handleStitchTap = (nodeId: string) => {

    setSelectedNodeId(nodeId);

    setTooltipVisible(true);

  };



  if (loading) {

    return (

      <View style={styles.loadingContainer}>

        <ActivityIndicator size="large" color="#3B82F6" />

      </View>

    );

  }



  const currentFrame = frames[currentRound - 1];



  return (

    <View style={styles.container}>

      <View style={styles.renderContainer}>

        {currentFrame && (

          <SVGRenderer

            frame={currentFrame}

            width={400}

            height={400}

            onStitchTap={handleStitchTap}

          />

        )}

        <Legend />

      </View>



      <RoundScrubber />



      <StitchTooltip

        visible={tooltipVisible}

        nodeId={selectedNodeId}

        stitchType={currentFrame?.nodes.find(n => n.id === selectedNodeId)?.stitch_type || ''}

        stitchName="Single Crochet"

        onClose={() => setTooltipVisible(false)}

      />

    </View>

  );

};



const styles = StyleSheet.create({

  container: {

    flex: 1,

    backgroundColor: '#F9FAFB',

  },

  loadingContainer: {

    flex: 1,

    justifyContent: 'center',

    alignItems: 'center',

  },

  renderContainer: {

    flex: 1,

    position: 'relative',

  },

});

```



---



## Success Criteria



### Phase Exit Criteria



**Backend:**

- [ ] DSL → frames conversion functional for all Phase 1 shapes

- [ ] Visualization API endpoint deployed and tested

- [ ] Frame compilation < 100ms (pytest-benchmark verified)

- [ ] Unit test coverage > 80%

- [ ] Integration tests pass (API contract validation)



**Frontend:**

- [ ] RN/Expo app runs on iOS simulator and Android emulator

- [ ] Navigation stack functional (Home → Generate → Visualize → Settings)

- [ ] SVG rendering displays all rounds without visual artifacts

- [ ] Round scrubber navigates smoothly (60 FPS verified)

- [ ] Stitch highlighting visually clear (green/red/gray)

- [ ] Tooltips appear on tap

- [ ] Legend overlay explains color coding

- [ ] Touch targets ≥ 48×48 dp (manual verification)

- [ ] Component test coverage > 60%



**Accessibility:**

- [ ] All interactive elements have accessibility labels

- [ ] Screen reader announces round changes

- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)

- [ ] Focus indicators visible on external keyboard navigation

- [ ] axe-core audit passes with 0 critical issues



**Performance:**

- [ ] End-to-end pattern load < 500ms (manual testing)

- [ ] SVG rendering 60 FPS on iPhone 11+ (React DevTools Profiler)

- [ ] SVG rendering 60 FPS on Pixel 4+ (React DevTools Profiler)

- [ ] No memory leaks during round navigation (500+ round changes)



**Integration:**

- [ ] Backend → Frontend API integration functional

- [ ] Error handling graceful (network failures, invalid patterns)

- [ ] Loading states displayed during async operations



---



## Dependencies & Risks



### Dependencies from Phase 1



**Met Dependencies:**

- ✅ PatternDSL schema finalized (Phase 1)

- ✅ Sphere, cylinder, cone compilers functional (Phase 1)

- ✅ Pattern engine performance validated (sub-millisecond, Phase 1)

- ✅ Test patterns available (sphere 10cm, cylinder 8×12cm, cone 6→2cm)



**Required for Phase 2:**

- PatternDSL JSON serialization (available via `.to_json()`)

- Round-level DSL access (`pattern.rounds[]`)

- Stitch operation types (`sc`, `inc`, `dec`)



### External Dependencies



**Backend:**

- FastAPI 0.104+ (already installed in Phase 0)

- Pydantic v2 (already used in Phase 1)

- Python 3.11+ (already configured)



**Frontend:**

- react-native-svg (needs installation)

- @react-navigation/native (needs installation)

- @react-navigation/stack (needs installation)

- zustand (needs installation)

- @react-native-community/slider (needs installation)



**Installation Required:**

```bash

# Frontend dependencies

pnpm --filter mobile add react-native-svg

pnpm --filter mobile add @react-navigation/native @react-navigation/stack

pnpm --filter mobile add zustand

pnpm --filter mobile add @react-native-community/slider

```



### Risks & Mitigation



| Risk | Probability | Impact | Mitigation |

|------|-------------|--------|------------|

| **SVG performance on low-end devices** | Medium | High | Progressive rendering, lazy load rounds, optimize node count |

| **react-native-svg compatibility issues** | Low | Medium | Use stable version (14.x), test early on both platforms |

| **Circular layout algorithm complexity** | Low | Medium | Reuse standard polar coordinate conversion, well-documented |

| **Accessibility label completeness** | Medium | High | Use axe-core automated audit + manual testing with VoiceOver/TalkBack |

| **Backend frame compilation memory usage** | Low | Medium | Stream frames for large patterns (100+ rounds), pagination |

| **Frontend state management complexity** | Low | Low | Zustand keeps it simple, avoid Redux overhead |



### Blockers



**Current Blockers:**

- None (Phase 1 complete, all dependencies met)



**Potential Blockers:**

- Expo SDK compatibility issues (mitigation: use SDK 51+)

- iOS simulator unavailable (mitigation: use Android emulator or web)

- Backend deployment delays (mitigation: test locally with docker-compose)



---



## Testing Requirements



### Backend Testing



**Unit Tests:**

- `test_visualization_service.py` - DSL → frames conversion logic

  - Test circular layout (node positions correct)

  - Test highlight identification (inc/dec marked)

  - Test edge generation (consecutive + closing edge)

  - Test edge cases (empty rounds, single stitch, 100+ stitches)

- `test_visualization_models.py` - Pydantic model validation

  - Test RenderNode, RenderEdge, VisualizationFrame schemas

  - Test invalid inputs rejected



**Integration Tests:**

- `test_visualization_api.py` - API endpoint contracts

  - POST /visualization/frames with valid PatternDSL → 200 OK

  - POST /visualization/frames with invalid DSL → 422 Validation Error

  - Verify response schema matches VisualizationResponse

  - Test performance (< 100ms for 50-round pattern)



**Coverage Target:** > 80%



### Frontend Testing



**Component Tests:**

- `SVGRenderer.test.tsx` - Rendering logic

  - Renders nodes and edges correctly

  - Applies correct colors (green/red/gray)

  - Handles tap events

  - Scales correctly to viewport

- `RoundScrubber.test.tsx` - Navigation controls

  - Prev/Next buttons update round

  - Slider jumps to correct round

  - Buttons disabled at boundaries

- `StitchTooltip.test.tsx` - Tooltip display

  - Shows/hides on tap

  - Displays correct stitch information

- `Legend.test.tsx` - Legend overlay

  - Displays all stitch types

  - Color mapping correct



**Integration Tests:**

- `VisualizationScreen.test.tsx` - Full screen integration

  - Loads frames on mount

  - Updates SVG when round changes

  - Shows loading state during API call

  - Displays error state on API failure



**Coverage Target:** > 60%



### Accessibility Testing



**Automated:**

- axe-core audit on VisualizationScreen

  - 0 critical issues

  - 0 serious issues

  - Document minor/moderate issues for Phase 3



**Manual:**

- VoiceOver (iOS) announces round changes

- TalkBack (Android) announces stitch taps

- External keyboard navigation functional

- Color contrast verified with contrast checker



---



## Next Phase Preview



### Phase 3: Advanced Visualization (Weeks 8-10)



**Primary Goals:**

- Text parsing (limited grammar)

- Multi-format export (PDF, SVG, JSON)

- Kid Mode toggle and simplified UI

- Advanced tooltips (animations, "what is an increase?")

- Handedness mirroring

- US ↔ UK terminology toggle (live update)



**Epics:**

- EPIC B: Visualization (advanced features)

- EPIC C: Parsing & I/O

- EPIC E: Kid Mode & Accessibility (full implementation)



**Dependencies from Phase 2:**

- SVG rendering engine (will extend with animations)

- Navigation controls (will add round jump input)

- Zustand stores (will add settings persistence)

- Accessibility baseline (will extend to full WCAG AA)



**Estimated Effort:** 80-90 story points



---



## Phase 2 Summary



**Total Story Points:** 98 points

**Duration:** 3 weeks (Sprints 3-4)

**Team:** 2 BE, 2 FE, 1 QA (5 people)

**Velocity:** 49 points/week (sustainable pace)



**Critical Path Stories:**

- B1: DSL → RenderPrimitive converter (blocks B2, B3)

- B2: Visualization API endpoint (blocks B3)

- D1: Navigation setup (blocks all FE stories)

- B3: SVG rendering engine (blocks B4, B5, B6, B7, B8)



**Parallel Workstreams:**

- Backend: B1 → B2 (sequential, 2 weeks)

- Frontend App Shell: D1 → D2, D3, D4, D5, D6 (parallel, Week 5-6)

- Frontend Visualization: B3 → B4, B5, B6, B7, B8 (mixed, Week 7)



**Risk Level:** Low-Medium

- Known technologies (react-native-svg, FastAPI)

- Clear acceptance criteria from PRD

- Phase 1 provides solid foundation



**Confidence:** High

- Algorithm complexity contained (circular layout is straightforward)

- Pattern engine proven performant (sub-millisecond)

- Team experienced with React Native and Python



---



**Document Status:** FINAL

**Next Review:** Phase 2 kickoff (Sprint 3 planning)

**Owner:** Development Team

---

**END OF PHASE 2 PLAN**