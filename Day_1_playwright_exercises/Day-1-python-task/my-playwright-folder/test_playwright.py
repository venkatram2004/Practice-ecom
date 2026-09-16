import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"

# 1. Verify Homepage Title and Brand Logo
def test_homepage_title_and_banner(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
    expect(page).to_have_title("Swag Labs")
    expect(page.locator(".login_logo")).to_be_visible()

# 2. Verify Login and Product Catalog
def test_search_and_filter_product(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
    
    # Login as standard user
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    
    # Filter / sort products (low to high)
    sort_dropdown = page.locator("[data-test='product-sort-container']")
    expect(sort_dropdown).to_be_visible(timeout=10000)
    sort_dropdown.select_option("lohi")
    
    # Verify products list is rendered
    items = page.locator(".inventory_item")
    expect(items).to_have_count(6)

# 3. Add Item to Cart and Check Cart Badge
def test_add_tool_to_cart(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
    
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    
    # Add first product to cart
    add_btn = page.locator("[data-test='add-to-cart-sauce-labs-backpack']")
    expect(add_btn).to_be_visible(timeout=10000)
    add_btn.click()
    
    # Assert cart quantity is updated to 1
    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

# 4. Validate Error on Invalid Login
def test_invalid_login_validation(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
    
    page.locator("[data-test='username']").fill("locked_out_user")
    page.locator("[data-test='password']").fill("wrong_password")
    page.locator("[data-test='login-button']").click()
    
    # Assert error banner appears
    error_container = page.locator("[data-test='error']")
    expect(error_container).to_be_visible(timeout=10000)
    expect(error_container).to_contain_text("Username and password do not match")
