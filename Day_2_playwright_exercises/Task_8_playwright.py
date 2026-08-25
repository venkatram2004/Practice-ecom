from playwright.sync_api import sync_playwright, expect
Base_url="https://practicesoftwaretesting.com/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()

    page.goto(Base_url)
    page.wait_for_timeout(2000)
    print("application opend")

    products=page.locator('a[href^="/product/"]')
    product_count=products.count()
    print("no of products: ",product_count)
    assert product_count>0,\
        "no product are there"
    for i in range (product_count):
        product= products.nth(i)
        if product.locator('[data-test="out-of-stock"]').count() > 0:
            continue
        expect(product).to_be_visible()
        product.click()
        page.wait_for_timeout(2000)
        break
    print("Product selected")

    product_name=page.locator("h1")
    expect(product_name).to_be_visible()
    product_name_text=product_name.inner_text()
    print("product name:",product_name_text)

    product_price = page.locator('[data-test="unit-price"]')
    expect(product_price).to_be_visible()
    product_price_text=product_price.inner_text()
    print("product price:",product_price_text)

    price=float(product_price_text.replace("$",""))
    print("price: ",price)

    quantity=page.get_by_role("spinbutton",name="Quantity")
    expect(quantity).to_be_visible()
    quantity.fill("3")
    print("quantity changed to 3")

    quantity_value=quantity.input_value()
    assert quantity_value=="3",\
        "qunatity not changed to 3"
    print("quantity verified")

    add_to_cart=page.get_by_role("button",name="Add to cart")
    expect(add_to_cart).to_be_visible()
    add_to_cart.click()
    page.wait_for_timeout(2000)
    print("added to cart")

    cart= page.get_by_role("link",name="cart")
    expect(cart).to_be_visible()
    cart.click()
    page.wait_for_timeout(2000)
    print("cart opend")

    cart_row=page.locator("tr").filter(has_text=product_name_text)
    expect(cart_row).to_be_visible()
    cart_quantity=cart_row.locator('[data-test="product-quantity"]')
    expect(cart_quantity).to_be_visible()
    cart_quantity_value=cart_quantity.input_value()
    print("cart quantity: ",cart_quantity_value)
    assert cart_quantity_value=="3",\
        "cart quantity is not 3"
    print("cart quantity verified")

    expected_price=price*3

    line_price=cart_row.locator('[data-test="line-price"]')
    expect(line_price).to_be_visible()
    line_price_text=line_price.inner_text()
    print("price: ",line_price_text)

    actual_total = float(line_price_text.replace("$", ""))
    assert actual_total==expected_price,\
        "expected price is wrong"
    print("total price verified")

    page.wait_for_timeout(3000)

    browser.close()
