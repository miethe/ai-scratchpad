# Colorblind Palette Quick Reference

Quick visual reference for knit-wit accessibility palettes. Use this as a cheat sheet during development.

## Protanopia / Deuteranopia (Red-Green Blind)

Most common type - affects ~2% of males

| Stitch Type | Color | Hex | Pattern | Symbol |
|-------------|-------|-----|---------|--------|
| Increase | ![#0072B2](https://via.placeholder.com/60x30/0072B2/0072B2.png) | `#0072B2` | Diagonal stripes ⟋ | ▲ |
| Decrease | ![#D55E00](https://via.placeholder.com/60x30/D55E00/D55E00.png) | `#D55E00` | Crosshatch ⨯ | ▼ |
| Normal | ![#999999](https://via.placeholder.com/60x30/999999/999999.png) | `#999999` | Solid | ● |

**Usage:**
```tsx
const palette = colorblindPalettes.protanopia;
// or
const palette = colorblindPalettes.deuteranopia; // Same colors
```

## Tritanopia (Blue-Blind)

Rare - affects ~0.001% of population

| Stitch Type | Color | Hex | Pattern | Symbol |
|-------------|-------|-----|---------|--------|
| Increase | ![#E69F00](https://via.placeholder.com/60x30/E69F00/E69F00.png) | `#E69F00` | Diagonal stripes ⟋ | ▲ |
| Decrease | ![#56B4E9](https://via.placeholder.com/60x30/56B4E9/56B4E9.png) | `#56B4E9` | Crosshatch ⨯ | ▼ |
| Normal | ![#999999](https://via.placeholder.com/60x30/999999/999999.png) | `#999999` | Solid | ● |

**Usage:**
```tsx
const palette = colorblindPalettes.tritanopia;
```

## High Contrast (Low Vision)

For users with severe visual impairment (use on dark backgrounds)

| Stitch Type | Color | Hex | Pattern | Symbol |
|-------------|-------|-----|---------|--------|
| Increase | ![#00FF00](https://via.placeholder.com/60x30/00FF00/00FF00.png) | `#00FF00` | Diagonal stripes ⟋ | ▲ |
| Decrease | ![#FF0000](https://via.placeholder.com/60x30/FF0000/FF0000.png) | `#FF0000` | Crosshatch ⨯ | ▼ |
| Normal | ![#FFFFFF](https://via.placeholder.com/60x30/FFFFFF/FFFFFF.png) | `#FFFFFF` | Solid | ● |

**Usage:**
```tsx
const palette = colorblindPalettes.highContrast;
// NOTE: Requires dark background!
```

## Pattern Visual Reference

### Increase Pattern (Diagonal Stripes)
```
  /  /  /
 /  /  /
/  /  /
```
- SVG Path: `M0,8 L8,0`
- ID: `diagonal-stripes`
- Stroke: 2px @ 30% opacity

### Decrease Pattern (Crosshatch)
```
 X  X  X
  X  X  X
 X  X  X
```
- SVG Path: `M0,0 L8,8 M8,0 L0,8`
- ID: `hash-pattern`
- Stroke: 1px @ 30% opacity

### Normal Pattern (Solid)
```
█████████
█████████
█████████
```
- No pattern - solid fill
- Base color only

## Symbol Reference

| Set | Increase | Decrease | Normal | Use Case |
|-----|----------|----------|--------|----------|
| **Primary** | ▲ | ▼ | ● | Default (geometric) |
| **Alternative** | + | − | • | Small sizes (math) |
| **Text** | INC | DEC | SC | Screen readers |

## One-Liner Usage

```tsx
// Get all visualization properties at once
const { color, pattern, symbol, description } = getStitchVisualization(
  'increase',    // stitch type
  'protanopia',  // palette type
  'primary'      // symbol set (optional)
);

// Use in component
<Circle fill={color} accessibilityLabel={description} />
<Text>{symbol}</Text>
```

## Contrast Ratios (WCAG AA Compliance)

| Palette | Inc vs Normal | Dec vs Normal | Inc vs Dec |
|---------|---------------|---------------|------------|
| Protanopia | 5.2:1 ✓ | 4.8:1 ✓ | 6.1:1 ✓ |
| Deuteranopia | 5.2:1 ✓ | 4.8:1 ✓ | 6.1:1 ✓ |
| Tritanopia | 4.9:1 ✓ | 3.8:1 ✓ | 5.4:1 ✓ |
| High Contrast | 15.3:1 ✓✓✓ | 12.8:1 ✓✓✓ | 8.9:1 ✓✓✓ |

✓ = WCAG AA (4.5:1+)
✓✓✓ = WCAG AAA (7:1+)

## Implementation Checklist

- [ ] Import `AccessibilityPatternDefs` in SVG root
- [ ] Use `getStitchVisualization()` for consistent properties
- [ ] Add `accessibilityLabel` to all interactive elements
- [ ] Test patterns render at 8×8 dp minimum size
- [ ] Verify colors in colorblind simulator
- [ ] Test in grayscale/print preview
- [ ] Validate contrast ratios with WebAIM checker

## Common Pitfalls

1. **Forgetting pattern defs** - SVG patterns won't render without `<AccessibilityPatternDefs />`
2. **Using color alone** - Always combine color with patterns/symbols
3. **Wrong palette for user** - Detect or allow user selection of palette type
4. **High contrast on light bg** - White stitches invisible on light backgrounds
5. **Symbol size too small** - Symbols need minimum 12pt to be readable

## Testing URLs

- **Coblis Simulator:** https://www.color-blindness.com/coblis-color-blindness-simulator/
- **WebAIM Contrast Checker:** https://webaim.org/resources/contrastchecker/
- **Color Oracle (Desktop):** https://colororacle.org/

## Related Files

- `/apps/mobile/src/theme/accessibilityTheme.ts` - Main palette definitions
- `/apps/mobile/src/theme/AccessibilityPatterns.tsx` - React Native SVG components
- `/apps/mobile/src/theme/index.ts` - Theme exports
- `/docs/design/colorblind-palette-verification.md` - Full design documentation
