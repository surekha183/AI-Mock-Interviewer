import fitz

def extract_text_from_pdf(pdf_path):

    print("=" * 50)
    print("Opening PDF:", pdf_path)

    text = ""

    document = fitz.open(pdf_path)

    print("Number of pages:", len(document))

    for page_num, page in enumerate(document, start=1):
        page_text = page.get_text()

        print(f"\n----- Page {page_num} -----")
        print(page_text[:500])   # Print first 500 characters

        text += page_text

    document.close()

    print("\nFinal extracted text length:", len(text))
    print("=" * 50)

    return text