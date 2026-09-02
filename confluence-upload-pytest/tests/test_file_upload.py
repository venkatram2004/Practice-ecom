"""
Challenge 1 — File Upload + Validation (Confluence sandbox), pytest version.

Assumes standard Confluence attachment flow:
    Page -> "..." (more actions) -> Attachments -> Upload files

Adjust the locator text below if your sandbox's theme/version differs.
All file paths come from the `valid_files` / `invalid_file` fixtures in
conftest.py, which are relative to the project (test-data/) — never
machine-specific absolute paths.
"""
import re
import pytest
from playwright.sync_api import expect


def open_upload_dialog(page):
    """Shared helper: navigates the attachments upload UI from a page view."""
    page.get_by_role("button", name=re.compile("more actions|···", re.I)).click()
    page.get_by_role("menuitem", name=re.compile("attachments", re.I)).click()
    page.get_by_role("button", name=re.compile("upload files?|attach files?", re.I)).click()


def test_valid_file_upload_succeeds(page, valid_files):
    file_path = valid_files["pdf"]

    open_upload_dialog(page)

    # Select the file via Playwright's file-upload API
    file_input = page.locator("input[type='file']")
    file_input.set_input_files(str(file_path))

    # Verify the file was selected before submitting
    expect(page.get_by_text(file_path.name)).to_be_visible()

    # Submit the upload
    page.get_by_role("button", name=re.compile("^upload$|save", re.I)).click()

    # Verify actual success — banner or the file now listed in attachments
    success = page.get_by_text(re.compile("uploaded successfully|attachment added", re.I))
    listed = page.get_by_text(file_path.name)
    expect(success.or_(listed)).to_be_visible(timeout=10_000)


def test_invalid_file_type_is_rejected(page, invalid_file):
    open_upload_dialog(page)

    file_input = page.locator("input[type='file']")
    file_input.set_input_files(str(invalid_file))

    # Attempt submit only if the button is enabled — some UIs block it client-side
    upload_button = page.get_by_role("button", name=re.compile("^upload$|save", re.I))
    if upload_button.is_enabled():
        upload_button.click()

    # Validate the actual rejection — an error is shown, no success confirmation
    error = page.get_by_text(
        re.compile("not allowed|unsupported file type|rejected|invalid file", re.I)
    )
    expect(error).to_be_visible(timeout=10_000)

    success = page.get_by_text(re.compile("uploaded successfully|attachment added", re.I))
    expect(success).not_to_be_visible()


# --- Bonus: parameterized test across 3 valid file types ---
@pytest.mark.parametrize("file_key,label", [
    ("txt", "text file"),
    ("pdf", "PDF file"),
    ("png", "PNG image"),
])
def test_upload_succeeds_for_file_type(page, valid_files, file_key, label):
    file_path = valid_files[file_key]

    open_upload_dialog(page)

    file_input = page.locator("input[type='file']")
    file_input.set_input_files(str(file_path))

    expect(page.get_by_text(file_path.name)).to_be_visible()

    page.get_by_role("button", name=re.compile("^upload$|save", re.I)).click()

    success = page.get_by_text(re.compile("uploaded successfully|attachment added", re.I))
    listed = page.get_by_text(file_path.name)
    expect(success.or_(listed)).to_be_visible(timeout=10_000)
