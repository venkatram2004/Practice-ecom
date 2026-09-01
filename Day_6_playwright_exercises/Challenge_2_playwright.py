import asyncio
from playwright.async_api import expect
from playwright.async_api import async_playwright

TEST_PRODUCTS = [
    "Combination Pliers",
    "Hammer",
    "Bolt Cutters",
    "Screwdriver",
    "Pliers",
]
async def search_single_product(browser, product_name: str):
    page = await browser.new_page()
    try:
        await page.goto("https://practicesoftwaretesting.com/")

        search_inp = page.locator('input[id="search-query"]')
        await expect(search_inp).to_be_visible(timeout=10000) 
        await search_inp.fill(product_name)

        search_bn = page.locator('button[data-test="search-submit"]')
        await search_bn.click()
        result_title = page.locator('h5[data-test="product-name"]').first
        await expect(result_title).to_be_visible(timeout=10000)

        print(f"{product_name} → PASS")
        return {"product": product_name, "status": "PASS"}

    except Exception as e:
        print(f"{product_name} → FAIL")
        return {"product": product_name, "status": "FAIL", "error": str(e)}

    finally:
        await page.close()


async def main():
    print(f"Starting {len(TEST_PRODUCTS)} products...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        tasks = [
            search_single_product(browser, product) for product in TEST_PRODUCTS
        ]

        results = await asyncio.gather(*tasks)

        await browser.close()

    print("\n--- Execution Summary ---")
    for res in results:
        print(f"{res['product']:<20} : {res['status']}")

if __name__ == "__main__":
    asyncio.run(main())
