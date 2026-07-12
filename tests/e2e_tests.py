"""
FrugalRoute Playwright E2E Test Suite
Tests all 4 pages: Landing, Chat, Analytics, Settings
"""
import asyncio
import json
import time
from playwright.async_api import async_playwright, expect, Page

BASE_URL = "http://localhost:8080"
BACKEND_URL = "http://localhost:8000"
RESULTS = []

def log(test_name: str, status: str, detail: str = ""):
    icon = "[OK]" if status == "PASS" else "[XX]"
    print(f"  {icon} [{status}] {test_name}" + (f" - {detail}" if detail else ""))
    RESULTS.append({"test": test_name, "status": status, "detail": detail})

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
async def goto(page: Page, path: str = ""):
    await page.goto(f"{BASE_URL}{path}", wait_until="networkidle", timeout=15000)

# ─────────────────────────────────────────────────────────────────────────────
# SUITE 1: BACKEND HEALTH
# ─────────────────────────────────────────────────────────────────────────────
async def suite_backend(page: Page):
    print("\n-- Suite 1: Backend Health --")
    try:
        resp = await page.request.get(f"{BACKEND_URL}/api/health")
        body = await resp.json()
        if resp.status == 200 and body.get("ok"):
            log("GET /api/health -> 200 ok", "PASS", f"engine={body.get('engine')}")
        else:
            log("GET /api/health -> 200 ok", "FAIL", f"status={resp.status} body={body}")
    except Exception as e:
        log("GET /api/health -> 200 ok", "FAIL", str(e))

    try:
        resp = await page.request.post(
            f"{BACKEND_URL}/api/route",
            data=json.dumps({"task": "What is 1+1?"}),
            headers={"Content-Type": "application/json"},
        )
        if resp.status == 200:
            body = await resp.json()
            log("POST /api/route -> 200", "PASS", f"source={body.get('source')} answer={str(body.get('answer',''))[:60]}")
        else:
            text = await resp.text()
            log("POST /api/route -> 200", "FAIL", f"status={resp.status} body={text[:200]}")
    except Exception as e:
        log("POST /api/route -> 200", "FAIL", str(e))

# ─────────────────────────────────────────────────────────────────────────────
# SUITE 2: LANDING PAGE
# ─────────────────────────────────────────────────────────────────────────────
async def suite_landing(page: Page):
    print("\n-- Suite 2: Landing Page --")
    await goto(page)

    # Page loads
    try:
        await expect(page).to_have_title("FrugalRoute — Intelligence Routed. Costs Slashed.", timeout=8000)
        log("Page title correct", "PASS")
    except Exception as e:
        log("Page title correct", "FAIL", str(e))

    # Hero heading visible
    try:
        heading = page.locator("text=Intelligence Routed")
        await expect(heading).to_be_visible(timeout=5000)
        log("Hero heading visible", "PASS")
    except Exception as e:
        log("Hero heading visible", "FAIL", str(e))

    # Sidebar FRUGALROUTE logo visible
    try:
        logo = page.locator("aside").locator("text=FRUGALROUTE")
        await expect(logo).to_be_visible(timeout=5000)
        log("Sidebar logo visible", "PASS")
    except Exception as e:
        log("Sidebar logo visible", "FAIL", str(e))

    # Overview nav item active
    try:
        overview_link = page.locator("a", has_text="Overview")
        await expect(overview_link).to_be_visible(timeout=5000)
        log("Overview nav item visible", "PASS")
    except Exception as e:
        log("Overview nav item visible", "FAIL", str(e))

    # New Chat button in sidebar
    try:
        new_chat_btn = page.locator("a", has_text="New Chat").first
        await expect(new_chat_btn).to_be_visible(timeout=5000)
        log("New Chat button in sidebar", "PASS")
    except Exception as e:
        log("New Chat button in sidebar", "FAIL", str(e))

    # LOCAL NODE ONLINE status
    try:
        status = page.locator("aside").locator("text=LOCAL NODE ONLINE")
        await expect(status).to_be_visible(timeout=5000)
        log("LOCAL NODE ONLINE status visible", "PASS")
    except Exception as e:
        log("LOCAL NODE ONLINE status visible", "FAIL", str(e))

    # Analytics at bottom
    try:
        analytics_link = page.locator("aside").locator("a", has_text="Analytics")
        await expect(analytics_link).to_be_visible(timeout=5000)
        log("Analytics nav item visible", "PASS")
    except Exception as e:
        log("Analytics nav item visible", "FAIL", str(e))

    # Settings at bottom
    try:
        settings_link = page.locator("a", has_text="Settings")
        await expect(settings_link).to_be_visible(timeout=5000)
        log("Settings nav item visible", "PASS")
    except Exception as e:
        log("Settings nav item visible", "FAIL", str(e))

    # Launch New Chat CTA
    try:
        cta = page.locator("text=Launch New Chat")
        await expect(cta).to_be_visible(timeout=5000)
        log("Hero CTA 'Launch New Chat' visible", "PASS")
    except Exception as e:
        log("Hero CTA 'Launch New Chat' visible", "FAIL", str(e))

    # Stats strip
    for stat in ["LOCAL HIT RATE", "P95 LATENCY", "SAVINGS"]:
        try:
            el = page.locator(f"text={stat}")
            await expect(el).to_be_visible(timeout=5000)
            log(f"Footer stat '{stat}' visible", "PASS")
        except Exception as e:
            log(f"Footer stat '{stat}' visible", "FAIL", str(e))

# ─────────────────────────────────────────────────────────────────────────────
# SUITE 3: CHAT PAGE
# ─────────────────────────────────────────────────────────────────────────────
async def suite_chat(page: Page):
    print("\n-- Suite 3: Chat Page --")
    await goto(page, "/chat")

    # Page header
    try:
        heading = page.locator("h1", has_text="New Chat")
        await expect(heading).to_be_visible(timeout=8000)
        log("Chat page header 'New Chat' visible", "PASS")
    except Exception as e:
        log("Chat page header 'New Chat' visible", "FAIL", str(e))

    # Empty state
    try:
        empty = page.locator("text=Start a conversation")
        await expect(empty).to_be_visible(timeout=5000)
        log("Empty state shown on fresh chat", "PASS")
    except Exception as e:
        log("Empty state shown on fresh chat", "FAIL", str(e))

    # Suggestion chips
    try:
        chips = page.locator("button", has_text="Extract the total amount")
        await expect(chips.first).to_be_visible(timeout=5000)
        log("Suggestion chips visible", "PASS")
    except Exception as e:
        log("Suggestion chips visible", "FAIL", str(e))

    # Textarea present and enabled
    try:
        textarea = page.locator("textarea")
        await expect(textarea).to_be_visible(timeout=5000)
        await expect(textarea).to_be_enabled()
        log("Chat textarea visible and enabled", "PASS")
    except Exception as e:
        log("Chat textarea visible and enabled", "FAIL", str(e))

    # Clicking a suggestion fills textarea
    try:
        chip = page.locator("button", has_text="Translate")
        await chip.click()
        textarea = page.locator("textarea")
        value = await textarea.input_value()
        if "Translate" in value or "French" in value:
            log("Clicking suggestion fills textarea", "PASS", f"value={value[:50]}")
        else:
            log("Clicking suggestion fills textarea", "FAIL", f"got='{value}'")
    except Exception as e:
        log("Clicking suggestion fills textarea", "FAIL", str(e))

    # Clear and type a message manually
    try:
        textarea = page.locator("textarea")
        await textarea.fill("")
        await textarea.type("Hello FrugalRoute!")
        value = await textarea.input_value()
        assert "Hello FrugalRoute!" in value
        log("Typing in textarea works", "PASS")
    except Exception as e:
        log("Typing in textarea works", "FAIL", str(e))

    # Send button present
    try:
        send_btn = page.locator("button").filter(has_text="").last
        await expect(send_btn).to_be_visible(timeout=3000)
        log("Send button visible", "PASS")
    except Exception as e:
        log("Send button visible", "FAIL", str(e))

    # Send a message and wait for response
    try:
        textarea = page.locator("textarea")
        await textarea.fill("What is 2 + 2?")
        await textarea.press("Enter")
        # Wait for user bubble
        user_bubble = page.locator("main").locator("text=What is 2 + 2?")
        await expect(user_bubble).to_be_visible(timeout=5000)
        log("User message appears in chat", "PASS")

        # Wait for response (up to 30s for local model)
        assistant_response = page.locator(".glass").last
        await expect(assistant_response).to_be_visible(timeout=35000)
        log("Assistant response received", "PASS")

        # Check for routing badge
        badge = page.locator("text=LOCAL").or_(page.locator("text=REMOTE")).or_(page.locator("text=Semantic Cache"))
        await expect(badge.first).to_be_visible(timeout=5000)
        badge_text = await badge.first.text_content()
        log("Routing badge visible", "PASS", f"badge='{badge_text}'")
    except Exception as e:
        log("End-to-end chat message flow", "FAIL", str(e))

    # Session appears in recent chats after sending
    try:
        # Navigate away and back to trigger sidebar refresh
        await page.goto(f"{BASE_URL}/", wait_until="networkidle", timeout=10000)
        recent_sidebar = page.locator("aside").locator(".group", has_text="What is 2")
        await expect(recent_sidebar.first).to_be_visible(timeout=5000)
        log("Sent message appears in sidebar history", "PASS")
    except Exception as e:
        log("Sent message appears in sidebar history", "FAIL", str(e))

# ─────────────────────────────────────────────────────────────────────────────
# SUITE 4: ANALYTICS PAGE
# ─────────────────────────────────────────────────────────────────────────────
async def suite_analytics(page: Page):
    print("\n-- Suite 4: Analytics Page --")
    await goto(page, "/analytics")

    try:
        heading = page.locator("h1", has_text="Analytics")
        await expect(heading).to_be_visible(timeout=8000)
        log("Analytics h1 visible", "PASS")
    except Exception as e:
        log("Analytics h1 visible", "FAIL", str(e))

    for text in ["Cost Savings", "Routing Distribution", "Recent Queries"]:
        try:
            el = page.locator(f"text={text}")
            await expect(el.first).to_be_visible(timeout=5000)
            log(f"Section '{text}' visible", "PASS")
        except Exception as e:
            log(f"Section '{text}' visible", "FAIL", str(e))

# ─────────────────────────────────────────────────────────────────────────────
# SUITE 5: SETTINGS PAGE
# ─────────────────────────────────────────────────────────────────────────────
async def suite_settings(page: Page):
    print("\n-- Suite 5: Settings Page --")
    await goto(page, "/settings")

    try:
        heading = page.locator("h1", has_text="Settings")
        await expect(heading).to_be_visible(timeout=8000)
        log("Settings h1 visible", "PASS")
    except Exception as e:
        log("Settings h1 visible", "FAIL", str(e))

    for label in ["Ollama", "Confidence", "API"]:
        try:
            el = page.locator(f"text={label}")
            await expect(el.first).to_be_visible(timeout=5000)
            log(f"Settings section '{label}' visible", "PASS")
        except Exception as e:
            log(f"Settings section '{label}' visible", "FAIL", str(e))

# ─────────────────────────────────────────────────────────────────────────────
# SUITE 6: NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
async def suite_navigation(page: Page):
    print("\n-- Suite 6: Navigation --")
    await goto(page)

    # Click Analytics in sidebar
    try:
        await page.locator("aside").locator("a", has_text="Analytics").click()
        await page.wait_for_url(f"{BASE_URL}/analytics", timeout=5000)
        log("Sidebar Analytics link navigates correctly", "PASS")
    except Exception as e:
        log("Sidebar Analytics link navigates correctly", "FAIL", str(e))

    # Click Settings in sidebar
    try:
        await page.locator("a", has_text="Settings").click()
        await page.wait_for_url(f"{BASE_URL}/settings", timeout=5000)
        log("Sidebar Settings link navigates correctly", "PASS")
    except Exception as e:
        log("Sidebar Settings link navigates correctly", "FAIL", str(e))

    # Click Overview
    try:
        await page.locator("a", has_text="Overview").click()
        await page.wait_for_url(f"{BASE_URL}/", timeout=5000)
        log("Sidebar Overview link navigates correctly", "PASS")
    except Exception as e:
        log("Sidebar Overview link navigates correctly", "FAIL", str(e))

    # Click hero CTA
    try:
        await page.locator("text=Launch New Chat").click()
        await page.wait_for_url(f"{BASE_URL}/chat", timeout=5000)
        log("Hero 'Launch New Chat' CTA navigates to /chat", "PASS")
    except Exception as e:
        log("Hero 'Launch New Chat' CTA navigates to /chat", "FAIL", str(e))

    # 404 page
    try:
        await page.goto(f"{BASE_URL}/does-not-exist", wait_until="networkidle", timeout=8000)
        el = page.locator("text=404")
        await expect(el).to_be_visible(timeout=5000)
        log("404 page renders for unknown routes", "PASS")
    except Exception as e:
        log("404 page renders for unknown routes", "FAIL", str(e))

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
async def main():
    print("=" * 60)
    print("  FrugalRoute E2E Test Suite")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await ctx.new_page()

        await suite_backend(page)
        await suite_landing(page)
        await suite_chat(page)
        await suite_analytics(page)
        await suite_settings(page)
        await suite_navigation(page)

        await browser.close()

    # Summary
    passed = sum(1 for r in RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in RESULTS if r["status"] == "FAIL")
    total = len(RESULTS)

    print("\n" + "=" * 60)
    print(f"  Results: {passed}/{total} passed  |  {failed} failed")
    print("=" * 60)
    if failed:
        print("\nFailed tests:")
        for r in RESULTS:
            if r["status"] == "FAIL":
                print(f"  [X] {r['test']}")
                if r["detail"]:
                    print(f"    {r['detail'][:200]}")

    # Save results
    with open("test_results.json", "w") as f:
        json.dump({"passed": passed, "failed": failed, "total": total, "results": RESULTS}, f, indent=2)
    print("\nResults saved to test_results.json")

asyncio.run(main())
