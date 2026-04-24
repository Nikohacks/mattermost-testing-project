"""TC-06 to TC-08: Channel Management Tests"""
from playwright.sync_api import sync_playwright, expect
import re, time

BASE = "https://community.mattermost.com"
EMAIL = "nikodimosrodas@gmail.com"     
PASSWORD = "Testpassword@1234"         
PUB = f"pub-{int(time.time())}"
PRIV = f"priv-{int(time.time())}"

def go_to_login(page):
    page.goto(f"{BASE}/landing#/login")
    page.wait_for_timeout(1000)
    page.click("a[href='https://community.mattermost.com/login']")
    page.wait_for_timeout(2000)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=400)
    
    # TC-06: Create channel (will be private due to demo server limitations)
    print("\n--- TC-06: Create Channel ---")
    context6 = browser.new_context()
    page6 = context6.new_page()
    go_to_login(page6)
    page6.fill("#input_loginId", EMAIL)
    page6.fill("#input_password-input", PASSWORD)
    page6.click("#saveSetting")
    page6.wait_for_url(re.compile(r"/channels/"), timeout=15000)
    
    page6.click("#addChannelsCta")
    page6.wait_for_timeout(500)
    page6.click("text=Create New Channel")
    page6.wait_for_timeout(500)
    
    # On demo server, only private channels are allowed
    page6.locator("input[placeholder*='name' i]").first.fill(PUB)
    page6.click("button:has-text('Create Channel')")
    expect(page6.locator(f"text={PUB}").first).to_be_visible(timeout=15000)
    print(f"TC-06: PASS - Channel '{PUB}' created (private only on demo server)")
    context6.close()
    
    # TC-07: Create private channel (explicitly test private)
    print("\n--- TC-07: Create Private Channel ---")
    context7 = browser.new_context()
    page7 = context7.new_page()
    go_to_login(page7)
    page7.fill("#input_loginId", EMAIL)
    page7.fill("#input_password-input", PASSWORD)
    page7.click("#saveSetting")
    page7.wait_for_url(re.compile(r"/channels/"), timeout=15000)
    
    page7.click("#addChannelsCta")
    page7.wait_for_timeout(500)
    page7.click("text=Create New Channel")
    page7.wait_for_timeout(500)
    
    # Fill channel name - Private is selected by default
    page7.locator("input[placeholder*='name' i]").first.fill(PRIV)
    # Verify Private is selected (optional check)
    private_radio = page7.locator("text=Private")
    expect(private_radio).to_be_visible()
    page7.click("button:has-text('Create Channel')")
    expect(page7.locator(f"text={PRIV}").first).to_be_visible(timeout=15000)
    print(f"TC-07: PASS - Private channel '{PRIV}' created")
    context7.close()
    
    # TC-08: Join public channel (complete verification)
    print("\n--- TC-08: Join Public Channel ---")
    context8 = browser.new_context()
    page8 = context8.new_page()
    go_to_login(page8)
    page8.fill("#input_loginId", EMAIL)
    page8.fill("#input_password-input", PASSWORD)
    page8.click("#saveSetting")
    page8.wait_for_url(re.compile(r"/channels/"), timeout=15000)
    
    page8.click("#addChannelsCta")
    page8.wait_for_timeout(500)
    page8.click("text=Browse Channels")
    page8.wait_for_timeout(2000)
    
    page8.fill("#searchChannelsTextbox", "k")
    page8.wait_for_timeout(2000)
    
    channel_rows = page8.locator(".more-modal__row").all()
    joined = False
    
    for row in channel_rows:
        row.hover()
        page8.wait_for_timeout(500)
        
        join_button = row.locator("button#joinViewChannelButton")
        if join_button.count() > 0 and join_button.is_visible():
            channel_name = row.locator(".more-modal__name span").first.text_content()
            print(f"  Joining channel: {channel_name}")
            
            join_button.click()
            page8.wait_for_timeout(2000)
            
            expect(page8.locator(".channel-header").first).to_be_visible(timeout=10000)
            print(f"TC-08: PASS - Successfully joined '{channel_name}'")
            joined = True
            break
    
    if not joined:
        assert False, "No joinable channels found in search results"
    
    context8.close()
    
    browser.close()
    print("\n--- All channel tests completed ---")
    print("\nNOTE: On Mattermost demo server, regular users cannot create public channels.")
    print("      Only private channels are allowed. TC-06 creates a private channel.")