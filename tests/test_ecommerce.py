import re
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def setup_page(page: Page):
    """Navigate to home page and wait until DOM is ready."""
    page.goto("https://practicesoftwaretesting.com/",
              wait_until="domcontentloaded")
    expect(page).to_have_title(re.compile(
        "Practice Software Testing", re.IGNORECASE))

# Task 1: Home Page Validation
def test_task_1_home_page_validation(page: Page):
    # 1. Verify navigation bar is visible
    nav_bar = page.get_by_role("navigation")
    expect(nav_bar).to_be_visible()

    product_cards = page.locator("a.card")
    expect(product_cards.first).to_be_visible(timeout=10000)
    assert product_cards.count() > 0

    first_product_title = product_cards.first.locator(
        '[data-test="product-name"]').inner_text()
    product_cards.first.click()
    expect(page.locator('[data-test="product-name"]')
           ).to_have_text(first_product_title)



# Task 2: Product search
def test_task_2_search_valid_product(page: Page):
    # Type 'Pliers' and click search
    page.locator('[data-test="search-query"]').fill("Pliers")
    page.locator('[data-test="search-submit"]').click()

    # Check that search results appear
    first_result = page.locator('[data-test="product-name"]').first
    expect(first_result).to_be_visible()
    expect(first_result).to_contain_text("Pliers")


def test_task_2_search_invalid_product(page: Page):
    # Search for an item that does not exist
    page.locator('[data-test="search-query"]').fill("InvalidItem999")
    page.locator('[data-test="search-submit"]').click()

    # Check for the empty state message
    empty_message = page.get_by_text("There are no products found.")
    expect(empty_message).to_be_visible()



# Task 3: Product Details & Add to Cart

def test_task_3_product_details(page: Page):
    # 1. Open first product
    page.locator("a.card").first.click()

    # 2. Verify all product details exist
    expect(page.locator('[data-test="product-name"]')).to_be_visible()
    expect(page.locator('[data-test="unit-price"]')).to_be_visible()
    expect(page.locator('img.figure-img')).to_be_visible()
    expect(page.locator('[data-test="product-description"]')).to_be_visible()

    # 3. Click 'Add to cart' and check badge count
    page.locator('[data-test="add-to-cart"]').click()
    expect(page.locator('[data-test="cart-quantity"]')).to_have_text("1")



# Task 4: Shopping Cart Flow

def test_task_4_shopping_cart(page: Page):
    # 1. Add product to cart
    page.locator("a.card").first.click()
    page.locator('[data-test="add-to-cart"]').click()

    # 2. Go to shopping cart
    page.locator('[data-test="nav-cart"]').click()

    # 3. Check product details in the cart
    expect(page.locator('.product-title')).to_be_visible()
    expect(page.locator('[data-test="product-quantity"]')).to_have_value("1")

    # 4. Remove item and check empty message
    page.locator('a.btn-danger').click()
    expect(page.get_by_text("The cart is empty. Nothing to display.")).to_be_visible()



