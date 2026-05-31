#!/usr/bin/env python3
"""
Screenshot capture script for documentation.
Requires: pip install playwright
Then run: playwright install chromium
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def take_screenshots():
    """Capture screenshots of the application."""

    screenshots_dir = Path("docs/images")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        print("📸 Taking screenshots...")

        # 1. Homepage/Web UI
        print("1. Main web UI...")
        await page.goto("http://localhost:8000")
        await page.wait_for_timeout(2000)  # Wait for load
        await page.screenshot(path=screenshots_dir / "01-web-ui-homepage.png")

        # 2. Fill in a test problem
        print("2. Test problem filled...")
        await page.fill("#question", "What is 12 × 8?")
        await page.fill("#correctAnswer", "96")
        await page.fill("#studentAnswer", "94")
        await page.screenshot(path=screenshots_dir / "02-test-problem-input.png")

        # 3. Single harness response
        print("3. Single harness test...")
        await page.click('button:has-text("Test Harness")')
        await page.wait_for_timeout(3000)  # Wait for API response
        await page.screenshot(path=screenshots_dir / "03-single-harness-response.png")

        # 4. Compare all harnesses
        print("4. Comparing all harnesses...")
        await page.click('button:has-text("Compare All Harnesses")')
        await page.wait_for_timeout(5000)  # Wait for all API calls
        await page.screenshot(path=screenshots_dir / "04-compare-all-harnesses.png")

        # 5. API Documentation
        print("5. API docs...")
        await page.goto("http://localhost:8000/docs")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=screenshots_dir / "05-api-documentation.png")

        # 6. API endpoint expanded
        print("6. API endpoint detail...")
        await page.click('div:has-text("POST/api/coach")')
        await page.wait_for_timeout(1000)
        await page.screenshot(path=screenshots_dir / "06-api-coach-endpoint.png")

        await browser.close()
        print(f"\n✅ Screenshots saved to {screenshots_dir}/")
        print("\nScreenshots created:")
        for img in sorted(screenshots_dir.glob("*.png")):
            print(f"  - {img.name}")

if __name__ == "__main__":
    print("🚀 Starting screenshot capture...")
    print("⚠️  Make sure the server is running: cd backend && python server.py\n")

    try:
        asyncio.run(take_screenshots())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTo install dependencies:")
        print("  pip install playwright")
        print("  playwright install chromium")
