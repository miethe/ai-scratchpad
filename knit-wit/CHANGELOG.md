# Changelog

All notable changes to Knit-Wit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-30

### MVP Release

Complete initial launch of Knit-Wit with core pattern generation and visualization features.

See [MVP Release Notes](./docs/releases/mvp-v1.0.md) for comprehensive feature list, known limitations, and browser support.

### Added

#### Core Features
- **Pattern Generation**: Parametric crochet pattern generation for geometric shapes
  - Sphere shape support (diameter parameter)
  - Cylinder shape support (height and diameter parameters)
  - Cone/Tapered shape support (height and base diameter parameters)
  - Stitch type: Single crochet (US and UK terminology)
  - Customizable gauge (stitches per 10cm, rows per 10cm)
  - Unit selection (cm or inches)
  - Terminology selection (US or UK stitch names)
  - Yardage estimation

#### Visualization Engine
- **Interactive Round-by-Round Visualization**: SVG-based step-by-step pattern visualization
  - Play/pause animation
  - Previous/next round navigation
  - Round jump/selection
  - Zoom in/out controls
  - Responsive design for all screen sizes
  - Touch and keyboard navigation

#### Export Capabilities
- **PDF Export**: Print-ready pattern documentation
  - Multiple paper sizes (A4, Letter, Legal)
  - Includes diagrams and full instructions
  - Properly formatted stitch notation

- **SVG Export**: Vector format for high-quality output
  - Infinitely scalable diagrams
  - Editable in design software
  - Suitable for print shops

- **PNG Export**: Raster image for quick sharing
  - Standard and high-quality resolutions
  - Perfect for social media and email

- **JSON Export**: Pattern DSL v0.1 format
  - Complete pattern data export
  - Machine-readable format
  - Suitable for archival and programmatic use

#### Accessibility Features
- **WCAG 2.1 Level AA Compliance**
  - Complete screen reader support (NVDA, JAWS, VoiceOver, TalkBack)
  - Full keyboard navigation support
  - Accessible form labels and instructions
  - Proper focus management and visible focus indicators
  - Minimum 44x44pt touch targets on mobile

- **High Contrast Mode**: Enhanced color contrast for low-vision users
  - 7:1 text contrast ratio (exceeds WCAG AAA)
  - Higher contrast button states
  - More prominent borders and dividers

- **Dyslexia-Friendly Font**: OpenDyslexic font support
  - Weighted letter bottoms to prevent flipping
  - Distinct letter shapes for improved differentiation
  - Optimized spacing and sizing

- **Zoom Support**: Responsive design scales properly at all zoom levels
  - Works with browser zoom (up to 300%)
  - Works with pinch-to-zoom on mobile devices
  - Touch targets remain appropriately sized

#### User Interface
- **Home Screen**: Welcome and feature overview
- **Generate Screen**: Pattern generation form with intuitive controls
- **Visualization Screen**: Interactive pattern display and controls
- **Export Screen**: Multiple export format options
- **Settings Screen**: User preferences and accessibility options
- **Bottom Tab Navigation**: Easy access to all main screens

#### Kid Mode
- **Simplified UI**: Larger buttons and clearer interface
- **Beginner Terminology**: "Basic Stitch" instead of "Single Crochet", etc.
- **Animated Tutorials**: Video tutorials for basic techniques
- **Encouraging Language**: Friendly, supportive copy
- **Accessible Defaults**: Optimized for young users and beginners

#### Settings & Customization
- Terminology preference (US vs UK stitch names)
- Dark mode theme option (visual design, functionality TBA)
- Text size options (small, regular, large)
- High contrast mode toggle
- Dyslexia font toggle
- Kid Mode toggle
- Pattern history clearing
- App version and build information

#### Technical Infrastructure
- **Frontend**: React Native/Expo with TypeScript
  - Zustand state management
  - React Navigation for routing
  - react-native-svg for visualization
  - Axios for API communication
  - Jest + React Native Testing Library for tests

- **Backend**: FastAPI with Python 3.11+
  - Pydantic v2 for validation
  - Uvicorn ASGI server
  - Pattern DSL v0.1 support
  - Comprehensive error handling
  - Structured logging with request correlation IDs
  - Sentry integration for error tracking

- **Pattern Engine**: Standalone Python library
  - Parametric algorithm implementations
  - Support for sphere, cylinder, cone shapes
  - Gauge-based stitch calculation
  - Even distribution of increases/decreases (Bresenham algorithm)
  - Yardage estimation
  - DSL serialization/deserialization

- **DevOps & Deployment**
  - Docker containerization
  - Docker Compose for local development
  - GitHub Actions CI/CD pipeline
  - Health checks and readiness probes
  - Environment-based configuration

### Performance Characteristics

- Pattern generation: <200ms (p95)
- Visualization rendering: <100ms per frame
- API response time: <500ms (p95)
- Frontend rendering: 60 FPS
- Mobile-first responsive design
- Optimized bundle size for fast loading

### Browser & Device Support

**Desktop Browsers**:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Mobile Devices**:
- iOS 14+ (iPhone, iPad)
- Android 10+
- Tested on screen sizes from 4" phones to 10" tablets

**Screen Readers**:
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (iOS/macOS)
- TalkBack (Android)

### Known Limitations

#### Stitch Support
- Only single crochet currently supported
- Double crochet, half double crochet, and other stitches coming in v1.1

#### Shape Support
- Sphere, cylinder, and cone only
- Cubes, pyramids, and toruses planned for future versions
- Custom shape definitions planned for v2.0

#### Pattern Features
- Spiral rounds only (joined rounds coming in v1.1)
- No colorwork or stripes (planned for v2.0)
- No complex stitch combinations or pattern stitches

#### User Features
- No user accounts or authentication in MVP
- Patterns not persisted (generate fresh each session)
- No pattern history or favorites (session-only history)
- No community features or pattern sharing

#### Export Features
- PDF export is server-side generated (may be slow for complex patterns)
- SVG export not yet optimized for very large patterns
- No async export queue (large patterns may timeout)

#### Performance
- Pattern generation timeout at 30 seconds
- Maximum stitch count limit: ~2000 per round
- No caching/persistence of patterns between sessions

### Testing Coverage

- Backend: 60%+ coverage on API services
- Pattern Engine: 80%+ coverage on algorithms
- Frontend: 60%+ coverage on components
- Integration tests covering critical user flows
- Accessibility testing with axe-core and manual WCAG AA audits

### Documentation

- Complete user guide with getting started and feature overviews
- Comprehensive FAQ with common questions and troubleshooting
- API contract documentation with request/response examples
- Architecture and design documentation
- Accessibility compliance documentation
- Developer setup guides for backend and frontend

### Bug Fixes

#### Initial Release
- No previous bugs (initial release)

---

## [Unreleased]

### Planned for v1.1
- [ ] Support for double crochet and half double crochet stitches
- [ ] Joined rounds in addition to spiral rounds
- [ ] User authentication (JWT/OAuth 2.0)
- [ ] Pattern persistence and history
- [ ] Favorites/bookmarking
- [ ] Search and filter saved patterns
- [ ] Rate limiting and usage metrics

### Planned for v2.0
- [ ] Colorwork and striped patterns
- [ ] Custom shape definitions
- [ ] Community pattern sharing
- [ ] Yarn recommendation engine
- [ ] AR preview of finished objects
- [ ] Advanced export: Email patterns, share links
- [ ] Subscription features for advanced shapes

### Future Enhancements
- [ ] Cubes and pyramids
- [ ] Toruses (donut shapes)
- [ ] Treble crochet and other stitches
- [ ] Standing start and other advanced techniques
- [ ] Audio descriptions for visualization (additional accessibility)
- [ ] Internationalization (additional languages)
- [ ] Offline mode for generated patterns
- [ ] Mobile app (native iOS/Android)
- [ ] Pattern templates and variations
- [ ] Collaborative pattern design
- [ ] Integration with yarn database APIs

---

## Technical Details

### Version Scheme

Knit-Wit follows Semantic Versioning:
- **MAJOR** (1.0.0): Breaking changes, significant feature additions
- **MINOR** (1.1.0): New features, backward compatible
- **PATCH** (1.0.1): Bug fixes, backward compatible

### Release Process

1. Development occurs on feature branches
2. Pull request code review
3. Automated testing and CI/CD validation
4. Merge to main branch
5. Version bump and changelog update
6. Release tag created
7. Automated deployment to production

### Support & Maintenance

- **MVP Phase (v1.0.x)**: Bug fixes and stability improvements only
- **Active Development (v1.1+)**: Regular feature releases
- **LTS (planned)**: Long-term support version TBA

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Requesting features
- Contributing code
- Setting up development environment

---

## Credits

Knit-Wit was developed as an open-source project to make crochet pattern generation accessible to everyone.

**Special thanks to:**
- The crochet community for feedback and inspiration
- Open-source communities for amazing libraries
- Accessibility testing volunteers

---

**Latest Version**: 1.0.0
**Release Date**: November 30, 2024
**Status**: MVP - Production Ready
