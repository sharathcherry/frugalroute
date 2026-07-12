from playwright.sync_api import sync_playwright

def run_tests():
    with sync_playwright() as p:
        # Launch Chromium in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to http://127.0.0.1:8000/chat...")
        page.goto("http://127.0.0.1:8000/chat")
        
        # Test 1: The 'mic' button (should trigger an alert)
        print("Testing dummy buttons (mic)...")
        
        alert_text = []
        page.on("dialog", lambda dialog: (alert_text.append(dialog.message), dialog.accept()))
        
        # Click the mic button (it's the button before the chat-send button)
        # Using a selector for the mic button based on the icon text "mic"
        mic_btn = page.locator("button:has-text('mic')").first
        mic_btn.click()
        
        if len(alert_text) > 0 and "coming soon" in alert_text[0].lower():
            print("PASS: Dummy button successfully showed 'Coming Soon' alert.")
        else:
            print("FAIL: Dummy button did not trigger the expected alert.")

        # Test 2: The chat send flow
        print("Testing chat send flow...")
        chat_input = page.locator("#chat-input")
        chat_input.fill("What is the capital of France?")
        
        chat_send = page.locator("#chat-send")
        chat_send.click()
        
        # Check if user bubble appeared
        user_bubble = page.locator(".user-bubble-accent").last
        if user_bubble.is_visible():
            print("PASS: User bubble appeared in chat history.")
        else:
            print("FAIL: User bubble not found.")
            
        # Wait for AI response (the loading bubble should disappear and the answer should appear)
        print("Waiting for AI response (this might take a few seconds)...")
        # We wait for the AI badge to appear
        # The badge contains "Local" or "Remote" or "Cache"
        page.wait_for_selector(".ai-bubble-accent p:not(.animate-pulse)", timeout=15000)
        
        ai_response = page.locator(".ai-bubble-accent").last.inner_text()
        print("AI Response received:")
        print("-" * 20)
        print(ai_response)
        print("-" * 20)
        print("PASS: AI response successfully loaded in the UI.")
        
        browser.close()

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"Test failed with error: {e}")
