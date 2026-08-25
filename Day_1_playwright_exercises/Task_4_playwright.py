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
    assert product_count > 0, \
        "No products are available"
    for i in range (product_count):
        product= products.nth(i)
        if product.locator('[data-test="out-of-stock"]').count() > 0:
            continue
        expect(product).to_be_visible()
        product.click()
        page.wait_for_timeout(2000)
        break
    print("Product selected")


    product_name = page.locator("h1")
    expect(product_name).to_be_visible()
    product_name_text = product_name.inner_text()
    print("Product name:",product_name_text)


    product_price = page.locator("text=/\\$[0-9]+\\.[0-9]+/").first
    expect(product_price).to_be_visible()
    product_price_text = product_price.inner_text()
    print("Product price:",product_price_text)


    add_to_cart = page.get_by_role("button",name="Add to cart")
    expect(add_to_cart).to_be_visible()
    add_to_cart.click()
    page.wait_for_timeout(2000)
    print("Product added to cart")


    cart_link = page.get_by_role("link",name="Cart")
    expect(cart_link).to_be_visible()
    cart_link.click()
    page.wait_for_timeout(2000)
    print("Cart opened")


    cart_product = page.get_by_text(product_name_text,exact=True)
    expect(cart_product).to_be_visible()
    print("Product verified in cart:",product_name_text)


    quantity = page.get_by_role("spinbutton",name=f"Quantity for {product_name_text}")
    expect(quantity).to_be_visible()
    quantity_value = quantity.input_value()
    print("Quantity:",quantity_value)
    assert quantity_value == "1", \
        "Product quantity is not 1"
    print("Quantity verified")


    cart_price = page.get_by_text(product_price_text,exact=False).first
    expect(cart_price).to_be_visible()
    print("Price verified:",product_price_text)


    cart_row = page.locator("tr").filter(has_text=product_name_text)
    expect(cart_row).to_be_visible()
    remove_button = cart_row.locator("a.btn.btn-danger")
    expect(remove_button).to_be_visible()
    remove_button.click()
    page.wait_for_timeout(3000)
    print("Remove button clicked")



    cart_rows = page.locator("table tbody tr")
    cart_row_count = cart_rows.count()
    print("Number of cart rows after removal:",cart_row_count)
    assert cart_row_count == 0, \
        "Product is still present in the cart"
    print("Cart is empty")

    page.wait_for_timeout(5000)

    browser.close()
