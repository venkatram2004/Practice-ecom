from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

CURRENT_DIR = Path(__file__).resolve().parent
TEST_DATA_DIR = CURRENT_DIR / "test_data"
URL = "https://the-internet.herokuapp.com/upload"


def test_successful_file_upload(page: Page):
    page.goto(URL)

    image_path = TEST_DATA_DIR / "valid_sample.png"

    upload_input = page.locator("#file-upload")
    upload_input.set_input_files(str(image_path))

    assert "valid_sample.png" in upload_input.input_value()

    page.get_by_role("button", name="Upload").click()

    expect(page.locator("#uploaded-files")).to_contain_text("valid_sample.png")


def test_empty_upload_rejection(page: Page):
    page.goto(URL)

    page.get_by_role("button", name="Upload").click()

    expect(page.locator("h1")).to_have_text("Internal Server Error")


@pytest.mark.parametrize(
    "file_name",
    [
        "valid_sample.png",
        "sample_report.pdf",
        "notes.txt",
    ],
)
def test_checking_3_parametrized(page: Page, file_name: str):
    page.goto(URL)

    file_path = TEST_DATA_DIR / file_name

    upload_input = page.locator("#file-upload")
    upload_input.set_input_files(str(file_path))

    assert file_name in upload_input.input_value()

    page.get_by_role("button", name="Upload").click()

    expect(page.locator("h3")).to_have_text("File Uploaded!")
    expect(page.locator("#uploaded-files")).to_contain_text(file_name)
