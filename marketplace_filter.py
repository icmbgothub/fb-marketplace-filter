import re
import pandas as pd
import streamlit as st
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# === Configuration ===
FILTER_KEYWORDS = ["John Deere 2025R"]
EXCLUDE_KEYWORDS = ["wanted", "ISO"]
MAX_PRICE = 20000
YEAR_THRESHOLD = 2020
SEPARATE_GEN_MODELS = True
REFERENCE_LOCATION = (43.0731, -89.4012)  # Madison, WI (zip 53701)

# === Streamlit Interface ===
st.title("Facebook Marketplace Listing Filter")
st.markdown("Paste your raw Facebook Marketplace listings below:")
raw_data = st.text_area("Listings", height=300)

# === Parsing and Geocoding Functions ===
geolocator = Nominatim(user_agent="marketplace_parser")
location_cache = {}

def get_coords(location_str):
    if location_str in location_cache:
        return location_cache[location_str]
    try:
        loc = geolocator.geocode(location_str)
        if loc:
            coords = (loc.latitude, loc.longitude)
            location_cache[location_str] = coords
            return coords
    except:
        pass
    return None

def parse_listings(raw_text):
    listings = []
    entries = raw_text.strip().split("\n\n")

    for entry in entries:
        lines = entry.split("\n")
        if not lines or len(lines) < 2:
            continue

        title_line = lines[0]
        description = lines[1] if len(lines) > 1 else ""
        date_posted = lines[2] if len(lines) > 2 else ""

        match = re.match(r"(.*?) - \$(.*?) - (.*)", title_line)
        if not match:
            continue

        title, price_str, location = match.groups()
        try:
            price = float(price_str.replace(",", "").strip())
        except ValueError:
            price = None

        gen_model = "Unknown"
        if SEPARATE_GEN_MODELS:
            if re.search(r"gen ?1", description.lower()):
                gen_model = "Gen 1"
            elif re.search(r"gen ?2", description.lower()):
                gen_model = "Gen 2"

        coords = get_coords(location)
        distance = geodesic(REFERENCE_LOCATION, coords).miles if coords else None

        listings.append({
            "Title": title.strip(),
            "Price": price,
            "Location": location.strip(),
            "Description": description.strip(),
            "Date Posted": date_posted.strip(),
            "Gen Model": gen_model,
            "Distance (mi)": distance
        })

    return listings

def filter_listings(listings):
    filtered = []
    for listing in listings:
        if listing["Price"] is None or listing["Price"] > MAX_PRICE:
            continue
        title_desc = (listing["Title"] + " " + listing["Description"]).lower()
        if any(keyword.lower() not in title_desc for keyword in FILTER_KEYWORDS):
            continue
        if any(bad.lower() in title_desc for bad in EXCLUDE_KEYWORDS):
            continue
        if "2021" in title_desc or "2022" in title_desc or "2023" in title_desc:
            continue
        filtered.append(listing)
    return filtered

# === Main Execution ===
if raw_data:
    parsed = parse_listings(raw_data)
    filtered = filter_listings(parsed)
    df = pd.DataFrame(filtered)
    if not df.empty:
        df = df.sort_values(by="Distance (mi)", ascending=True)
        st.success("Filtered and sorted listings:")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="filtered_listings.csv", mime="text/csv")

        if SEPARATE_GEN_MODELS:
            gen1 = df[df["Gen Model"] == "Gen 1"]
            gen2 = df[df["Gen Model"] == "Gen 2"]
            if not gen1.empty:
                st.subheader("Gen 1 Listings")
                st.dataframe(gen1)
            if not gen2.empty:
                st.subheader("Gen 2 Listings")
                st.dataframe(gen2)
    else:
        st.warning("No listings matched your criteria.")
