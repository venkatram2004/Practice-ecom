from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(BASE_URL)
    page.wait_for_timeout(2000)
    print("Application opened")

    products = page.locator("a[href^='/product/']")
    product_count = products.count()
    print("Number of products:", product_count)
    assert product_count > 1, \
        "Less than 2 products are available"
    for i in range(product_count):
        product = products.nth(i)
        if product.locator('[data-test="out-of-stock"]').count() > 0:
            continue
        expect(product).to_be_visible()
        product_a_url = product.get_attribute("href")
        product.click()
        page.wait_for_timeout(2000)
        break
    print("Product A selected")

    product_name = page.locator("h1")
    expect(product_name).to_be_visible()
    product_a_name = product_name.inner_text().strip()
    print("Product A:", product_a_name)
    product_price = page.locator("text=/\\$[0-9]+\\.[0-9]+/").first
    expect(product_price).to_be_visible()
    product_a_price_text = product_price.inner_text().strip()
    print("Product A price:", product_a_price_text)
    product_a_price = float(product_a_price_text.replace("$", ""))
    add_to_cart = page.get_by_role("button",name="Add to cart")
    expect(add_to_cart).to_be_visible()
    add_to_cart.click()
    page.wait_for_timeout(2000)
    print("Product A added to cart")

    cart_link = page.locator('a[href="/checkout"]')
    expect(cart_link).to_be_visible()
    cart_link.click()
    page.wait_for_timeout(1000)
    continue_shopping = page.get_by_role("button",name="Continue Shopping")
    expect(continue_shopping).to_be_visible()
    continue_shopping.click()
    page.wait_for_timeout(2000)
    print("Returned to product listing")

    products = page.locator("a[href^='/product/']")
    product_count = products.count()
    product_b_selected = False
    for i in range(product_count):
        product = products.nth(i)
        if product.locator('[data-test="out-of-stock"]').count() > 0:
            continue
        product_url = product.get_attribute("href")
        if product_url == product_a_url:
            continue
        expect(product).to_be_visible()
        product.click()
        page.wait_for_timeout(2000)
        product_b_selected = True
        break
    assert product_b_selected, \
        "Could not find Product B"
    print("Product B selected")

    product_name = page.locator("h1")
    expect(product_name).to_be_visible()
    product_b_name = product_name.inner_text().strip()
    print("Product B:", product_b_name)
    product_price = page.locator("text=/\\$[0-9]+\\.[0-9]+/").first
    expect(product_price).to_be_visible()
    product_b_price_text = product_price.inner_text().strip()
    print("Product B price:", product_b_price_text)
    product_b_price = float(product_b_price_text.replace("$", ""))

    add_to_cart = page.get_by_role("button",name="Add to cart")
    expect(add_to_cart).to_be_visible()
    add_to_cart.click()
    page.wait_for_timeout(4000)
    print("Product B added to cart")

    cart_link = page.locator('a[href="/checkout"]')
    expect(cart_link).to_be_visible()
    cart_link.click()
    page.wait_for_timeout(2000)
    print("Cart opened")

    quantity_a = page.get_by_role("spinbutton",name=f"Quantity for {product_a_name}")
    expect(quantity_a).to_be_visible()
    quantity_a_value = int(quantity_a.input_value())
    print("Product A quantity:", quantity_a_value)

    quantity_b = page.get_by_role("spinbutton",name=f"Quantity for {product_b_name}")
    expect(quantity_b).to_be_visible()
    quantity_b_value = int(quantity_b.input_value())
    print("Product B quantity:", quantity_b_value)

    expected_total = (product_a_price * quantity_a_value + product_b_price * quantity_b_value)
    print("Expected total:",f"${expected_total:.2f}")

    total_text = page.locator("text=/\\$[0-9]+\\.[0-9]+/").last
    expect(total_text).to_be_visible()
    actual_total_text = total_text.inner_text().strip()
    actual_total = float(actual_total_text.replace("$", ""))
    print("Actual cart total:",f"${actual_total:.2f}")
    assert round(actual_total, 2) == round(expected_total, 2), \
        "Cart total calculation is incorrect"
    print("Initial cart total verified")

    quantity_a.fill("2")
    quantity_a.press("Enter")
    page.wait_for_timeout(3000)
    print("Product A quantity changed to 2")

    quantity_a_value = int(quantity_a.input_value())
    print("Updated Product A quantity:",quantity_a_value)
    assert quantity_a_value == 2, \
        "Product A quantity was not updated"

    expected_total_after_quantity_change = (product_a_price * quantity_a_value + product_b_price * quantity_b_value)
    print("Expected total after quantity change:",f"${expected_total_after_quantity_change:.2f}")

    total_text = page.locator("text=/\\$[0-9]+\\.[0-9]+/").last
    expect(total_text).to_be_visible()
    actual_total_text = total_text.inner_text().strip()
    actual_total_after_quantity_change = float(actual_total_text.replace("$", ""))
    print("Actual total after quantity change:",f"${actual_total_after_quantity_change:.2f}")

    assert round(actual_total_after_quantity_change, 2) == round(expected_total_after_quantity_change, 2), \
        "Cart total was not updated correctly"
    print("Updated cart total verified")

    page.wait_for_timeout(3000)

    browser.close()
