import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { useSettingsStore } from './stores/useSettingsStore';
import HomeScreen from './screens/HomeScreen';
import GenerateScreen from './screens/GenerateScreen';
import VisualizationScreen from './screens/VisualizationScreen';
import ParseScreen from './screens/ParseScreen';
import ExportScreen from './screens/ExportScreen';
import SettingsScreen from './screens/SettingsScreen';
import { colors, kidModeColors, spacing, borderRadius, typography } from './theme';

function Navigation() {
  const location = useLocation();
  const { kidMode } = useSettingsStore();

  const theme = kidMode ? kidModeColors : colors;

  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/generate', label: kidMode ? 'Make' : 'Generate' },
    { path: '/parse', label: kidMode ? 'Check' : 'Parse' },
    { path: '/settings', label: 'Settings' },
  ];

  return (
    <nav style={{
      backgroundColor: colors.surface,
      borderBottom: `1px solid ${colors.border}`,
      padding: spacing.md,
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: spacing.md,
      }}>
        <Link
          to="/"
          style={{
            fontSize: typography.fontSize.xl,
            fontWeight: typography.fontWeight.bold,
            color: theme.primary,
            textDecoration: 'none',
          }}
        >
          Knit-Wit {kidMode && '🧶'}
        </Link>

        <div style={{
          display: 'flex',
          gap: spacing.sm,
          flexWrap: 'wrap',
        }}>
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              style={{
                padding: `${spacing.sm} ${spacing.md}`,
                backgroundColor: location.pathname === item.path ? theme.primary : 'transparent',
                color: location.pathname === item.path ? colors.textInverse : colors.textPrimary,
                textDecoration: 'none',
                borderRadius: borderRadius.md,
                fontSize: typography.fontSize.base,
                fontWeight: typography.fontWeight.medium,
                transition: 'background-color 150ms ease-in-out',
              }}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div style={{
        minHeight: '100vh',
        backgroundColor: colors.background,
      }}>
        <Navigation />
        <Routes>
          <Route path="/" element={<HomeScreen />} />
          <Route path="/generate" element={<GenerateScreen />} />
          <Route path="/visualize" element={<VisualizationScreen />} />
          <Route path="/parse" element={<ParseScreen />} />
          <Route path="/export" element={<ExportScreen />} />
          <Route path="/settings" element={<SettingsScreen />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
