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



