"""TC-01 to TC-05: Authentication Tests"""
from playwright.sync_api import sync_playwright, expect
import re, time

BASE = "https://community.mattermost.com"
EMAIL = "nikodimosrodas@gmail.com"
PASSWORD = "Testpassword@1234"

def go_to_login(page):
    page.goto(f"{BASE}/landing#/login")
    page.wait_for_timeout(1000)
    page.click("a[href='https://community.mattermost.com/login']")
    page.wait_for_timeout(2000)
def go_to_signup(page):
    page.goto(f"{BASE}/landing#/signup_user_complete")
    page.wait_for_timeout(1000)
    page.click("a[href='https://community.mattermost.com/signup_user_complete']")
    page.wait_for_timeout(2000)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=400)
    
    # TC-01: Valid login
    print("\n--- TC-01: Valid Login ---")
    context1 = browser.new_context()
    page1 = context1.new_page()
    go_to_login(page1)
    page1.fill("#input_loginId", EMAIL)
    page1.fill("#input_password-input", PASSWORD)
    page1.click("#saveSetting")
    expect(page1).to_have_url(re.compile(r"/channels/"), timeout=15000)
    print("TC-01: PASS")
    context1.close()
    
    # TC-02: Invalid password
    print("\n--- TC-02: Invalid Password ---")
    context2 = browser.new_context()
    page2 = context2.new_page()
    go_to_login(page2)
    page2.fill("#input_loginId", EMAIL)
    page2.fill("#input_password-input", "wrongpass123")
    page2.click("#saveSetting")
    page2.wait_for_timeout(2000)
    expect(page2.locator(".AlertBanner__title")).to_be_visible()
    print("TC-02: PASS")
    context2.close()
    
    # TC-03: Empty fields
    print("\n--- TC-03: Empty Fields ---")
    context3 = browser.new_context()
    page3 = context3.new_page()
    go_to_login(page3)
    page3.fill("#input_loginId", "")
    page3.fill("#input_password-input", "")
    page3.click("#saveSetting")
    page3.wait_for_timeout(2000)
    assert page3.locator(".AlertBanner__title").count() > 0
    print("TC-03: PASS")
    context3.close()
    
    # TC-04: Logout
    print("\n--- TC-04: Logout ---")
    context4 = browser.new_context()
    page4 = context4.new_page()
    go_to_login(page4)
    page4.fill("#input_loginId", EMAIL)
    page4.fill("#input_password-input", PASSWORD)
    page4.click("#saveSetting")
    page4.wait_for_url(re.compile(r"/channels/"), timeout=15000)
    page4.click("#userAccountMenuButton")
    page4.wait_for_timeout(500)
    page4.click("text=Log Out")
    expect(page4).to_have_url(re.compile(r"/login"), timeout=10000)
    print("TC-04: PASS")
    context4.close()
    
    # TC-05: Password minimum length (BVA)
    print("\n--- TC-05: Password Minimum Length (13 chars - should fail) ---")
    context5 = browser.new_context()
    page5 = context5.new_page()
    go_to_signup(page5)
    
    # Fill signup form
    page5.fill("#input_email", f"test{int(time.time())}@example.com")
    page5.fill("#input_name", "testuser123")
    page5.fill("#input_password-input", "Ab1!Ab1!Ab1!?")  # 13 chars
    page5.check("#signup-body-card-form-check-terms-and-privacy")
    page5.click("#saveSetting")
    
    page5.wait_for_timeout(3000)
    
    assert "/signup" in page5.url or "signup" in page5.url
    print("TC-05: PASS - 13-char password rejected")
    context5.close()
    
    browser.close()
    print("\n--- All tests completed ---")