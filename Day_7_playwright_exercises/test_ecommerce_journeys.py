import time
import pytest
import pytest_asyncio
from playwright.async_api import Page, async_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com"


@pytest_asyncio.fixture
async def async_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        yield page

        await context.close()
        await browser.close()

# t1
@pytest.mark.asyncio
async def test_01_product_search(async_page: Page):
    target_product = "Combination Pliers"

    await async_page.goto(BASE_URL, wait_until="domcontentloaded")

    search_box = async_page.locator(
        'input[id="search-query"], input[data-test="search-query"]'
    )
    await expect(search_box).to_be_visible(timeout=15000)
    await search_box.fill(target_product)

    search_button = async_page.locator('button[data-test="search-submit"]')
    await search_button.click()

    first_result = async_page.locator('h5[data-test="product-name"]').first
    await expect(first_result).to_be_visible(timeout=15000)
    await expect(first_result).to_have_text(target_product)


# t2
@pytest.mark.asyncio
async def test_02_product_details(async_page: Page):
    await async_page.goto(BASE_URL, wait_until="domcontentloaded")

    first_product_card = async_page.locator("a.card").first
    await expect(first_product_card).to_be_visible(timeout=15000)
    await first_product_card.click()

    product_name = async_page.locator('h1[data-test="product-name"]')
    await expect(product_name).to_be_visible(timeout=15000)

    product_price = async_page.locator('span[aria-label="unit-price"]')
    await expect(product_price).to_be_visible()

    product_desc = async_page.locator('p[id="description"]')
    await expect(product_desc).to_be_visible()

    add_to_cart_btn = async_page.locator('button[data-test="add-to-cart"]')
    await expect(add_to_cart_btn).to_be_visible()


# t3
@pytest.mark.asyncio
async def test_03_category_navigation(async_page: Page):
    await async_page.goto(BASE_URL, wait_until="domcontentloaded")

    categories_dropdown = async_page.get_by_role("button", name="Categories")
    await expect(categories_dropdown).to_be_visible(timeout=15000)
    await categories_dropdown.click()

    hand_tools_link = async_page.locator('a[data-test="nav-hand-tools"]')
    await expect(hand_tools_link).to_be_visible()
    await hand_tools_link.click()

    category_header = async_page.locator("h2")
    await expect(category_header).to_be_visible(timeout=15000)
    await expect(category_header).to_contain_text("Hand Tools")

    product_cards = async_page.locator("a.card")
    await expect(product_cards.first).to_be_visible(timeout=15000)


#t4
@pytest.mark.asyncio
async def test_04_user_registration(async_page: Page):
    await async_page.goto(
        f"{BASE_URL}/auth/register", wait_until="domcontentloaded"
    )

    timestamp = int(time.time() * 1000)
    unique_email = f"user_{timestamp}@testmail.com"
    secure_password = f"P@ssw0rd_{timestamp}!#Xz"

    first_name = async_page.locator(
        'input[data-test="first-name"], input#first_name'
    )
    await expect(first_name).to_be_visible(timeout=15000)
    await first_name.fill("venkatram")

    await async_page.locator(
        'input[data-test="last-name"], input#last_name'
    ).fill("Doe")
    await async_page.locator('input[data-test="dob"], input#dob').fill(
        "2004-02-2004"
    )
    await async_page.locator(
        'select[data-test="country"], select#country'
    ).select_option("IN")

    await async_page.locator(
        'input[data-test="postcode"], input[data-test="postal-code"], input#postal_code, input#postcode'
    ).fill("600001")
    await async_page.locator(
        'input[placeholder*="42"], input[data-test="house-number"], input[data-test="street-number"], input#house_number'
    ).fill("42")

    await async_page.locator(
        'input[data-test="address"], input[data-test="street"], input#street, input#address'
    ).fill("123 Main Street")
    await async_page.locator('input[data-test="city"], input#city').fill(
        "Chennai"
    )
    await async_page.locator('input[data-test="state"], input#state').fill("TN")
    await async_page.locator('input[data-test="phone"], input#phone').fill(
        "9876543210"
    )
    await async_page.locator('input[data-test="email"], input#email').fill(
        unique_email
    )
    await async_page.locator('input[data-test="password"], input#password').fill(
        secure_password
    )

    register_btn = async_page.locator('button[data-test="register-submit"]')
    await expect(register_btn).to_be_enabled()
    await register_btn.click()


    login_heading = async_page.locator('h3:has-text("Login")')
    await expect(login_heading).to_be_visible(timeout=15000)
