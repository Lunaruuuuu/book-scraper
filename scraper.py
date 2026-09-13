from playwright.sync_api import sync_playwright
import csv
import re


# ============================================================
# CONFIGURATION
# ============================================================

URL = "https://books.toscrape.com/"

MAX_BOOKS = 20

RAW_FILE = "books_raw.csv"
CLEAN_FILE = "books_clean.csv"


# ============================================================
# DATA CLEANING FUNCTIONS
# ============================================================

def clean_text(text):
    """
    Membersihkan teks dari spasi berlebihan.
    """

    if not text:
        return ""

    # Menghapus spasi berlebihan
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_price(value):
    """
    Mengubah harga dari string menjadi float.

    Contoh:
    "£51.77" -> 51.77
    """

    if not value:
        return 0.0

    # Hapus simbol mata uang dan karakter selain angka/desimal
    value = re.sub(r"[^0-9.]", "", value)

    try:
        return float(value)

    except ValueError:
        return 0.0


def clean_rating(value):
    """
    Mengubah rating dalam bentuk kata menjadi integer.

    Contoh:
    "One"   -> 1
    "Two"   -> 2
    "Three" -> 3
    "Four"  -> 4
    "Five"  -> 5
    """

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    if not value:
        return 0

    # Ambil kata rating dari class
    for rating_name, rating_value in rating_map.items():

        if rating_name in value:
            return rating_value

    return 0


# ============================================================
# SAVE RAW DATA
# ============================================================

def save_raw_data(data):
    """
    Menyimpan data hasil scraping sebelum cleaning.
    """

    with open(
        RAW_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["title", "price", "rating"]
        )

        writer.writeheader()
        writer.writerows(data)

    print(f"Raw data disimpan ke: {RAW_FILE}")


# ============================================================
# CLEAN DATA
# ============================================================

def clean_data(data):
    """
    Membersihkan seluruh data hasil scraping.
    """

    cleaned = []

    for item in data:

        title = clean_text(item["title"])
        price = clean_price(item["price"])
        rating = clean_rating(item["rating"])

        # Missing value handling
        if not title:
            title = "Unknown"

        cleaned.append({
            "title": title,
            "price": price,
            "rating": rating
        })

    return cleaned


# ============================================================
# SAVE CLEAN DATA
# ============================================================

def save_clean_data(data):

    with open(
        CLEAN_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["title", "price", "rating"]
        )

        writer.writeheader()
        writer.writerows(data)

    print(f"Clean data disimpan ke: {CLEAN_FILE}")


# ============================================================
# MAIN SCRAPER
# ============================================================

def scrape_books():

    books = []

    with sync_playwright() as p:

        # ----------------------------------------------------
        # Launch browser
        # ----------------------------------------------------

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page(
            viewport={
                "width": 1280,
                "height": 720
            }
        )

        print("Membuka Books to Scrape...")

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Halaman berhasil dibuka.")

        # ----------------------------------------------------
        # Wait for book elements
        # ----------------------------------------------------

        page.wait_for_selector(
            "article.product_pod",
            timeout=30000
        )

        print("Data buku berhasil dimuat.")

        # ----------------------------------------------------
        # Get book elements
        # ----------------------------------------------------

        book_elements = page.locator(
            "article.product_pod"
        )

        book_count = book_elements.count()

        print(
            f"Jumlah buku pada halaman: {book_count}"
        )

        # ----------------------------------------------------
        # Scraping
        # ----------------------------------------------------

        available = min(
            book_count,
            MAX_BOOKS
        )

        for i in range(available):

            try:

                book = book_elements.nth(i)

                # ------------------------------------------------
                # Title
                # ------------------------------------------------

                title_element = book.locator(
                    "h3 a"
                )

                title = title_element.get_attribute(
                    "title"
                )

                # ------------------------------------------------
                # Price
                # ------------------------------------------------

                price = book.locator(
                    ".price_color"
                ).inner_text()

                # ------------------------------------------------
                # Rating
                # ------------------------------------------------

                rating = book.locator(
                    ".star-rating"
                ).get_attribute(
                    "class"
                )

                # ------------------------------------------------
                # Store raw data
                # ------------------------------------------------

                books.append({
                    "title": title,
                    "price": price,
                    "rating": rating
                })

                print(
                    f"[{len(books)}/{MAX_BOOKS}] "
                    f"{title} | "
                    f"{price} | "
                    f"{rating}"
                )

            except Exception as e:

                print(
                    f"Gagal mengambil buku ke-{i + 1}: {e}"
                )

        # ----------------------------------------------------
        # Close browser
        # ----------------------------------------------------

        browser.close()

    return books


# ============================================================
# PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("BOOKS TO SCRAPE")
    print("=" * 60)

    # --------------------------------------------------------
    # Scraping
    # --------------------------------------------------------

    raw_data = scrape_books()

    print("\nScraping selesai.")
    print(f"Total buku ditemukan: {len(raw_data)}")

    # --------------------------------------------------------
    # Save raw data
    # --------------------------------------------------------

    save_raw_data(raw_data)

    # --------------------------------------------------------
    # Cleaning
    # --------------------------------------------------------

    cleaned_data = clean_data(raw_data)

    # --------------------------------------------------------
    # Save cleaned data
    # --------------------------------------------------------

    save_clean_data(cleaned_data)

    print("\n" + "=" * 60)
    print("SELESAI")
    print("=" * 60)