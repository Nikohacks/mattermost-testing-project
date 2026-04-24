"""TC-09 to TC-12: Messaging Tests"""
from playwright.sync_api import sync_playwright, expect
import re, time

BASE = "https://community.mattermost.com"
EMAIL = "nikodimosrodas@gmail.com"      # ← UPDATE
PASSWORD = "Testpassword@1234"            # ← UPDATE
USER2 = "@nikodimos17"              # ← UPDATE (for DM)

def go_to_login(page):
    """Go from landing page to actual login page"""
    page.goto(f"{BASE}/landing#/login")
    page.wait_for_timeout(1000)
    page.click("a[href='https://community.mattermost.com/login']")
    page.wait_for_timeout(2000)

def login(page):
    """Login with credentials"""
    go_to_login(page)
    page.fill("#input_loginId", EMAIL)
    page.fill("#input_password-input", PASSWORD)
    page.click("#saveSetting")
    page.wait_for_url(re.compile(r"/channels/"), timeout=15000)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=400)
    
    # TC-09: Send message
    print("\n--- TC-09: Send Message ---")
    context9 = browser.new_context()
    page9 = context9.new_page()
    login(page9)
    
    page9.goto(f"{BASE}/core/channels/ceilingtest-01")
    page9.wait_for_selector("#post_textbox", timeout=15000)
    m9 = f"TC09 {int(time.time())}"
    page9.fill("#post_textbox", m9)
    page9.keyboard.press("Enter")
    expect(page9.locator(f"text={m9}").first).to_be_visible(timeout=10000)
    print("TC-09: PASS - Message sent and visible")
    context9.close()
    
    # TC-10: Edit message (keyboard shortcut method)
    print("\n--- TC-10: Edit Message ---")
    context10 = browser.new_context()
    page10 = context10.new_page()
    login(page10)
    
    page10.goto(f"{BASE}/core/channels/ceilingtest-01")
    page10.wait_for_selector("#post_textbox", timeout=15000)
    m10 = f"TC10 {int(time.time())}"
    page10.fill("#post_textbox", m10)
    page10.keyboard.press("Enter")
    
    # Wait for message
    page10.wait_for_timeout(2000)
    
    # Click on the message to focus it
    message_text = page10.locator(f".post-message__text:has-text('{m10}')").first
    expect(message_text).to_be_visible(timeout=10000)
    message_text.click()
    page10.wait_for_timeout(500)
    
    # Press Up arrow to select the message (Mattermost shortcut)
    page10.keyboard.press("ArrowUp")
    page10.wait_for_timeout(500)
    
    # Press E to edit (Mattermost keyboard shortcut)
    page10.keyboard.press("e")
    page10.wait_for_timeout(500)
    
    # Edit the content
    page10.keyboard.press("Control+A")
    page10.keyboard.type("EDITED")
    page10.keyboard.press("Enter")
    
    # Wait for save
    page10.wait_for_timeout(3000)
    
    # Verify edited message
    edited_message = page10.locator(".post-message__text:has-text('EDITED')").first
    expect(edited_message).to_be_visible(timeout=10000)
    
    # Verify edited indicator using the correct selector
    edited_indicator = page10.locator("span.post-edited__indicator")
    expect(edited_indicator.first).to_be_visible(timeout=5000)
    print("TC-10: PASS - Message edited with indicator")
    
    context10.close()
    
        # TC-11: Delete message
    print("\n--- TC-11: Delete Message ---")
    context11 = browser.new_context()
    page11 = context11.new_page()
    login(page11)
    
    page11.goto(f"{BASE}/core/channels/ceilingtest-01")
    page11.wait_for_selector("#post_textbox", timeout=15000)
    m11 = f"TC11 {int(time.time())}"
    page11.fill("#post_textbox", m11)
    page11.keyboard.press("Enter")
    
    # Wait for message
    page11.wait_for_timeout(2000)
    
    # Find the post by the message text in post-message__text
    message_post = page11.locator(f".post-message__text:has-text('{m11}')").first
    expect(message_post).to_be_visible(timeout=10000)
    
    # Hover over the post__body
    post_body = message_post.locator("xpath=ancestor::div[@class='post__body']")
    post_body.first.hover()
    page11.wait_for_timeout(1000)
    
    # Use JavaScript to force click the three-dot menu
    page11.evaluate(f"""
        const post = document.querySelector('[data-testid="postContent"]');
        if (post) {{
            const menuButton = post.querySelector('button[data-testid^="PostDotMenu-Button"]');
            if (menuButton) {{
                menuButton.click();
            }}
        }}
    """)
    page11.wait_for_timeout(500)
    
    # Click Delete from dropdown using exact selector
    delete_option = page11.locator('li:has-text("Delete")').first
    expect(delete_option).to_be_visible(timeout=5000)
    delete_option.click()
    page11.wait_for_timeout(500)
    
    # Confirm deletion
    page11.click("button:has-text('Delete')")
    page11.wait_for_timeout(3000)
    
    # Verify message is gone
    assert page11.locator(f".post-message__text:has-text('{m11}')").count() == 0
    print("TC-11: PASS - Message deleted with confirmation")
    context11.close()
    
    # TC-12: Direct message
    print("\n--- TC-12: Direct Message ---")
    context12 = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page12 = context12.new_page()
    login(page12)
    page12.goto(f"{BASE}/core/channels/ceilingtest-01")
    page12.wait_for_selector("#post_textbox", timeout=15000)
    
    page12.click("#newDirectMessageButton")
    page12.wait_for_timeout(500)
    
    search_input = page12.locator("input[aria-label='Search for people']")
    expect(search_input).to_be_visible(timeout=5000)
    search_input.fill(USER2)
    page12.wait_for_timeout(2000)
    
    user_row = page12.locator(".more-modal__row").first
    expect(user_row).to_be_visible(timeout=5000)
    user_row.click()
    page12.wait_for_timeout(500)
    
    go_button = page12.locator("#saveItems, button:has-text('Go')")
    expect(go_button).to_be_visible(timeout=5000)
    go_button.click()
    page12.wait_for_timeout(3000)
    
    page12.wait_for_selector("#post_textbox", timeout=15000)
    
    m12 = f"TC12 DM {int(time.time())}"
    page12.fill("#post_textbox", m12)
    page12.keyboard.press("Enter")
    page12.wait_for_timeout(2000)
    
    expect(page12.locator(f".post-message__text:has-text('{m12}')").first).to_be_visible(timeout=10000)
    print("TC-12: PASS - Direct message delivered")
    context12.close()    print("\n--- All messaging tests completed ---")
