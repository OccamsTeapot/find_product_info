from googlesearch import search
from src.utils import scrape_text_from_url, extract_products, scrape_internal_urls
import os
import argparse
import pandas as pd
from src.product import Product, ProductList
from typing import Union, Any
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "-o",
    "--output_dir",
    dest="output_dir",
    help="Output directory",
    type=str,
    required=True,
)

parser.add_argument(
    "-s",
    "--search",
    dest="search",
    help="Search query for Google.",
    type=str,
    required=False,
    default="CBD topicals for pain -youtube.com -reddit.com -amazon.com -forbes.com -healthline.com -medicalnewstoday.com -webmd.com -drugs.com -mayoclinic.org -arthritis.org -harvard.edu -quora.com -wikipedia.org -fda.gov -pdxmonthly.com -observer.com"
)

args = parser.parse_args()
Path(args.output_dir).mkdir(parents=True, exist_ok=True)

urls = []
urls.extend(search(
    args.search, num_results=150, unique=True, lang="en", region="us"
))

internals=[]
for v in urls:
    internals.extend(scrape_internal_urls(v))

clean_internals = [v for v in internals if "product" in v]

urls_df = pd.DataFrame(urls + clean_internals, columns=["url"])
urls_df.to_csv(f"{args.output_dir}/search_results.csv", index=False)

scraped_text=[]

for u in urls_df.url:
    print(u)
    text = scrape_text_from_url(u)
    scraped_text.append(text)

url_with_text=urls_df.insert(1,"Text",scraped_text)
urls_with_text.to_csv(f"{args.output_dir}/urls_with_text.csv", index=False)
