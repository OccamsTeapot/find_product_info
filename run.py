from googlesearch import search
from src.utils import scrape_text_from_url, extract_products
import openai
from dotenv import load_dotenv
import os
from pprint import pprint 
load_dotenv()

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
model = "gpt-4o-2024-08-06"
res = search("CDB gummies for sleep", num_results=200, unique=True, lang="en", region="us")
output_dir = "output"
prompt = "Extract information on each CBD gummy product you can find in this text from a website. Capture the name of the `brand`, the name of the `product`, a url to the lab report if it's available, and whether or not it's a product page."

for i in res:
    text = scrape_text_from_url(i)
    print("----")
    print(i)
    products = extract_products(text, prompt, model, client)
    print("----")



