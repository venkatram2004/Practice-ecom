from playwright.sync_api import expect, sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_timeout(3000)

    page.locator('img[alt="Combination Pliers"]').click()
    page.wait_for_timeout(3000)

    p_name = page.locator('h1[data-test="product-name"]')
    expect(p_name).to_be_visible()
    name_text = p_name.text_content()
    print("Product Name:", name_text)

    p_price = page.locator('span[aria-label="unit-price"]')
    expect(p_price).to_be_visible()
    price_text = p_price.text_content()
    print("Product Price:", price_text)

    expect(page.locator("img.figure-img")).to_be_visible()
    print("Product image is visible")

    p_description = page.locator('p[id="description"]')
    expect(p_description).to_be_visible()
    print(p_description.text_content())

    expect(page.locator('input[data-test="quantity"]')).to_be_visible()
    print("Quantity control is visible")

    add_btn = page.locator('button[data-test="add-to-cart"]')
    expect(add_btn).to_be_visible()
    add_btn.click()
    page.wait_for_timeout(3000)

    page.locator('[data-test="nav-cart"]').click()
    page.wait_for_timeout(3000)

    cart_title = page.locator('[data-test="product-title"]')
    expect(cart_title).to_have_text(name_text)
    print("Cart Product Title:", cart_title.text_content())

    cart_price = page.locator('[data-test="product-price"]')
    expect(cart_price).to_have_text(price_text)
    print("Cart Product Price:", cart_price.text_content())

    page.wait_for_timeout(5000)
    browser.close()
