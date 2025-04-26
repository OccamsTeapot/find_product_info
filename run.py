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
    default="Extract information as is in verbatim on each CBD gummy product you can find in this text from a website. Capture the name of the `brand`, the name of the `product`, a url to the lab report if it's available, and whether or not it's a product page. Include the URL of the product if available."
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
    default="CBD gummies for sleep"
)

load_dotenv()

args = parser.parse_args()
Path(args.output_dir).mkdir(parents=True, exist_ok=True)

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

urls = search(
    args.search, num_results=20, unique=True, lang="en", region="us"
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

