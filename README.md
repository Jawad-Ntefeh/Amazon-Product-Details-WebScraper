# Amazon-Product-Details-WebScraper

This project is a web scraping tool built with Python and Selenium to extract product details from Amazon.sa. The script focuses on products such as shoes and collects detailed information, including product names, prices, and additional specifications. The results are stored in a CSV file, and product images are downloaded for further analysis or use.

## Features

- Scrapes product details including:
  - Name, price, care instructions, sole materials, outer materials, and closure types.
  - Additional details: ASIN, department, availability dates, shipping and seller information.
- Downloads product images and saves them to a specified directory.
- Exports the collected data into a structured CSV file.

## Requirements

- Python 3.x
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

### Python Libraries

Install the required libraries using pip:

```bash
pip install selenium requests
```

## Usage

1. **Set up the Environment**:
   - Download and place the `chromedriver.exe` in your project directory or ensure it's in your system's PATH.

2. **Run the Script**:
   - Execute the Python script:
     ```bash
     python main.py
     ```

3. **Outputs**:
   - `product_details.csv`: Contains the scraped product details.
   - `product images/`: Directory storing downloaded product images.

## Customization

- Modify the `input_element.send_keys()` line to scrape products other than shoes:
  ```python
  input_element.send_keys("<Your Search Query>" + Keys.ENTER)
  ```
- Adjust `product_index` to set the number of products to scrape.

## Notes

- Ensure compliance with Amazon's terms of service before using this tool.
- The script currently scrapes the first three products. Adjust the limit in the loop for more results:
  ```python
  if product_index < <desired_number_of_products>:
  ```
