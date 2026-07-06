import streamlit as st
import requests
import json
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Amazon Daily Top 10 Merch Matrix", layout="wide")

st.title("🏹 Amazon Daily Top 10 Merch Matrix")
st.write("Your fresh, daily blueprint for high-volume Amazon buyer search trends with direct-launch Canva integration.")

if st.button("🔄 Clear Cache & Refresh Daily Trends"):
    st.cache_data.clear()
    st.rerun()

SEED_ROOTS = [
    "retro vintage", 
    "coastal summer", 
    "funny dog", 
    "aesthetic graphic", 
    "club shirt", 
    "book lovers",
    "funny graphic"
]

amazon_trends = []

for root in SEED_ROOTS:
    try:
        url = f"https://completion.amazon.com/api/2017/suggestions?session-id=123-4567890-1234567&customer-id=A1234567890&request-id=1234567890&page-type=Gateway&alias=aps&site-variant=desktop&version=1&mid=ATVPDKIKX0DER&lz=1&keyword={root}%20shirt"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            suggestions = data.get("suggestions", [])
            for s in suggestions:
                phrase = s.get("value", "")
                if len(phrase) > len(root) + 6 and "shirt" in phrase:
                    clean_phrase = phrase.replace("t-shirt", "").replace("tshirt", "").replace("shirt", "").strip().title()
                    if clean_phrase and len(clean_phrase) < 45:
                        amazon_trends.append({
                            "Niche Class": root.upper(),
                            "Active Amazon Buyer Trend": clean_phrase
                        })
    except:
        pass

df_raw = pd.DataFrame(amazon_trends).drop_duplicates(subset=["Active Amazon Buyer Trend"])

if len(df_raw) < 10:
    fallback_data = [
        {"Niche Class": "COASTAL SUMMER", "Active Amazon Buyer Trend": "Gulf Of Mexico Beach Club Vintage"},
        {"Niche Class": "RETRO VINTAGE", "Active Amazon Buyer Trend": "Mama Mini Groovy 70s Match"},
        {"Niche Class": "BOOK LOVERS", "Active Amazon Buyer Trend": "Just A Girl Who Loves Romance Books & Coffee"},
        {"Niche Class": "FUNNY DOG", "Active Amazon Buyer Trend": "Official Couch Potato Security Crew"},
        {"Niche Class": "CLUB SHIRT", "Active Amazon Buyer Trend": "Vintage Hiking Club Aesthetic"},
        {"Niche Class": "AESTHETIC GRAPHIC", "Active Amazon Buyer Trend": "Cottagecore Wildflower Botanical"},
        {"Niche Class": "RETRO VINTAGE", "Active Amazon Buyer Trend": "Pickleball Social Club Local"},
        {"Niche Class": "FUNNY GRAPHIC", "Active Amazon Buyer Trend": "Introverted But Great At Data Math"},
        {"Niche Class": "COASTAL SUMMER", "Active Amazon Buyer Trend": "Amalfi Coast Sailing Club Vintage"},
        {"Niche Class": "BOOK LOVERS", "Active Amazon Buyer Trend": "Read More Books Emotional Rescue"}
    ]
    df_raw = pd.DataFrame(fallback_data)

df_top_10 = df_raw.head(10).reset_index(drop=True)
df_top_10.index += 1

st.subheader("📋 Top 10 Daily Trending Products Checklist")
st.write("Click on any product slot below to open its custom workspace assets:")

selected_slot = st.radio(
    "Choose a product position to execute right now:",
    options=df_top_10.index,
    format_func=lambda x: f"Slot #{x}: {df_top_10.loc[x, 'Active Amazon Buyer Trend']} ({df_top_10.loc[x, 'Niche Class']})"
)

chosen_trend = df_top_10.loc[selected_slot, "Active Amazon Buyer Trend"]

st.markdown("---")
st.markdown(f"### ⚡ Processing Layout Workstation for: **Slot #{selected_slot} — {chosen_trend}**")

# --- NEW: DIRECT CANVA WORKSPACE GENERATOR LINK ---
st.subheader("🚀 Step 1: Launch Pre-Sized Canva Workspace")
st.write("Clicking this button opens a brand new Canva project configured exactly to Amazon Merch parameters (4500x5400px):")

# Programmatically build custom Canva creator deep link
canva_base_url = "https://www.canva.com/design/new?units=px&width=4500&height=5400"
st.link_button("🎨 Open 4500 x 5400px Canvas Project", canva_base_url, type="primary", use_container_width=True)

# --- STEP 2: CANVA IMAGING PROMPTER ---
st.subheader("🎨 Step 2: Canva Text-to-Image Optimized Prompt")
st.write("Copy this phrase into Canva's **Magic Media** tab on the left sidebar of your new project:")

canva_prompt = (
    f"A high-quality, professional t-shirt vector graphic emblem featuring the phrase: \"{chosen_trend}\". "
    f"Minimalist streetwear style design with clean lines and bold typography seamlessly woven into the icon layout. "
    f"Limited flat retro color palette with no complex realistic photo gradients. "
    f"CRITICAL DESIGN REQUISITE: Isolated object style, positioned centrally over a completely solid, plain white background. "
    f"The artwork must have thick, clean, sharp borders with a clear sticker-cut silhouette outline to allow for smooth one-click background removal."
)

st.text_area("📋 Copy This Prompt For Canva AI:", value=canva_prompt, height=130)

# --- STEP 3: SEO LISTING METADATA ---
st.subheader("📝 Step 3: Amazon Merch On Demand Listing Metadata Pack")

seo_title = f"{chosen_trend} Shirt Vintage Retro T-Shirt"
seo_brand = f"{chosen_trend} Aesthetic Apparel Collective"
seo_b1 = f"Stand out with this unique premium-style {chosen_trend} t-shirt. Features a custom high-contrast graphic layout that fits perfectly into casual everyday outfits, streetwear looks, or active wear."
seo_b2 = f"The ultimate graphic design selection for fans and apparel collectors. This vintage-inspired {chosen_trend} layout makes an incredible gift for birthdays, holidays, or special group events."

col1, col2 = st.columns(2)
with col1:
    st.text_input("📋 Optimized Product Title (Max 60 Characters)", value=seo_title[:60], key="title_v2")
with col2:
    st.text_input("📋 Brand Name Specification", value=seo_brand[:60], key="brand_v2")

st.text_area("📋 Key Feature Bullet Point 1", value=seo_b1, height=65, key="b1_v2")
st.text_area("📋 Key Feature Bullet Point 2", value=seo_b2, height=65, key="b2_v2")
