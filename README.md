# Facebook Marketplace Listing Filter

This is a Streamlit web app that parses, filters, and sorts copied Facebook Marketplace listings for used equipment (e.g., John Deere tractors). It supports filtering by price, keywords, generation type (Gen 1 vs Gen 2), and sorts by proximity to Madison, Wisconsin.

## Features

- ✅ Paste raw Facebook Marketplace text listings into a simple web form
- ✅ Automatically extract and structure listing data (title, price, location, etc.)
- ✅ Filter by price and keywords
- ✅ Separate results by Gen 1 and Gen 2 (based on description clues)
- ✅ Sort listings by distance from Madison, WI (ZIP 53701)
- ✅ Export filtered results as CSV
- ✅ View Gen 1 and Gen 2 results separately

## How to Run Locally

1. Clone this repository or download the ZIP.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run marketplace_filter.py
```

## How to Deploy to Streamlit Cloud

1. Push the contents of this repo to your GitHub account.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with GitHub.
3. Select the repository and deploy.

## Example Listing Format (Input)

```
John Deere 2025R with Loader and Snowblower - $13,500 - Madison, WI
Excellent condition, 2014 Gen 1 model. Includes 54" snowblower, loader.
Posted 3 days ago
```

## License

MIT License.
