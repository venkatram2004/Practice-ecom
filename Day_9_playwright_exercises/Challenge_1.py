import pytest
from playwright.sync_api import Page, expect
from user_login import user_auth

def test_strict_mode_and_locator_precision(page: Page):
    user_auth(page)

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    ambiguous_button = page.locator("button.btn_inventory")

    count_ambiguous = ambiguous_button.count()
    print(f"\nLocator matched: {count_ambiguous} elements")
    assert count_ambiguous > 1, "Expected multiple matching buttons"

    with pytest.raises(Exception) as exc_info:
        ambiguous_button.click()

    print(str(exc_info.value))
    assert "strict mode violation" in str(exc_info.value)

    target_product_name = "Sauce Labs Backpack"

    target_product_card = page.locator(".inventory_item").filter(
        has=page.locator(".inventory_item_name", has_text=target_product_name)
    )
    precise_button = target_product_card.locator("button.btn_inventory")

    count_precise = precise_button.count()
    print(f"Locator matched: {count_precise} element")
    assert count_precise == 1, f"Expected 1 element, found {count_precise}"

    precise_button.click()

    expect(precise_button).to_have_text("Remove")

    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

    page.locator(".shopping_cart_link").click()
    expect(page.locator(".inventory_item_name")
           ).to_have_text(target_product_name)
