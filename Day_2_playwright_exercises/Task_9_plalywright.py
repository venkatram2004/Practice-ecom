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
    print("first available product: ",product_name_text)
    assert "/product/" in page.url,\
        "product details page did not opened"
    print("product page opened successfully")

    page.wait_for_timeout(3000)

    browser.close()
