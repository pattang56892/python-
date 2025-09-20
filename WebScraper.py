from bs4 import BeautifulSoup
import urllib.request

def scrape_quotes():
    print("\n=== CODE DEMONSTRATION ===")
    
    # Step 1: Define URL
    url = "http://quotes.toscrape.com/"
    print("STEP 1 - CODE: url = 'http://quotes.toscrape.com/'")
    print(f"Action: Setting target URL to {url}")
    
    # Step 2: Make HTTP request
    print("\nSTEP 2 - CODE: urllib.request.urlopen(url).read().decode()")
    print("Action: Sending HTTP request to fetch webpage content")
    try:
        resp = urllib.request.urlopen(url).read().decode()
        print(f"Success: Retrieved {len(resp)} characters of HTML content")
    except Exception as e:
        print(f"Error: Failed to retrieve webpage - {e}")
        return
    
    # Step 3: Parse HTML with BeautifulSoup
    print("\nSTEP 3 - CODE: BeautifulSoup(resp, features='html.parser')")
    print("Action: Parsing HTML content into a searchable structure")
    soup = BeautifulSoup(resp, features="html.parser")
    print("Success: HTML parsed and ready for element extraction")
    
    # Step 4: Find quote elements
    print("\nSTEP 4 - CODE: soup.find_all(name='span', attrs={'class':'text'})")
    print("Action: Searching for all <span> elements with class='text'")
    aTag = soup.find_all(name="span", attrs={"class": "text"})
    print(f"Found: {len(aTag)} quote elements")
    print("Sample elements found:")
    for i, tag in enumerate(aTag[:3]):  # Show first 3
        print(f"  Quote {i+1}: {tag.text[:50]}...")
    
    # Step 5: Extract and display quotes
    print("\nSTEP 5 - CODE: for a in aTag: print(f'%{i}%:%a.text')")
    print("Action: Iterating through quote elements and extracting text")
    print("\n--- EXTRACTED QUOTES ---")
    i = 0
    for a in aTag:
        i = i + 1
        print(f"%{i}%: {a.text}")
    
    # Step 6: Find author elements
    print(f"\nSTEP 6 - CODE: soup.find_all(name='small', attrs={{'class':'author'}})")
    print("Action: Searching for all <small> elements with class='author'")
    zz = soup.find_all(name="small", attrs={"class": "author"})
    print(f"Found: {len(zz)} author elements")
    
    # Step 7: Extract and display authors
    print("\nSTEP 7 - CODE: for a in zz: print(f'%{i}%:%a.text')")
    print("Action: Iterating through author elements and extracting text")
    print("\n--- EXTRACTED AUTHORS ---")
    i = 0
    for a in zz:
        i = i + 1
        print(f"%{i}%: {a.text}")
    
    print("\n=== SCRAPING COMPLETE ===")
    print(f"Successfully extracted {len(aTag)} quotes and {len(zz)} authors")

def main():
    print("=== PROBLEM EXPLANATION ===")
    print("Task: Web scraping to extract quotes and authors from a website")
    print()
    
    print("WHAT THE CODE DOES:")
    print("1. Makes an HTTP request to quotes.toscrape.com")
    print("2. Downloads the HTML content of the webpage")
    print("3. Parses the HTML using BeautifulSoup library")
    print("4. Finds all quote text elements (span with class='text')")
    print("5. Finds all author elements (small with class='author')")
    print("6. Extracts and displays the text content")
    print()
    
    print("ALGORITHM ANALYSIS:")
    print("Problem: How do we extract specific data from a webpage?")
    print("Solution: Web scraping with HTML parsing!")
    print("- HTTP request: Download the raw HTML content")
    print("- HTML parsing: Convert HTML into searchable structure")
    print("- Element selection: Find specific HTML elements by tag/class")
    print("- Text extraction: Get the actual text content from elements")
    print()
    
    print("WHY IT WORKS:")
    print("- Websites store data in structured HTML format")
    print("- HTML elements have predictable patterns (tags, classes, IDs)")
    print("- BeautifulSoup can navigate and search HTML like a tree")
    print("- We target specific CSS selectors to find desired content")
    print("- Example: <span class='text'>Quote here</span>")
    print("           <small class='author'>Author name</small>")
    print()
    
    print("LIBRARIES USED:")
    print("- urllib.request: Built-in Python library for HTTP requests")
    print("- BeautifulSoup: Third-party library for HTML parsing")
    print("- Installation: pip install beautifulsoup4")
    
    print("\n" + "="*60)
    
    print("DEMONSTRATION: Scraping quotes.toscrape.com")
    print("Expected: Extract quotes and their authors from the website")
    
    # Run the scraping function
    scrape_quotes()
    
    print("\n=== ALGORITHM SUMMARY ===")
    print("✓ Successfully made HTTP request to target website")
    print("✓ Parsed HTML content into searchable structure")
    print("✓ Extracted quotes using CSS class selectors")
    print("✓ Extracted authors using CSS class selectors")
    print("✓ Displayed formatted results with numbering")
    print()
    
    print("KEY CONCEPTS DEMONSTRATED:")
    print("- HTTP requests and response handling")
    print("- HTML parsing and DOM navigation")
    print("- CSS selector-based element finding")
    print("- Text extraction from HTML elements")
    print("- Error handling for network requests")
    print()
    
    print("PRACTICAL APPLICATIONS:")
    print("- Price monitoring from e-commerce sites")
    print("- News article collection")
    print("- Social media data extraction")
    print("- Research data gathering")
    print("- Content aggregation")
    
    print("\n=== HOW TO RUN THIS FILE ===")
    print("1. Install required library: pip install beautifulsoup4")
    print("2. Save as: WebScraper.py")
    print("3. Run: python WebScraper.py")
    print("4. Make sure you have internet connection")

if __name__ == "__main__":
    main()