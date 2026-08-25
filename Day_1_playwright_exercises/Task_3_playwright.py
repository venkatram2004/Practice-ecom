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
    assert product_count > 0, \
        "No products are available"
    first_product = products.first
    expect(first_product).to_be_visible()
    first_product.click()
    page.wait_for_timeout(2000)
    print("Product selected")


    product_name = page.locator("h1")
    expect(product_name).to_be_visible()
    product_name_text = product_name.inner_text()
    print("Product name:", product_name_text)
    assert product_name_text.strip() != "", \
        "Product name is empty"
    print("Product name verified")


    product_price = page.locator("text=/\\$[0-9]+\\.[0-9]+/").first
    expect(product_price).to_be_visible()
    product_price_text = product_price.inner_text()
    print("Product price:", product_price_text)
    assert "$" in product_price_text, \
        "Product price is not displayed"
    print("Product price verified")


    product_image = page.locator("figure img").first
    expect(product_image).to_be_visible()
    image_source = product_image.get_attribute("src")
    assert image_source, \
        "Product image is not available"
    print("Product image verified")


    description = page.locator("p").filter(has_text="combination pliers").first
    expect(description).to_be_visible()
    description_text = description.inner_text()
    print("Product description:")
    print(description_text)
    assert description_text.strip() != "", \
        "Product description is empty"
    print("Product description verified")


    add_to_cart = page.get_by_role("button",name="Add to cart")
    expect(add_to_cart).to_be_visible()
    print("Add to cart button is visible")


    add_to_cart.click()
    page.wait_for_timeout(2000)
    print("Product added to cart")


    cart = page.get_by_role("link",name="Cart")
    expect(cart).to_be_visible()
    cart.click()
    page.wait_for_timeout(2000)
    print("Cart opened")


    cart_product = page.get_by_text(product_name_text,exact=True)
    expect(cart_product).to_be_visible()
    print("Product found in cart:",product_name_text)

    page.wait_for_timeout(5000)

    browser.close()
