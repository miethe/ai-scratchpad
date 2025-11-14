# Knit-Wit User Guide

Welcome to Knit-Wit! This guide will help you generate beautiful, parametric crochet patterns for geometric shapes and visualize them step-by-step.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Generating Your First Pattern](#generating-your-first-pattern)
4. [Understanding Patterns](#understanding-patterns)
5. [Visualization Guide](#visualization-guide)
6. [Exporting Patterns](#exporting-patterns)
7. [Using Kid Mode](#using-kid-mode)
8. [Accessibility Features](#accessibility-features)
9. [Settings and Customization](#settings-and-customization)
10. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Knit-Wit?

Knit-Wit is a free, mobile-friendly web application designed to help crocheters of all skill levels generate professional crochet patterns for geometric shapes. Instead of searching through multiple pattern websites, Knit-Wit creates custom patterns based on your specific measurements and preferences.

### What Can Knit-Wit Do?

- **Generate Patterns**: Create parametric crochet patterns for spheres, cylinders, and cones in seconds
- **Visualize**: See round-by-round instructions with interactive step-by-step visualization
- **Customize**: Adjust pattern parameters to match your specific yarn, hook size, and preferences
- **Export**: Download patterns in multiple formats (PDF, SVG, PNG, JSON)
- **Accessible**: Designed for everyone, including support for screen readers, high contrast modes, and dyslexia-friendly fonts
- **Beginner-Friendly**: Kid Mode offers simplified terminology and helpful tutorials

### Who Should Use Knit-Wit?

- **Hobbyist crocheters** - Create quick patterns without searching pattern databases
- **Pattern designers** - Generate base patterns as starting points for variations
- **Yarn crafters** - Quickly design items for specific yarn weights and hook sizes
- **Educators** - Use interactive visualization to teach crochet techniques
- **Beginners** - Get started with simple, clear instructions in Kid Mode

---

## Getting Started

### System Requirements

- **Browsers**: Chrome, Firefox, Safari, or Edge (latest versions)
- **Mobile Devices**: iOS 14+ or Android 10+
- **Screen Reader Support**: NVDA (Windows), JAWS (Windows), or VoiceOver (iOS/macOS)
- **Internet**: Active internet connection required for pattern generation

### Opening Knit-Wit

1. Visit https://knit-wit.app in your web browser
2. The app loads with a welcome screen featuring key features and a quick-start button
3. No account or login required—start generating patterns immediately

### First-Time User Checklist

- Review the home screen feature highlights
- Read "Interpreting US vs UK Terminology" if not familiar with terminology differences
- Check "Settings" to set your preferred terminology (US or UK stitch names)
- For kids or beginners: Enable "Kid Mode" in Settings for simplified instructions

---

## Generating Your First Pattern

### Step-by-Step Pattern Generation

#### 1. Navigate to Generate Screen

From the home screen, tap or click the "Generate Pattern" button. You'll see the pattern generator form.

#### 2. Select Your Shape

Choose the shape for your project:

- **Sphere**: Create balls, amigurumi heads, or perfectly round objects
  - Parameters: Diameter (in cm or inches)
  - Good for: Bouncy balls, stress toys, ornaments

- **Cylinder**: Create tubes, cups, or straight-sided objects
  - Parameters: Height, Diameter
  - Good for: Containers, cups, vases, hat bases

- **Cone/Tapered**: Create pointed objects with even increase distribution
  - Parameters: Height, Base Diameter
  - Good for: Ice cream cones, hats, party decorations

#### 3. Enter Dimensions

- **Diameter**: Measure across the widest part of your desired object
- **Height**: (for cylinders/cones) Measure from base to top
- **Units**: Choose between centimeters (cm) or inches (in)

**Helpful Conversion**:
- 1 inch = 2.54 cm
- Most yarn patterns use cm, but US crocheters often prefer inches

#### 4. Set Your Gauge

**What is Gauge?**

Gauge measures how tightly you crochet. Different gauge = different size object from the same stitch count.

**How to Check Your Gauge:**

1. Crochet a swatch with your yarn and hook size (10cm x 10cm minimum)
2. Count stitches across 10cm
3. Count rows across 10cm
4. Enter these numbers in the gauge fields

**Example:**
- Your swatch has 14 stitches per 10cm
- Your swatch has 16 rows per 10cm
- Enter: Stitches per 10cm = 14, Rows per 10cm = 16

**Finding Gauge Without a Swatch:**

- Check your yarn label for recommended hook sizes
- Look at pattern databases (Ravelry.com) for similar yarn and hook combinations
- Knit-Wit has sensible defaults, but custom gauge gives more accurate results

#### 5. Choose Stitch Type

Currently, MVP supports:
- **Single Crochet (sc)**: The most basic stitch, creates dense, tight fabric
- Additional stitches coming in future versions

#### 6. Select Terminology

Choose your preferred stitch name terminology:
- **US Terminology**: Used primarily in North America
- **UK Terminology**: Used in UK and Commonwealth countries

The pattern will use your chosen terminology throughout.

#### 7. Generate Your Pattern

Click "Generate Pattern" and wait 2-3 seconds for the magic to happen. The pattern engine calculates:
- Total stitch count needed
- Where to place increases/decreases
- Yardage estimate
- Round-by-round instructions

**Common Questions:**
- *"Why does generation take a few seconds?"* The backend calculates optimal increase placement. Larger patterns take longer.
- *"What if it says it's too large?"* Very large patterns need unusual gauge or would use excessive yarn. Try smaller dimensions.

---

## Understanding Patterns

### What You'll See After Generation

After successful generation, you'll see:

1. **Pattern Summary**
   - Shape type and dimensions
   - Estimated yarn needed
   - Stitch count per round
   - Difficulty indicator

2. **Pattern Notation**
   - Stitch abbreviations (sc, inc, dec, etc.)
   - Round numbering starting from Round 1
   - Special notes for technique (magic ring, join rounds, etc.)

3. **Visualization Preview**
   - Step-by-step visual guide showing the shape developing
   - Interactive round selector
   - Stitch highlighting showing what changes each round

### Pattern Abbreviations (US Terminology)

| Abbreviation | Term | Meaning |
|:---|:---|:---|
| **sc** | Single Crochet | Basic stitch through both loops |
| **inc** | Increase | 2 stitches in same stitch |
| **dec** | Decrease | Single crochet 2 together |
| **MR** | Magic Ring | Starting method (optional, can use ch4 + join) |
| **slst** | Slip Stitch | Join stitch for joined rounds |
| **ch** | Chain | Base row stitch |

**Note:** UK terminology uses different names for the same stitches. Enable UK terminology in Settings to see UK names.

### Stitch Techniques Explained

#### Magic Ring (MR)

A starting method that creates a tight center:

1. Make a loop with yarn
2. Insert hook in ring, yarn over, pull through
3. Chain 1 to secure
4. Work stitches around ring
5. Pull yarn end to tighten center

**Alternative:** If magic ring is difficult, use ch4 + slip stitch to join instead.

#### Increases (inc)

Working 2 stitches in the same stitch to add stitches:

1. Insert hook in stitch
2. Yarn over, pull through (2 loops on hook)
3. Yarn over, pull through both loops (1 stitch)
4. Repeat in same stitch for second stitch

#### Decreases (dec)

Combining two stitches into one to reduce stitch count:

1. Insert hook in first stitch, yarn over, pull through (2 loops)
2. Insert hook in next stitch, yarn over, pull through (3 loops total)
3. Yarn over, pull through all 3 loops

### Pattern Sustainability Features

All Knit-Wit patterns use:
- **Consistent yarn weight**: Same yarn throughout
- **Spiral method**: No joins between rounds (more seamless)
- **Even distribution**: Increases/decreases placed mathematically evenly
- **Beginner-friendly**: Only basic stitches, no complex techniques

---

## Visualization Guide

### Accessing Visualization

After generating a pattern, tap/click "View Visualization" or the visualization tab.

### Understanding the Visualization

The visualization shows:

1. **Shape Preview**: A 2D representation of your crocheted object as viewed from above or side
2. **Round Indicator**: Current round number and total rounds
3. **Stitch Count**: How many stitches are active in the current round
4. **Interactive Controls**:
   - **Play**: Animate through all rounds automatically
   - **Previous/Next**: Step through one round at a time
   - **Round Selector**: Jump to any specific round
   - **Zoom In/Out**: Get closer or farther view
   - **Reset**: Return to starting position

### How to Read the Visualization

- **Colors**: Each color represents different parts of the pattern (increases appear highlighted)
- **Shape Changes**: Watch how increases add stitches and gradually expand the object
- **Mid-point**: Halfway through, the shape reaches maximum width and begins decreasing
- **Final Rounds**: Stitches decrease until the shape closes

### Using Visualization for Learning

- **Beginners**: Watch the full animation to understand structure
- **Visual Learners**: See exactly how increases and decreases affect shape
- **Designers**: Experiment with different gauges to see size impact
- **Presentation**: Project during teaching or crafting circles to demonstrate technique

### Keyboard Navigation

- **Space**: Play/Pause animation
- **Left Arrow**: Previous round
- **Right Arrow**: Next round
- **Plus (+)**: Zoom in
- **Minus (-)**: Zoom out
- **Tab**: Focus on controls
- **Enter**: Activate button

---

## Exporting Patterns

### Export Options

Knit-Wit provides multiple export formats to suit different needs:

#### PDF Export

**Best for**: Printing, physical reference while crocheting

**Includes**:
- Complete round-by-round instructions
- Stitch count per round
- Yardage estimates
- Shape diagram
- Your selected terminology

**Paper Size Options**: A4, Letter (US), Legal
**How to Export**:
1. From pattern details, tap/click "Export as PDF"
2. Choose paper size
3. Your browser downloads the PDF
4. Print or save to device

#### SVG Export

**Best for**: Editing, digital reference, sharing with other designers

**Includes**:
- Scalable diagram (infinite zoom quality)
- Vector format (editable in Adobe Illustrator, Inkscape, Figma)
- High-resolution output

**How to Export**:
1. From pattern details, tap/click "Export as SVG"
2. Save the file to your device
3. Open in any vector editor or image viewer

#### PNG Export

**Best for**: Social media, email sharing, quick previews

**Includes**:
- High-resolution image of pattern diagram
- Raster format (standard image)

**How to Export**:
1. From pattern details, tap/click "Export as PNG"
2. Choose resolution (Standard or High-Quality)
3. Save to device or share directly

#### JSON Export

**Best for**: Advanced users, API integration, backup/archival

**Includes**:
- Complete Pattern DSL v0.1 format
- All pattern data in machine-readable format
- Can be re-imported or processed by other tools

**How to Export**:
1. From pattern details, tap/click "Export as JSON"
2. Save the file
3. Store for future use or import elsewhere

### Sharing Patterns

**Export as PDF or PNG**, then:
- Email to friends
- Upload to pattern sharing sites (Ravelry, Pinterest)
- Post on social media
- Print for crafting groups

**Note**: Always give credit to Knit-Wit if sharing your designs!

---

## Using Kid Mode

### What is Kid Mode?

Kid Mode simplifies Knit-Wit for children and beginners with:
- Larger touch targets (easier to tap)
- Simplified stitch terminology
- Beginner-friendly explanations
- Animated tutorials showing basic techniques
- Friendly, encouraging language

### Enabling Kid Mode

1. Open Settings screen
2. Toggle "Kid Mode" on
3. Interface updates immediately with simplified design

### What Changes in Kid Mode

#### Simplified Terminology

| Standard | Kid Mode |
|:---|:---|
| Single Crochet | Basic Stitch |
| Increase | Add Stitches |
| Decrease | Skip Stitches |
| Magic Ring | Yarn Ring Start |
| Slip Stitch | Connector |

#### Simplified Instructions

- Shorter explanations
- Step-by-step numbered lists
- Visual diagrams for each technique
- Encouraging language ("You're doing great!")

#### Helpful Tutorials

- "What is an increase?" - Animated 30-second tutorial
- "Understanding gauge" - Interactive gauge explainer
- "Reading your pattern" - Step-by-step guide
- Access these from the Help section anytime

### Is Kid Mode Right for Me?

Use Kid Mode if you:
- Are learning to crochet
- Are teaching children
- Prefer simplified, clearer language
- Want animated technique tutorials
- Prefer larger text and buttons

---

## Accessibility Features

Knit-Wit is designed for everyone. We provide multiple accessibility options.

### Screen Reader Support

**Fully Compatible With:**
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (iOS/macOS)
- TalkBack (Android)

**Features:**
- All interactive elements labeled for screen readers
- Form fields clearly associated with labels
- Navigation landmarks for easy page jumping
- Error messages announced clearly
- Pattern content presented in logical reading order

**Using with Screen Reader:**
1. Enable your device's screen reader
2. Open Knit-Wit normally
3. Navigate using screen reader controls
4. All functionality fully accessible

### High Contrast Mode

**Enable in Settings:**
1. Open Settings screen
2. Toggle "High Contrast" on
3. Text and UI elements use higher contrast colors
4. Meets WCAG AAA color contrast standards

**What Changes:**
- Text on backgrounds: 7:1 contrast ratio (darker text)
- Button text: Higher contrast for clarity
- Error messages: More visible red
- Borders: More prominent dividers

### Dyslexia-Friendly Font

**Enable in Settings:**
1. Open Settings screen
2. Toggle "Dyslexia Font" on
3. Text displays in OpenDyslexic font
4. Improved readability for dyslexic users

**Features of Dyslexia Font:**
- Weighted bottoms on letters (B, D, P, R less confusing)
- Larger, distinct letter shapes
- Improved letter spacing
- Tested by dyslexic users

### Keyboard Navigation

Full keyboard support for all features:

| Key/Combo | Action |
|:---|:---|
| **Tab** | Move to next interactive element |
| **Shift + Tab** | Move to previous element |
| **Enter** | Activate button or link |
| **Space** | Toggle checkbox or radio button |
| **Arrow Keys** | Navigate within dropdowns or sliders |
| **Esc** | Close dialogs or menus |

### Zoom Support

- Pinch to zoom on touch devices (1.5x to 3x support)
- Browser zoom (Ctrl/Cmd +/- keys)
- Responsive design adapts to all zoom levels
- Text remains readable and functional at all zoom levels

### Accessibility Compliance

Knit-Wit meets **WCAG 2.1 Level AA** standards:
- ✓ Perceivable: Content visible to everyone
- ✓ Operable: All functionality via keyboard
- ✓ Understandable: Clear language, predictable behavior
- ✓ Robust: Compatible with assistive technologies

---

## Settings and Customization

### Accessing Settings

1. Open the app and locate "Settings" (usually gear icon)
2. Adjust preferences below

### Available Settings

#### Language & Terminology

**Stitch Terminology**
- Choose: US or UK stitch names
- Affects: All pattern instructions and abbreviations
- Default: US terminology
- *Note*: Can be overridden when generating patterns

#### Accessibility Options

**High Contrast Mode**
- Toggle: On/Off
- Effect: Increases text/UI contrast for better visibility
- Default: Off

**Dyslexia Font**
- Toggle: On/Off
- Effect: Enables OpenDyslexic font for easier reading
- Default: Off

**Kid Mode**
- Toggle: On/Off
- Effect: Simplified UI, beginner-friendly copy, larger buttons
- Default: Off

#### Display Options

**Dark Mode** (future feature)
- Toggle: On/Off
- Effect: Uses dark color scheme to reduce eye strain
- Coming soon in future versions

**Text Size**
- Options: Small, Regular, Large
- Effect: Increases all text sizes proportionally
- Default: Regular

#### Data & Privacy

**Clear History**
- Button: "Clear Pattern History"
- Effect: Removes all previously generated patterns from device
- Note: Cannot be undone; patterns not in cloud

**Export Settings**
- Button: "Export Settings as JSON"
- Effect: Saves your settings and preferences as a file
- Use Case: Back up settings or transfer to another device

---

## Troubleshooting

### Pattern Generation Issues

#### "Generation is slow"

**Normal behavior**: Pattern generation takes 2-5 seconds
- **Why?** The backend calculates optimal stitch placement mathematically
- **If longer than 10 seconds**: Refresh the page and try again

**Solutions:**
1. Ensure internet connection is stable
2. Try a simpler pattern (smaller dimensions)
3. Clear browser cache (Settings → Clear Cache)
4. Refresh page and try again

#### "Pattern is too large"

**Message**: "Pattern would exceed reasonable stitch count"

**Why?** Knit-Wit prevents generation of patterns that would use excessive yarn or require unreasonable stitch counts.

**Solutions:**
1. **Increase gauge**: More stitches per cm = smaller finished object
   - Try a hook one size smaller
   - Try a yarn with tighter gauge
2. **Decrease dimensions**: Make object smaller
3. **Check yarn weight**: Are you using the right yarn for desired size?

#### "Invalid gauge"

**Message**: "Gauge parameters must be between X and Y"

**Why?** Entered gauge falls outside the practical range

**Solutions:**
1. **Re-check your swatch**:
   - Did you measure correctly?
   - Is swatch at least 10cm x 10cm?
   - Did you count 10cm sections accurately?
2. **Try typical gauges**:
   - Worsted yarn: 12-16 sts/10cm
   - Sport yarn: 16-18 sts/10cm
   - Chunky yarn: 8-12 sts/10cm

#### "Generation failed"

**Message**: "An error occurred. Please try again."

**Why?** Unexpected backend error (rare)

**Solutions:**
1. Refresh the page
2. Clear browser cache
3. Try a different browser
4. Check internet connection
5. Try generating a simpler pattern first

### Export Issues

#### "Export button doesn't work"

**Possible causes:**
1. Internet connection lost
2. Browser popup blocker preventing download
3. Insufficient device storage

**Solutions:**
1. Check internet connection
2. Allow Knit-Wit to download files in browser settings
3. Free up device storage space
4. Try different export format

#### "PDF looks strange"

**Common issues:**
1. **Font not embedding**: Use browser's PDF reader to print-to-file
2. **Layout broken**: Try different paper size
3. **Colors faint**: Ensure "Backup" or "Print background" is enabled in print settings

**Solutions:**
1. Try exporting as SVG instead (better for printing later)
2. Change paper size to A4 or Letter
3. When printing: Enable "Background Graphics" in print dialog

#### "Can't open exported file"

**File type problems:**
- **PDF**: Should open in any PDF reader
- **SVG**: Open with image viewer or edit with design software
- **PNG**: Open with any image viewer
- **JSON**: Open with text editor or import tool

**Solutions:**
1. Make sure your device has appropriate software installed
2. Try saving with different filename
3. Check file wasn't corrupted during download

### Visualization Issues

#### "Visualization doesn't display"

**Why?** Visualization requires modern browser JavaScript

**Solutions:**
1. Ensure JavaScript is enabled (most browsers do by default)
2. Try different browser
3. Refresh the page
4. Update your browser to latest version

#### "Animation is choppy"

**Why?** Device performance or browser rendering issues

**Solutions:**
1. Close other browser tabs to free memory
2. Reduce other running applications
3. Try browser's "Performance Mode" if available
4. Use keyboard to step through instead of play animation

### Accessibility Issues

#### "Screen reader not reading content"

**Solutions:**
1. Refresh page and try again
2. Ensure screen reader is compatible (NVDA, JAWS, VoiceOver)
3. Check accessibility setting is enabled in screen reader
4. Try different screen reader if available

#### "High contrast mode doesn't work"

**Solutions:**
1. Refresh page after enabling
2. Clear browser cache and cookies
3. Try in incognito/private mode
4. Check browser supports CSS custom properties

#### "Keyboard navigation doesn't work"

**Solutions:**
1. Ensure focus is on page (click page first)
2. Check Tab key isn't reassigned in browser settings
3. Try with external keyboard (if on mobile)
4. Try different browser

### General Help

#### Still having trouble?

1. **Check internet connection**: Some features require online access
2. **Clear cache**: Settings → Clear Cache in app
3. **Update browser**: Ensure you're on latest version
4. **Try incognito mode**: Tests if extensions are interfering
5. **Email support**: Send detailed description to support@knit-wit.app

#### Report a Bug

If you find a bug:
1. Note exact steps to reproduce
2. Include your device type and OS version
3. Include browser name and version
4. Take a screenshot if possible
5. Email: bugs@knit-wit.app

---

## FAQ & Common Questions

See [FAQ.md](./faq.md) for answers to frequently asked questions.

---

## Glossary

**Amigurumi**: Japanese crochet technique for making small stuffed animals

**Gauge**: How many stitches and rows appear in 10cm of crocheted fabric

**Stitch**: The basic loop that makes up crochet fabric

**Single Crochet (US)**: The shortest basic crochet stitch

**Double Crochet (US)**: A medium-height stitch (not yet supported)

**Magic Ring**: A technique for starting patterns with a tight center

**Slip Stitch**: A stitch used to join rounds or move yarn

**Increase**: Adding stitches by working multiple stitches in one stitch

**Decrease**: Removing stitches by combining multiple stitches into one

**Round**: One complete circle of stitches; used instead of "row" in circular crochet

**Yarn Weight**: Classification of yarn thickness (worsted, sport, etc.)

---

## Getting Help

### Within Knit-Wit

- **Help Icon**: Tap the ? icon for context-sensitive help
- **Settings**: Contains accessibility options and information
- **Tutorials**: Kid Mode includes animated technique tutorials

### Online Resources

- **Official Website**: https://knit-wit.app
- **Support Email**: support@knit-wit.app
- **Issue Tracker**: https://github.com/knit-wit/issues

### Learning More About Crochet

- **Ravelry.com**: Pattern database and community
- **YouTube**: Search for "crochet [stitch name]" for video tutorials
- **Crafting Circles**: Find local groups at libraries or yarn shops

---

## Feedback & Suggestions

We'd love to hear from you! Share feedback about:
- New features you'd like
- Shapes or stitches to support
- Accessibility improvements
- Bugs or issues

**Email**: feedback@knit-wit.app

---

**Knit-Wit MVP v1.0**
Last Updated: November 2024
