from googlesearch import search
from src.utils import scrape_text_from_url, extract_products
import openai
from dotenv import load_dotenv
import os
import argparse
import pandas as pd
from src.product import Product, ProductList
from typing import Union, Any
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--model",
    dest="model",
    help="OpenAI model",
    type=str,
    default="gpt-4.1",
    required=False,
)
parser.add_argument(
    "-p",
    "--prompt",
    dest="prompt",
    help="Prompt to the system.",
    type=str,
    required=False,
    default="You are given a URL of a web page. Your task is to determine if the page is a product page for a CBD topical marketed for pain relief. A valid product page should meet all of the following criteria: 1) It lists a single product available for sale. 2) The product must be a CBD topical (e.g., cream, balm, gel, lotion) applied to the skin. 3) The product must be explicitly marketed for pain relief. If all criteria are met, extract the following: 1) Brand Name 2) Product Name 3)Product URL. Ensure that no more than two products from the same brand are included in total. If this would exceed the limit, return SKIP. Output Format (CSV-style): Brand Name,Product Name,URL. If the criteria are not met or the brand already has 2 products recorded, return SKIP."
)
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

load_dotenv()

args = parser.parse_args()
Path(args.output_dir).mkdir(parents=True, exist_ok=True)

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

urls = search(
    args.search, num_results=150, unique=True, lang="en", region="us"
)

urls_df = pd.DataFrame(urls, columns=["url"])
urls_df.to_csv(f"{args.output_dir}/search_results.csv", index=False)

output_data: list[dict[str, Any]] = []
for u in urls_df.url:
    print(u)
    text = scrape_text_from_url(u)
    if text:
        print("------------")
        products: Union[ProductList, None] = extract_products(text, args.prompt, args.model, client)
        if products:
            for choice in range(len(products)):
                print(f"Choice number {choice}\n")
                for p in products[choice].message.parsed.products:
                    res = dict(p)
                    res["url"] = u
                    print(res)
                    output_data.append(res)
                    pd.DataFrame(output_data).to_csv(f"{args.output_dir}/product_list.csv", index=False)
                    print()
        print("------------")
        print()

