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


# ============================================================
# Task 1: Home Page Validation
# ============================================================
def test_task_1_home_page_validation(page: Page):
    # 1. Verify navigation bar is visible
    nav_bar = page.get_by_role("navigation")
    expect(nav_bar).to_be_visible()

    # 2. Verify products are displayed
    product_cards = page.locator("a.card")
    expect(product_cards.first).to_be_visible(timeout=10000)
    assert product_cards.count() > 0

    # 3. Verify at least one product can be selected/clicked
    first_product_title = product_cards.first.locator(
        '[data-test="product-name"]').inner_text()
    product_cards.first.click()
    expect(page.locator('[data-test="product-name"]')
           ).to_have_text(first_product_title)


# # ============================================================
# # Task 2: Product Search
# # ============================================================
# def test_task_2_product_search_valid(page: Page):
#     search_term = "Pliers"

#     page.locator('[data-test="search-query"]').fill(search_term)
#     page.locator('[data-test="search-submit"]').click()

#     product_names = page.locator('[data-test="product-name"]')
#     expect(product_names.first).to_be_visible(timeout=10000)

#     all_names = product_names.all_inner_texts()
#     assert len(all_names) > 0
#     assert any(search_term.lower() in name.lower() for name in all_names)


# def test_task_2_product_search_non_existent(page: Page):
#     invalid_search = "XYZNonExistentProduct12345"

#     page.locator('[data-test="search-query"]').fill(invalid_search)
#     page.locator('[data-test="search-submit"]').click()

#     no_results_message = page.get_by_text("There are no products found.")
#     expect(no_results_message).to_be_visible(timeout=10000)


# # ============================================================
# # Task 3: Product Details & Add to Cart
# # ============================================================
# def test_task_3_product_details_and_add_to_cart(page: Page):
#     # Wait for products to appear before clicking
#     product_cards = page.locator("a.card")
#     expect(product_cards.first).to_be_visible(timeout=10000)
#     product_cards.first.click()

#     # Verify elements
#     product_name = page.locator('[data-test="product-name"]')
#     product_price = page.locator('[data-test="unit-price"]')
#     product_image = page.locator("img.figure-img")
#     product_description = page.locator('[data-test="product-description"]')
#     add_to_cart_btn = page.locator('[data-test="add-to-cart"]')

#     expect(product_name).to_be_visible()
#     expect(product_price).to_be_visible()
#     expect(product_image).to_be_visible()
#     expect(product_description).to_be_visible()
#     expect(add_to_cart_btn).to_be_enabled()

#     # Add to cart and verify cart counter badge updates
#     add_to_cart_btn.click()
#     cart_quantity_badge = page.locator('[data-test="cart-quantity"]')
#     expect(cart_quantity_badge).to_have_text("1")


# # ============================================================
# # Task 4: Shopping Cart End-to-End
# # ============================================================
# def test_task_4_shopping_cart_flow(page: Page):
#     # 1. Wait for products to load and select first product
#     product_cards = page.locator("a.card")
#     expect(product_cards.first).to_be_visible(timeout=10000)
#     product_cards.first.click()

#     # 2. Capture title and price
#     expected_title = page.locator('[data-test="product-name"]').inner_text()
#     expected_price = page.locator('[data-test="unit-price"]').inner_text()

#     # 3. Add to cart & verify badge
#     page.locator('[data-test="add-to-cart"]').click()
#     expect(page.locator('[data-test="cart-quantity"]')).to_have_text("1")

#     # 4. Open cart
#     page.locator('[data-test="nav-cart"]').click()
#     expect(page).to_have_url(re.compile(r".*checkout"))

#     # 5. Verify product details in cart table
#     cart_item_title = page.locator(".product-title")
#     cart_item_quantity = page.locator('[data-test="product-quantity"]')
#     cart_item_price = page.locator('[data-test="product-price"]')

#     expect(cart_item_title).to_contain_text(expected_title)
#     expect(cart_item_quantity).to_have_value("1")
#     expect(cart_item_price).to_contain_text(expected_price)

#     # 6. Delete item from cart and verify empty state message
#     page.locator("a.btn-danger, [data-test='delete-item']").first.click()

#     empty_cart_msg = page.get_by_text("The cart is empty. Nothing to display.")
#     expect(empty_cart_msg).to_be_visible(timeout=10000)


# # ============================================================
# # Task 5: Login Scenarios
# # ============================================================
# def navigate_to_login_page(page: Page):
#     """Helper to cleanly route to login page."""
#     page.locator('[data-test="nav-sign-in"]').click()
#     expect(page).to_have_url(re.compile(r".*auth/login"))


# def test_login_valid_credentials(page: Page):
#     navigate_to_login_page(page)
#     page.locator(
#         '[data-test="email"]').fill("customer@practicesoftwaretesting.com")
#     page.locator('[data-test="password"]').fill("welcome01")
#     page.locator('[data-test="login-submit"]').click()

#     expect(page).to_have_url(re.compile(r".*account"))
#     expect(page.locator('[data-test="page-title"]')).to_have_text("My account")


# def test_login_invalid_password(page: Page):
#     navigate_to_login_page(page)
#     page.locator(
#         '[data-test="email"]').fill("customer@practicesoftwaretesting.com")
#     page.locator('[data-test="password"]').fill("WrongPassword123!")
#     page.locator('[data-test="login-submit"]').click()

#     error_alert = page.locator('[data-test="login-error"]')
#     expect(error_alert).to_be_visible()
#     expect(error_alert).to_contain_text("Invalid email or password")


# def test_login_invalid_email(page: Page):
#     navigate_to_login_page(page)
#     page.locator('[data-test="email"]').fill("notregistered@example.com")
#     page.locator('[data-test="password"]').fill("welcome01")
#     page.locator('[data-test="login-submit"]').click()

#     error_alert = page.locator('[data-test="login-error"]')
#     expect(error_alert).to_be_visible()
#     expect(error_alert).to_contain_text("Invalid email or password")


# def test_login_empty_credentials(page: Page):
#     navigate_to_login_page(page)
#     page.locator('[data-test="login-submit"]').click()

#     email_error = page.locator('[data-test="email-error"]')
#     password_error = page.locator('[data-test="password-error"]')

#     expect(email_error).to_be_visible()
#     expect(email_error).to_contain_text("Email is required")
#     expect(password_error).to_be_visible()
#     expect(password_error).to_contain_text("Password is required")
