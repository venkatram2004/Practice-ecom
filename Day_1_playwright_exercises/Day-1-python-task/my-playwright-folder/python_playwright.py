import re
from playwright.sync_api import Page, expect

BASE_URL = "https://practicesoftwaretesting.com"

def test_homepage_title_and_banner(page: Page):
    page.goto(BASE_URL)
    
    # Assert browser tab title
    expect(page).to_have_title(re.compile("Practice Software Testing", re.IGNORECASE))
    
    # Assert banner/navbar brand exists
    navbar_brand = page.locator("a.navbar-brand")
    expect(navbar_brand).to_be_visible()

def test_search_and_filter_product(page: Page):
    """Search for a specific tool and assert search results."""
    page.goto(BASE_URL)

    search_input = page.locator("[data-test='search-query']")
    search_button = page.locator("[data-test='search-submit']")

    # Search for 'Pliers'
    search_input.fill("Pliers")
    search_button.click()

    # Verify at least one item matches 'Pliers' in card titles
    product_cards = page.locator(".card")
    expect(product_cards.first).to_be_visible()
    
    product_titles = page.locator("[data-test='product-name']")
    expect(product_titles.first).to_contain_text("Pliers")

def test_add_tool_to_cart(page: Page):
    """Open product details, select quantity, and add to cart."""
    page.goto(BASE_URL)

    # Click first available product card
    first_product = page.locator(".card").first
    first_product.click()

    # Wait for product details view
    add_to_cart_btn = page.locator("[data-test='add-to-cart']")
    expect(add_to_cart_btn).to_be_visible()

    # Increase quantity to 2
    quantity_input = page.locator("[data-test='quantity']")
    quantity_input.fill("2")

    # Click Add to Cart
    add_to_cart_btn.click()

    # Verify toast notification alert appears
    toast_alert = page.locator(".toast-body")
    expect(toast_alert).to_be_visible()
    expect(toast_alert).to_contain_text("Product added to shopping cart")

    # Verify cart badge counter updates to 2
    cart_counter = page.locator("[data-test='cart-quantity']")
    expect(cart_counter).to_have_text("2")

def test_invalid_login_validation(page: Page):
    """Validate error toast on entering invalid credentials."""
    page.goto(f"{BASE_URL}/auth/login")

    # Enter wrong user details
    page.locator("[data-test='email']").fill("invalid_user@mail.com")
    page.locator("[data-test='password']").fill("wrongpassword123")
    page.locator("[data-test='login-submit']").click()

    # Assert error banner appears
    error_message = page.locator("[data-test='login-error']")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Invalid email or password")
