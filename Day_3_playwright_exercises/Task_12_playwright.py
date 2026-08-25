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
    product_a_price = product_price.inner_text().strip()
    print("Product A price:", product_a_price)
    add_to_cart = page.get_by_role("button",name="Add to cart")
    expect(add_to_cart).to_be_visible()
    add_to_cart.click()
    page.wait_for_timeout(2000)
    print("Product A added to cart")

    cart_link = page.locator('a[href="/checkout"]')
    expect(cart_link).to_be_visible()
    cart_link.click()
    page.wait_for_timeout(2000)

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
    product_b_price = product_price.inner_text().strip()
    print("Product B price:", product_b_price)

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

    cart_row_a = page.locator("table tbody tr").filter(has_text=product_a_name)
    expect(cart_row_a).to_be_visible()
    print("Product A verified:",product_a_name)
    quantity_a = page.get_by_role("spinbutton",name=f"Quantity for {product_a_name}")
    expect(quantity_a).to_be_visible()
    assert quantity_a.input_value() == "1", \
        "Product A quantity is not 1"
    print("Product A quantity: 1")

    expect(cart_row_a).to_contain_text(product_a_price)
    print("Product A price verified:",product_a_price)

    product_b_text = page.get_by_text(product_b_name,exact=True)
    expect(product_b_text).to_be_visible()
    print("Product B verified:",product_b_name)

    cart_row_b = product_b_text.locator("xpath=ancestor::tr")
    expect(cart_row_b).to_be_visible()

    quantity_b = page.get_by_role("spinbutton",name=f"Quantity for {product_b_name}")
    expect(quantity_b).to_be_visible()
    quantity_b_value = quantity_b.input_value()
    print("Product B quantity:", quantity_b_value)
    assert quantity_b_value == "1", \
        "Product B quantity is not 1"
    print("Product B quantity verified")

    expect(cart_row_b).to_contain_text(product_b_price)
    print("Product B price verified:",product_b_price)
    print("Both products verified")

    remove_button = cart_row_a.locator("a.btn.btn-danger")
    expect(remove_button).to_be_visible()
    remove_button.click()
    page.wait_for_timeout(3000)
    print("Product A removed:",product_a_name)

    product_b_remaining = page.get_by_text(product_b_name,exact=True)
    expect(product_b_remaining).to_be_visible()
    print("Product B remains:",product_b_name)

    product_a_remaining = page.locator("table tbody tr").filter(has_text=product_a_name)
    expect(product_a_remaining).not_to_be_visible()
    print("Product A removed successfully")
    cart_rows = page.locator("table tbody tr")
    assert cart_rows.count() == 1, \
        "Product B is not the only product remaining"
    print("Only Product B remains")

    page.wait_for_timeout(3000)

    browser.close()
