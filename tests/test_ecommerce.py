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

