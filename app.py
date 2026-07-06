import streamlit as st
import xml.etree.ElementTree as ET
import requests
import pandas as pd

st.set_page_config(page_title="Merch Momentum Engine", layout="wide")

st.title("👕 Amazon Merch on Demand Momentum Engine")
st.write("Isolating real-time viral trends and auto-generating optimized Gemini design prompts and Amazon SEO listings.")

st.info("⚡ Aggregating real-time internet culture vectors and breakthrough search trends...")

# --- TREND AGGREGATION ---
trends_list = []
try:
    rss_url = "https://trends.google.com/trending/rss?geo=US"
    response = requests.get(rss_url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for item in root.findall('.//item'):
            title = item.find('title').text
            approx_traffic = item.find('{ht}approx_traffic')
            traffic_text = approx_traffic.text if approx_traffic is not None else "High Momentum"
            trends_list.append({"Trend Phrase": title, "Search Volume Velocity": traffic_text})
except Exception as e:
    st.warning("🔄 Temporary connection delay with primary live feed. Loading backup seasonal trends panel...")

if not trends_list:
    trends_list = [
        {"Trend Phrase": "Retro Vintage Pickleball Club", "Search Volume Velocity": "50,000+ searches"},
        {"Trend Phrase": "Just A Girl Who Loves Coffee and Book Series", "Search Volume Velocity": "30,000+ searches"},
        {"Trend Phrase": "Introverted But Willing To Discuss Financial Markets", "Search Volume Velocity": "25,000+ searches"},
        {"Trend Phrase": "Official Dog Walker / Couch Potato Support Crew", "Search Volume Velocity": "15,000+ searches"}
    ]

df_trends = pd.DataFrame(trends_list)

# --- USER SELECTION ---
st.subheader("🔥 Step 1: Select a High-Velocity Trend Target")
selected_trend = st.selectbox("Choose a breakthrough phrase to build your Merch product around:", df_trends["Trend Phrase"].tolist())

matched_row = df_trends[df_trends["Trend Phrase"] == selected_trend].iloc[0]
st.success(f"🎯 Target Acquired: **'{selected_trend}'** ({matched_row['Search Volume Velocity']})")

st.markdown("---")

# --- STEP 2: GEMINI GREEN-SCREEN PROMPT GENERATOR ---
st.subheader("🎨 Step 2: Copy-and-Paste Gemini Design Prompt Generator")
st.write("Copy this highly detailed, professional prompt into Gemini to generate a clean, isolated graphic asset for your shirt:")

clean_keyword = selected_trend.replace("'", "").replace('"', "")

# Dynamic prompt building logic based on layout traits
if len(clean_keyword) > 25:
    graphic_style = "A detailed, vintage-style distressed emblem graphic"
    composition_rules = "The typography must be arranged in a beautifully stacked, balanced typographic layout."
else:
    graphic_style = "A vibrant, minimalist vector icon emblem graphic"
    composition_rules = "The typography should be clean, centered, and seamlessly integrated into the icon artwork."

gemini_art_prompt = (
    f"Create a professional t-shirt graphic asset featuring the exact phrase: \"{clean_keyword}\". "
    f"The style must be {graphic_style}. {composition_rules} Use a bold, retro color palette featuring cream, "
    f"sunset orange, and deep teal accents. CRITICAL CHROMAKEY REQUIREMENTS FOR TRANSPARENCY: The background "
    f"MUST be a solid, completely flat, uniform green screen color using exactly hex code #00FF00. No shadows, "
    f"no gradients, no lighting variations, and no environmental background details. The subject artwork must "
    f"have crisp, sharp, well-defined borders with a thin white outline separating it from the green background "
    f"to allow for perfect programmatic cutout background removal."
)

st.text_area("📋 Copy This Complete Image Prompt For Gemini:", value=gemini_art_prompt, height=140)

st.markdown("---")

# --- STEP 3: SEO LISTING ---
st.subheader("📝 Step 3: Copy-and-Paste Amazon Merch SEO Listing Matrix")
st.write("Optimize your Amazon product visibility with these pre-formatted SEO data blocks:")

merch_title = f"{clean_keyword} Shirt Vintage Retro T-Shirt"
merch_brand = f"{clean_keyword} Aesthetic Apparel Co."
bullet_1 = f"Featuring a stylish and unique {clean_keyword} design, this graphic tee is perfect for everyday casual wear, community events, or gifting to friends and family."
bullet_2 = f"Grab this limited edition retro {clean_keyword} apparel layout. Designed with premium high-contrast colors to complement streetwear, denim, or standard athleisure fits."
description = f"Looking for the ultimate style statement? This premium {clean_keyword} graphic t-shirt combines comfortable everyday wearability with an elite retro typographic layout. Ideal for holidays, birthdays, or matching group outfits. Lightweight, classic fit, double-needle sleeve and bottom hem."

col_list1, col_list2 = st.columns(2)
with col_list1:
    st.text_input("📋 Amazon Product Title", value=merch_title[:60])
    st.text_input("📋 Brand Name", value=merch_brand[:60])
with col_list2:
    st.text_area("📋 Key Product Features / Bullet Point 1", value=bullet_1, height=70)
    st.text_area("📋 Key Product Features / Bullet Point 2", value=bullet_2, height=70)

st.text_area("📋 Full Product Description", value=description, height=80)
