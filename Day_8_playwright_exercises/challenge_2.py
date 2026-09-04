import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"


def test_browser_history_journey(page: Page):
    page.goto(BASE_URL)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

    product_1_link = page.locator(".inventory_item_name").nth(0)
    product_1_name = product_1_link.inner_text()

    product_1_link.click()

    expect(page).to_have_url(f"{BASE_URL}/inventory-item.html?id=4")
    expect(page.locator(".inventory_details_name")
           ).to_have_text(product_1_name)

    page.locator("#back-to-products").click()
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")

    product_2_link = page.locator(".inventory_item_name").nth(1)
    product_2_name = product_2_link.inner_text()

    product_2_link.click()

    expect(page).to_have_url(f"{BASE_URL}/inventory-item.html?id=0")
    expect(page.locator(".inventory_details_name")
           ).to_have_text(product_2_name)

    page.locator(".shopping_cart_link").click()

    expect(page).to_have_url(f"{BASE_URL}/cart.html")
    expect(page.locator(".title")).to_have_text("Your Cart")

    page.reload()

    expect(page).to_have_url(f"{BASE_URL}/cart.html")
    expect(page.locator(".title")).to_have_text("Your Cart")

    page.go_back()
    expect(page).to_have_url(f"{BASE_URL}/inventory-item.html?id=0")
    expect(page.locator(".inventory_details_name")
           ).to_have_text(product_2_name)

    page.go_back()
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

    page.go_back()
    expect(page).to_have_url(f"{BASE_URL}/inventory-item.html?id=4")
    expect(page.locator(".inventory_details_name")
           ).to_have_text(product_1_name)

    page.go_back()
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

    page.go_forward()
    expect(page).to_have_url(f"{BASE_URL}/inventory-item.html?id=4")
    expect(page.locator(".inventory_details_name")
           ).to_have_text(product_1_name)

    page.go_forward()
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

    page.go_forward()
    expect(page).to_have_url(f"{BASE_URL}/inventory-item.html?id=0")
    expect(page.locator(".inventory_details_name")
           ).to_have_text(product_2_name)

    page.go_forward()
    expect(page).to_have_url(f"{BASE_URL}/cart.html")
    expect(page.locator(".title")).to_have_text("Your Cart")
