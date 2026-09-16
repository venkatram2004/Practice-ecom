import re
from playwright.sync_api import Page, expect

BASE_URL = "https://practicesoftwaretesting.com"

# Set global timeout for elements to 10 seconds in CI
def test_homepage_title_and_banner(page: Page):
    page.goto(BASE_URL, wait_until="networkidle", timeout=60000)
    expect(page).to_have_title(re.compile("Practice Software Testing", re.IGNORECASE))
    expect(page.locator("a.navbar-brand")).to_be_visible()

def test_search_and_filter_product(page: Page):
    page.goto(BASE_URL, wait_until="networkidle", timeout=60000)
    
    search_input = page.locator("[data-test='search-query']")
    search_button = page.locator("[data-test='search-submit']")

    expect(search_input).to_be_visible()
    search_input.fill("Pliers")
    search_button.click()

    # Wait for filtered cards to reload
    page.wait_for_timeout(2000)
    product_cards = page.locator(".card")
    expect(product_cards.first).to_be_visible(timeout=10000)

def test_add_tool_to_cart(page: Page):
    page.goto(BASE_URL, wait_until="networkidle", timeout=60000)
    
    # Wait for products to show up and click
    first_product = page.locator(".card").first
    expect(first_product).to_be_visible(timeout=10000)
    first_product.click()

    add_to_cart_btn = page.locator("[data-test='add-to-cart']")
    expect(add_to_cart_btn).to_be_visible(timeout=10000)
    add_to_cart_btn.click()

    # Verify toast or cart counter
    expect(page.locator("[data-test='cart-quantity']")).to_have_text("1", timeout=10000)

def test_invalid_login_validation(page: Page):
    page.goto(f"{BASE_URL}/auth/login", wait_until="networkidle", timeout=60000)
    
    page.locator("[data-test='email']").fill("invalid_user@mail.com")
    page.locator("[data-test='password']").fill("wrongpassword123")
    page.locator("[data-test='login-submit']").click()

    error_message = page.locator("[data-test='login-error']")
    expect(error_message).to_be_visible(timeout=10000)
