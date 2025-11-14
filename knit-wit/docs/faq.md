# Knit-Wit Frequently Asked Questions

Answers to common questions about Knit-Wit pattern generation, usage, and features.

## General Questions

### What is Knit-Wit?

Knit-Wit is a free web application that generates parametric crochet patterns for geometric shapes (spheres, cylinders, cones) based on your specifications. It creates step-by-step instructions and interactive visualization to help you crochet objects of any size.

### Is Knit-Wit free?

Yes! Knit-Wit is completely free to use. No login, no subscription, no hidden costs. Generate as many patterns as you like.

### Do I need an account?

No account required. Just visit https://knit-wit.app and start generating patterns immediately.

### Can I use Knit-Wit offline?

Not currently. Knit-Wit requires an active internet connection because pattern generation happens on our backend servers. Future versions may support offline mode.

### Is my data saved?

Your generated patterns are not saved to cloud or a database. They exist only during your session on your device. For permanent storage, export patterns as PDF or JSON.

### Is Knit-Wit available in other languages?

Currently, Knit-Wit is in English only. Support for additional languages is planned for future versions.

---

## Pattern Generation Questions

### What shapes can Knit-Wit generate?

**MVP v1.0 supports:**
- Spheres (balls, stuffed heads, ornaments)
- Cylinders (cups, containers, straight tubes)
- Cones/Tapered shapes (ice cream cones, party hats)

**Coming in future versions:**
- Cubes
- Pyramids
- Toruses (donut shapes)
- Custom shapes

### What stitch types does Knit-Wit support?

**MVP v1.0:**
- Single Crochet (sc) - basic, tight stitch

**Coming in future versions:**
- Half Double Crochet (hdc)
- Double Crochet (dc)
- Treble Crochet (tr)
- And more!

### How accurate are the generated patterns?

Very accurate. Knit-Wit uses mathematically precise algorithms to:
- Calculate perfect stitch counts based on gauge and dimensions
- Distribute increases/decreases evenly (no lumpy areas)
- Maintain symmetry in shapes
- Estimate yardage accurately

However, **your actual results depend on your crochet technique**. Two people might get slightly different sizes even with the same pattern due to tension differences.

### Can I adjust a pattern after generation?

The MVP doesn't support editing generated patterns. However, you can:
- Generate a new pattern with different parameters
- Download as JSON and edit manually (advanced)
- Export as SVG and modify the diagram visually

Pattern editing will be added in future versions.

### How long does pattern generation take?

Typically 2-5 seconds. Larger, more complex patterns may take up to 10 seconds. This is normal—the backend is calculating optimal stitch placement.

If generation takes longer than 30 seconds, it has timed out and failed. Try refreshing and generating again.

### Why was my pattern generation rejected?

Common reasons:
1. **Pattern too large** - Stitch count would exceed 2000+ stitches. Solutions:
   - Increase gauge (use smaller hook, tighter yarn)
   - Decrease dimensions

2. **Invalid gauge** - Gauge parameters outside practical range. Solutions:
   - Verify your swatch measurements
   - Try typical gauges for your yarn weight

3. **Invalid dimensions** - Dimensions too small or too large. Solutions:
   - Use reasonable sizes (2cm-50cm diameter)
   - Re-enter dimensions carefully

4. **Server error** - Rare. Solution: Refresh page and try again.

---

## Yarn & Gauge Questions

### How do I determine my gauge?

1. **Crochet a test swatch** with your chosen yarn and hook
   - Make it at least 10cm x 10cm
   - Use the same stitch (single crochet for MVP)
   - Block it if pattern instructions require blocking

2. **Count stitches per 10cm**
   - Measure 10cm horizontally across your swatch
   - Count how many stitches fit in that space

3. **Count rows per 10cm**
   - Measure 10cm vertically down your swatch
   - Count how many rows fit in that space

4. **Enter into Knit-Wit**: Input these numbers in the gauge fields

### Can I use Knit-Wit without checking gauge?

You *can*, but results may vary. Knit-Wit provides default gauges based on yarn weight, but:
- Your tension might be different
- Different brands of "same weight" yarn vary
- Final size might be off by 10-20%

**Recommendation**: Check gauge for accurate results, especially if size is important.

### How do I adjust for my yarn/hook?

Knit-Wit patterns are based on gauge, not specific hook sizes. To use different yarn:

1. **Determine new yarn's gauge** (check label or test swatch)
2. **Generate a new pattern** with the new gauge
3. **Same final size, different stitch count**

Example:
- Original pattern: 14 stitches per 10cm = 5-inch sphere
- Using thicker yarn (10 stitches per 10cm): Enter new gauge
- New pattern: Same 5-inch sphere, fewer total stitches

### What if yarn label doesn't specify gauge?

Try these approaches:

1. **Test swatch**: Make a small swatch and measure it
2. **Ravelry.com**: Search yarn name and see projects to estimate
3. **Craft store**: Ask staff for typical gauges for that yarn
4. **Trial and error**: Generate pattern with estimated gauge, make small portion to check

### What yarn weights work best with Knit-Wit?

**Recommended:**
- Worsted Weight (medium, 12-16 sts/10cm)
- Aran Weight (heavier, 10-14 sts/10cm)
- DK Weight (light, 16-20 sts/10cm)

**Possible but challenging:**
- Fingering weight (very fine, 20+ sts/10cm) - very tiny stitches
- Bulky weight (very thick, 8-10 sts/10cm) - very large stitches

**Note**: MVP only supports single crochet. Different stitch types coming in future versions.

### How accurate is the yardage estimate?

Knit-Wit estimates yardage based on:
- Stitch count × stitch size × yarn factor
- Mathematical calculation, not dependent on actual yarn

**Accuracy**: Usually within 10-20%, but can vary based on:
- How loosely/tightly you crochet
- Yarn actual weight vs. label weight
- Block type and stitch type

**Recommendation**: Add 20% to estimate for safety. Better to have extra yarn than run short!

---

## Export Questions

### What export formats are available?

**MVP v1.0 supports:**
- **PDF**: Best for printing and sharing
- **SVG**: Best for editing or high-quality printing
- **PNG**: Best for social media and sharing
- **JSON**: Best for archival and advanced use

### Which format should I use?

**PDF**:
- Use if: You want to print or email
- Includes: Full instructions, diagram, all details
- Pro: Universal, looks professional, easy to print

**SVG**:
- Use if: You want to edit the diagram or need infinite zoom
- Best for: Designers, editing patterns, print shops
- Requires: Vector editing software (Adobe Illustrator, Inkscape, Figma)

**PNG**:
- Use if: You want to share on social media or via message
- Best for: Quick sharing, no editing needed
- Pro: Everyone can view, small file size

**JSON**:
- Use if: You're a programmer or want to process pattern data
- Best for: Backup, API integration, data analysis
- Requires: Understanding of JSON format

### Can I edit exported patterns?

**PDF**: Limited editing (add notes, but not pattern)
**SVG**: Full editing (redraw diagram in design software)
**PNG**: Can't edit without design software
**JSON**: Can edit in text editor (advanced)

Pattern editing features coming in future versions.

### Can I sell items made from Knit-Wit patterns?

Yes! Feel free to:
- Make items and sell them
- Sell patterns you've exported
- Modify patterns and sell them

No attribution required (but appreciated!). Knit-Wit patterns are free for personal and commercial use.

### What if I export a pattern and then need to regenerate it?

Regenerating the same parameters will produce the same pattern. However:
- You cannot import JSON patterns back in
- You must regenerate from original parameters
- Keep original dimensions/gauge recorded

**Pro tip**: Export as JSON and save the metadata (shape, dimensions, gauge) in a text file for future reference.

---

## Accessibility Questions

### Is Knit-Wit accessible?

Yes! Knit-Wit meets WCAG 2.1 Level AA accessibility standards:
- Full screen reader support
- Complete keyboard navigation
- High contrast mode
- Dyslexia-friendly font option
- Scalable text and UI

### What screen readers are supported?

- **Windows**: NVDA (free), JAWS (paid)
- **macOS**: VoiceOver (built-in)
- **iOS**: VoiceOver (built-in)
- **Android**: TalkBack (built-in)

All major screen readers fully support Knit-Wit.

### Can I navigate without a mouse?

Yes! Full keyboard navigation supported:
- Tab/Shift+Tab to navigate
- Enter to activate buttons
- Arrow keys for dropdowns
- Escape to close dialogs

All functionality available via keyboard.

### Does Knit-Wit work with browser zoom?

Yes! Fully responsive to browser zoom:
- Zoom up to 300%
- All features remain accessible
- Text stays readable
- Touch targets stay appropriately sized

### What is dyslexia-friendly font?

OpenDyslexic font has:
- Weighted bottoms on letters (prevents flipping)
- Distinct letter shapes (B/D/P more different)
- Larger, open letter forms
- Improved spacing

Tested by dyslexic users, significantly improves readability.

### Is color the only way to understand patterns?

No! The visualization uses:
- Color coding (but also)
- Text labels
- Position in diagram
- Round numbers and stitch counts

All information available through non-visual means.

---

## Kid Mode Questions

### What is Kid Mode?

Kid Mode is a simplified interface designed for children and beginners:
- Larger buttons (easier to tap)
- Simpler stitch names
- Beginner-friendly explanations
- Animated tutorials
- Encouraging language

### When should I use Kid Mode?

Use Kid Mode if:
- You're teaching children
- You're new to crochet
- You prefer simplified terminology
- You want animated technique tutorials
- You like larger, simpler UI

### How do I turn on Kid Mode?

1. Open Settings
2. Toggle "Kid Mode" on
3. Interface updates immediately

### Can adults use Kid Mode?

Absolutely! Kid Mode is for anyone who prefers simplified, clearer explanations. No age restriction.

### What techniques are covered in Kid Mode tutorials?

- What is an increase? (30-second animation)
- What is a decrease? (30-second animation)
- Understanding gauge (interactive guide)
- Reading pattern notation (step-by-step)
- Magic ring vs chain-4 start (demonstration)

More tutorials coming in future versions.

---

## US vs UK Terminology Questions

### What's the difference between US and UK terminology?

The same stitches have completely different names! This causes major confusion.

**Example: Single Crochet**
- US: Single Crochet (sc) = shortest stitch
- UK: Double Crochet (dc) = shortest stitch

**Example: Double Crochet**
- US: Double Crochet (dc) = medium stitch
- US: Half Double Crochet (hdc) = between short and medium

- UK: Treble (tr) = medium stitch
- UK: Double Treble (dtr) = longer

### Why are there two systems?

Historical: US and UK developed different naming conventions in the 1800s, and both communities stuck with their systems. Now it's just tradition.

### How do I know which to use?

**Check the pattern source:**
- US sources (Ravelry.com, American magazines) → US terms
- UK sources (UK magazines, UK designers) → UK terms
- If unsure: Ask the pattern designer

**Our recommendation:**
- Use whichever you learned first
- Be consistent within a project
- Knit-Wit can generate in either system

### Can I convert patterns between US and UK?

Yes, but it's tricky. A safe approach:
1. Follow the pattern in your familiar system
2. Adjust stitch counts by trial and error
3. Or use Knit-Wit to generate in your preferred system!

Knit-Wit always generates correct stitch patterns regardless of terminology chosen.

### What terminology does Knit-Wit use by default?

**Default: US terminology**

You can change to UK terminology in:
- Settings (applies to all future patterns)
- When generating a pattern (applies to that pattern only)

---

## Performance & Technical Questions

### Why does generation sometimes take longer?

Pattern generation time depends on:
- **Pattern complexity** (larger patterns = more calculations)
- **Server load** (busy times may be slower)
- **Your internet** (slow connection = longer perceived time)

Typical time: 2-5 seconds
Maximum: Should complete within 30 seconds

### Is there a way to make generation faster?

Yes:
- **Simpler patterns** (smaller dimensions) are faster
- **Lower gauge** (fewer total stitches) = faster
- **Try at different times** (off-peak faster)

Backend performance continues to improve in each release.

### What's the largest pattern I can generate?

**Limits:**
- Maximum stitch count: ~2000 stitches per round
- Maximum dimensions: ~50cm (about 20 inches)
- Maximum yardage estimate: ~500 yards

These limits prevent unrealistic patterns. If you hit a limit, try:
- Larger gauge (fewer stitches)
- Smaller dimensions
- Different yarn weight

### Do I need a powerful device?

Minimal requirements:
- Any device with a web browser (5+ years old is fine)
- Internet connection (any speed)
- No special hardware needed

Visualization works smoothly on phones, tablets, and computers.

### Can I run Knit-Wit on my phone?

Yes! Knit-Wit is mobile-first:
- Touch-optimized interface
- Works on iOS and Android
- No app download needed (web app)
- Responsive design for all screen sizes

Just visit https://knit-wit.app in your mobile browser.

---

## Comparison Questions

### How is Knit-Wit different from pattern databases like Ravelry?

**Ravelry** (pattern database):
- Browse thousands of community patterns
- Connect with other crafters
- Track projects and stash
- Requires searching, sorting

**Knit-Wit** (pattern generator):
- Instantly generate custom patterns
- Any size, any parameters
- No searching required
- Unique patterns specifically for you

**Complementary**: Use Knit-Wit to generate patterns, use Ravelry to find designs and connect with community.

### Can I use Knit-Wit patterns with other crochet techniques?

Sure! Knit-Wit patterns use basic single crochet, but you can:
- Substitute different stitches (changes gauge, adjust stitch count)
- Add colorwork or patterns (overlay your own design)
- Modify rounds (add borders, decorations)

The stitch count is correct; you can crochet it however you like!

### Is Knit-Wit better than hiring a pattern designer?

Different purposes:
- **Quick projects**: Knit-Wit saves time and money
- **Custom designs**: Professional designers understand personal style
- **Complex projects**: Designers handle intricate details

**Best approach**: Use Knit-Wit for basic shapes, hire designers for complicated projects.

---

## Privacy & Data Questions

### Is my data private?

Yes. Knit-Wit does not:
- Save your patterns
- Collect personal information
- Use cookies for tracking
- Share data with anyone

Your patterns exist only on your device during your session.

### Do you track my activity?

We log:
- Basic server performance metrics
- Error reports (to fix bugs)
- Aggregated statistics (how many patterns generated daily)

We do NOT track:
- What patterns you generate
- Your personal information
- Your browsing habits
- Your device details

### What data does Knit-Wit collect?

Minimal:
- Anonymous usage statistics
- Error reports
- Server performance metrics

All data aggregated and anonymized. No personal information collected.

### Is Knit-Wit GDPR compliant?

Yes, GDPR compliant by design:
- No personal data collection
- No third-party tracking
- No data retention
- No cookies for analytics

You control all your data (none stored on our servers).

---

## Future Features Questions

### What's coming in future versions?

**Phase 1 (planned):**
- More shapes (cubes, pyramids)
- More stitch types (double crochet, etc.)
- Pattern saving and history
- User accounts (optional)

**Phase 2+ (planned):**
- Colorwork and stripes
- Custom shape definitions
- Community pattern sharing
- AR preview

**Would you like a feature?** Email feedback@knit-wit.app

### When will [feature] be released?

Check the roadmap:
- https://knit-wit.app/roadmap
- GitHub issues: github.com/knit-wit/issues
- Email: feedback@knit-wit.app

Major features planned for Q1-Q2 2025.

### Can I request a feature?

Absolutely! We love feature requests:
1. Email: feedback@knit-wit.app
2. Include your idea and use case
3. Or: GitHub discussion/issues

Every suggestion helps us prioritize development.

### Will Knit-Wit always be free?

Current plan: Yes, Knit-Wit will remain free for basic pattern generation. Premium features (advanced shapes, advanced exports) might be added in future, but basic functionality will always be free.

---

## Troubleshooting Questions

### Pattern generation fails with timeout error

**Cause**: Generation took too long (>30 seconds)

**Solutions:**
1. Refresh the page
2. Try a simpler pattern (smaller, fewer stitches)
3. Try again at different time (less server load)
4. Clear browser cache and try again

### "Gauge parameters invalid" error

**Cause**: Your gauge numbers outside valid range

**Solutions:**
1. Double-check your swatch measurements
2. Try typical gauge for your yarn weight:
   - Worsted: 12-16 stitches per 10cm
   - DK: 16-20 stitches per 10cm
3. Measure swatch again more carefully

### Visualization doesn't load

**Cause**: JavaScript not supported or too slow device

**Solutions:**
1. Refresh page
2. Check JavaScript enabled (most browsers do by default)
3. Try different browser
4. Update browser to latest version
5. Clear cache: Ctrl+Shift+Delete (or equivalent)

### Export doesn't download

**Cause**: Browser blocking, poor connection, or device full

**Solutions:**
1. Check browser settings allow downloads from knit-wit.app
2. Check internet connection
3. Check available device storage
4. Try different format (PDF vs SVG vs PNG)
5. Try different browser

### Screen reader doesn't read content

**Cause**: Page not properly loaded or accessibility feature disabled

**Solutions:**
1. Refresh page and wait for full load
2. Check screen reader is compatible (NVDA, JAWS, VoiceOver)
3. Check accessibility enabled in device settings
4. Try incognito/private mode (disables extensions)

### "Still have problems?"

Email us with:
1. What you were trying to do
2. Exact error message (screenshot if possible)
3. Your device type and browser
4. Contact: support@knit-wit.app

We'll help troubleshoot!

---

## Getting Started

**New to Knit-Wit?**
1. Read [User Guide](./user-guide.md) for detailed instructions
2. Start with Settings to enable your preferences
3. Try generating a simple sphere first
4. Export and print your pattern
5. Happy crocheting!

**Have more questions?**
- Email: support@knit-wit.app
- Website: https://knit-wit.app

---

**Knit-Wit MVP v1.0**
Last Updated: November 2024
