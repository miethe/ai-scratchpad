# Knit-Wit Web App

A native web application for generating and visualizing parametric crochet patterns. This is the web counterpart to the React Native mobile app, providing full feature parity with an optimized web experience.

## Features

### Core Capabilities
- **Parametric Pattern Generation**: Generate custom crochet patterns for spheres, cylinders, and cones based on dimensions and gauge
- **Interactive Visualization**: Step-by-step SVG visualization with round navigation
- **Pattern Parsing**: Validate and visualize existing crochet patterns
- **Multi-Format Export**: Export patterns as PDF, SVG, or JSON
- **US/UK Terminology**: Toggle between US and UK crochet terminology
- **Kid Mode**: Simplified interface with larger buttons and beginner-friendly language

### Accessibility (WCAG AA Compliant)
- High contrast mode
- Reduced motion support
- Adjustable font sizes (small, medium, large)
- Keyboard navigation support
- Screen reader compatible
- Focus indicators on all interactive elements

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- FastAPI backend running (see `apps/api/`)

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Project Structure

```
apps/web/
├── src/
│   ├── screens/          # Page components
│   ├── stores/           # Zustand state management
│   ├── services/         # API client
│   ├── types/            # TypeScript types
│   ├── theme/            # Design system
│   └── App.tsx           # Root component with routing
└── README.md
```

## Feature Parity with Mobile App

This web app provides 100% feature parity with the React Native mobile app:

✓ Home Screen
✓ Pattern Generation  
✓ Interactive Visualization
✓ Pattern Parsing
✓ Export (PDF/SVG/JSON)
✓ Settings & Preferences
✓ Kid Mode
✓ US/UK Terminology
✓ WCAG AA Accessibility
✓ State Persistence

## Tech Stack

- React 18 + TypeScript
- Vite
- React Router v6
- Zustand
- Native Fetch API

## License

See main project LICENSE file.
