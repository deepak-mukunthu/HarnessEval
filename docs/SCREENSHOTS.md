# 📸 Screenshot Guide

Instructions for capturing screenshots for documentation.

## Quick Method: Use the Script

```bash
# Install playwright
pip install playwright
playwright install chromium

# Make sure server is running
cd backend && python server.py

# In another terminal, run the script
python take_screenshots.py
```

This will automatically capture all screenshots to `docs/images/`.

## Manual Method: Capture Yourself

If you prefer to take screenshots manually:

### 1. Web UI Homepage (01-web-ui-homepage.png)

1. Start server: `cd backend && python server.py`
2. Open: http://localhost:8000
3. Wait for page to load completely
4. Take full-page screenshot
5. **Capture:** Main interface showing input form (left) and harness selection (right)

**Key elements to show:**
- Connection status indicator (green dot)
- Input form with fields
- 5 harness cards
- Test buttons
- Purple gradient background

### 2. Test Problem Input (02-test-problem-input.png)

1. On homepage, fill in:
   - Question: "What is 12 × 8?"
   - Correct Answer: 96
   - Student's Answer: 94
   - Attempt: 1
   - Hint: "Think about 12 groups of 8"
2. Don't click submit yet
3. Take screenshot showing filled form

### 3. Single Harness Response (03-single-harness-response.png)

1. With form filled, click "🚀 Test Harness"
2. Wait for response to appear (2-3 seconds)
3. Take screenshot showing:
   - Filled form at top
   - Response box at bottom with coaching message
   - Hint and encouragement badges

### 4. Compare All Harnesses (04-compare-all-harnesses.png)

1. Click "📊 Compare All Harnesses"
2. Wait for all 5 responses (5-10 seconds)
3. Scroll to show all comparison cards
4. Take screenshot showing grid of 5 harness responses

**Tip:** May need to zoom out (Cmd/Ctrl + -) to fit all cards in one screenshot

### 5. API Documentation (05-api-documentation.png)

1. Open: http://localhost:8000/docs
2. Wait for Swagger UI to load
3. Take screenshot showing:
   - List of API endpoints
   - FastAPI/Swagger branding
   - Endpoint groups

### 6. API Endpoint Detail (06-api-coach-endpoint.png)

1. On API docs page, click on "POST /api/coach"
2. Expand to show request/response schema
3. Take screenshot showing:
   - Endpoint details
   - Request body schema
   - Response schema
   - "Try it out" button

## Optional: Dashboard Screenshots

If you've run experiments:

### 7. Dashboard - Performance Comparison (07-dashboard-performance.png)

```bash
python run_experiment.py 3
python src/dashboard.py
```

1. Open: http://127.0.0.1:8050
2. Go to "Performance Comparison" tab
3. Take screenshot showing all 6 bar charts

### 8. Dashboard - Radar Chart (08-dashboard-radar.png)

1. Click "Radar View" tab
2. Take screenshot showing multi-dimensional radar chart

### 9. Dashboard - Problem Analysis (09-dashboard-problems.png)

1. Click "Problem Analysis" tab  
2. Take screenshot showing grouped bar chart

## Screenshot Specifications

**Recommended settings:**
- Resolution: 1920x1080 or higher
- Format: PNG (better quality than JPG for UI screenshots)
- Browser: Chrome/Firefox (for consistent rendering)
- Zoom: 100% (or 90% for comparison view)

**Capture tools:**
- **Mac:** Cmd+Shift+4 → drag to select area
- **Windows:** Win+Shift+S → drag to select
- **Linux:** Use Screenshot tool or Spectacle
- **Browser extension:** Nimbus Screenshot, Awesome Screenshot

## File Naming Convention

```
docs/images/
├── 01-web-ui-homepage.png           # Main interface
├── 02-test-problem-input.png        # Form filled
├── 03-single-harness-response.png   # Single test result
├── 04-compare-all-harnesses.png     # Comparison view
├── 05-api-documentation.png         # Swagger UI
├── 06-api-coach-endpoint.png        # Endpoint detail
├── 07-dashboard-performance.png     # Dashboard charts
├── 08-dashboard-radar.png           # Radar view
└── 09-dashboard-problems.png        # Problem analysis
```

## Adding Screenshots to README

Once you have the screenshots, reference them in README.md:

```markdown
## Screenshots

### Interactive Web UI
![Web UI Homepage](docs/images/01-web-ui-homepage.png)

### Compare All Harnesses
![Compare Harnesses](docs/images/04-compare-all-harnesses.png)

### API Documentation
![API Docs](docs/images/05-api-documentation.png)

### Results Dashboard
![Dashboard](docs/images/07-dashboard-performance.png)
```

## Tips for Great Screenshots

1. **Clean browser:** Close unnecessary tabs/extensions
2. **Consistent zoom:** Keep 100% zoom across all screenshots
3. **Show context:** Include enough UI to understand what's happening
4. **Highlight key areas:** Consider adding annotations later
5. **Dark mode:** Some users prefer dark mode screenshots
6. **Mobile view:** Consider adding mobile/responsive screenshots

## Image Optimization

After capturing, optimize file sizes:

```bash
# Install ImageMagick (if not installed)
brew install imagemagick  # Mac
# or: sudo apt-get install imagemagick  # Linux

# Optimize all screenshots
cd docs/images
for img in *.png; do
    convert "$img" -quality 85 -strip "optimized_$img"
done
```

## Creating GIFs (Optional)

For animated demos:

```bash
# Install ffmpeg
brew install ffmpeg  # Mac

# Record screen with QuickTime/OBS
# Then convert to GIF
ffmpeg -i demo.mov -vf "fps=10,scale=1000:-1:flags=lanczos" demo.gif

# Or use online tool: https://ezgif.com/video-to-gif
```

**Good GIF ideas:**
- Clicking "Compare All Harnesses" and watching responses appear
- Testing different harnesses and seeing varied responses
- Dashboard tab navigation

## Troubleshooting

**Problem:** Screenshots too large (>1MB each)
**Solution:** Use PNG optimization or save as JPG with quality 85-90

**Problem:** Text appears blurry
**Solution:** Ensure you're capturing at actual size (not scaled)

**Problem:** Colors look washed out
**Solution:** Check color profile settings, export as sRGB

**Problem:** Automated script fails
**Solution:** Make sure server is running and ports are accessible

## Quick Screenshot Checklist

Before uploading to GitHub:

- [ ] All 6 core screenshots captured
- [ ] File names follow convention
- [ ] Images are in `docs/images/` directory
- [ ] File sizes reasonable (<500KB each)
- [ ] Screenshots show full context (not cropped too tight)
- [ ] Browser UI minimal/hidden (press F11 for fullscreen)
- [ ] README.md updated with image references
- [ ] Images committed to git

## Need Help?

If you encounter issues taking screenshots, you can:
1. Ask a colleague to help
2. Use the automated script
3. Submit PR without screenshots (maintainers can add later)
4. Create simple diagrams instead of screenshots

---

**Once screenshots are ready:**
```bash
git add docs/images/
git commit -m "docs: Add screenshots for README"
git push personal main
```
