import streamlit as st
import requests
import json
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Amazon Auto-Merch Studio", layout="wide")

st.title("🏹 Amazon Merch On Demand Auto-Studio")
st.write("Extracting Amazon trends and instantly rendering custom vibe-matched 4500x5400px transparent PNGs.")

if st.button("🔄 Clear Cache & Refresh Daily Trends"):
    st.cache_data.clear()
    st.rerun()

SEED_ROOTS = ["retro vintage", "coastal summer", "funny dog", "aesthetic graphic", "club shirt", "book lovers"]

amazon_trends = []
for root in SEED_ROOTS:
    try:
        url = f"https://completion.amazon.com/api/2017/suggestions?session-id=123-4567890-1234567&customer-id=A1234567890&request-id=1234567890&page-type=Gateway&alias=aps&site-variant=desktop&version=1&mid=ATVPDKIKX0DER&lz=1&keyword={root}%20shirt"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for s in response.json().get("suggestions", []):
                phrase = s.get("value", "")
                if "shirt" in phrase:
                    clean_phrase = phrase.replace("t-shirt", "").replace("tshirt", "").replace("shirt", "").strip().title()
                    if clean_phrase and len(clean_phrase) < 40:
                        amazon_trends.append({"Niche": root.upper(), "Trend": clean_phrase})
    except:
        pass

if len(amazon_trends) < 10:
    amazon_trends = [
        {"Niche": "COASTAL SUMMER", "Trend": "Gulf Of Mexico Beach Club"},
        {"Niche": "RETRO VINTAGE", "Trend": "Mama Mini Groovy Crew"},
        {"Niche": "BOOK LOVERS", "Trend": "Read Romance Books Drink Coffee"},
        {"Niche": "FUNNY DOG", "Trend": "Official Couch Potato Security"},
        {"Niche": "CLUB SHIRT", "Trend": "Vintage Hiking Club Aesthetic"},
        {"Niche": "AESTHETIC GRAPHIC", "Trend": "Cottagecore Wildflower Botanical"},
        {"Niche": "RETRO VINTAGE", "Trend": "Pickleball Social Club Local"},
        {"Niche": "FUNNY GRAPHIC", "Trend": "Introverted But Great At Math"},
        {"Niche": "COASTAL SUMMER", "Trend": "Amalfi Coast Sailing Club"},
        {"Niche": "BOOK LOVERS", "Trend": "Read More Books Rescue"}
    ]

df_top_10 = pd.DataFrame(amazon_trends).drop_duplicates(subset=["Trend"]).head(10).reset_index(drop=True)
df_top_10.index += 1

st.subheader("📋 Top 10 Live Trends Execution Panel")
selected_slot = st.radio("Select a slot to generate a design instantly:", options=df_top_10.index,
                         format_func=lambda x: f"Slot #{x}: {df_top_10.loc[x, 'Trend']} ({df_top_10.loc[x, 'Niche']})")

chosen_trend = df_top_10.loc[selected_slot, "Trend"]
chosen_niche = df_top_10.loc[selected_slot, "Niche"]

st.markdown("---")
st.subheader(f"🎨 Production Engine: Generating Artwork for Slot #{selected_slot}")

# --- DYNAMIC VIBE ENGINE CONFIGURATOR ---
# Automatically shifts font size, colors, and styling matching the specific target market
vibe_settings = {
    "COASTAL SUMMER": {"color": (0, 200, 200, 255), "size": 380, "spacing": 450, "desc": "🌴 Vibe: Coastal Summer (Electric Teal, Clean High-Impact Layout)"},
    "RETRO VINTAGE": {"color": (255, 94, 54, 255), "size": 410, "spacing": 430, "desc": "✌️ Vibe: Retro 70s Vintage (Sunset Orange, Bold Stacked Layout)"},
    "BOOK LOVERS": {"color": (255, 253, 208, 255), "size": 360, "spacing": 460, "desc": "📚 Vibe: Bookish Indie (Cream / Vintage White, Soft Literary Aesthetic)"},
    "FUNNY DOG": {"color": (255, 253, 208, 255), "size": 430, "spacing": 480, "desc": "🐾 Vibe: Quirky Humor (Cream / Vintage White, Massive Max-Scale Typography)"},
    "AESTHETIC GRAPHIC": {"color": (0, 200, 200, 255), "size": 370, "spacing": 440, "desc": "✨ Vibe: Minimal Streetwear (Electric Teal, Spaced Layout)"},
    "CLUB SHIRT": {"color": (255, 94, 54, 255), "size": 390, "spacing": 450, "desc": "🏅 Vibe: Athletic Club (Sunset Orange, Structured Group Block Layout)"}
}

# Safeguard check if a unique keyword falls outside parameters
current_vibe = vibe_settings.get(chosen_niche, {"color": (255, 253, 208, 255), "size": 380, "spacing": 440, "desc": "Standard Typography Matrix"})

st.caption(f"**Current Aesthetic Matrix applied:** {current_vibe['desc']}")

# --- THE STABLE WEB-FONT FETCH LAYER ---
@st.cache_data
def load_web_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf"
    font_response = requests.get(font_url)
    return font_response.content

try:
    font_bytes = load_web_font()
    # Pull dynamic scaled font size directly from vibe settings
    font = ImageFont.truetype(io.BytesIO(font_bytes), current_vibe["size"])
except Exception as e:
    font = ImageFont.load_default()

# --- PROGRAMMATIC IMAGE GENERATOR ---
img = Image.new("RGBA", (4500, 5400), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Dynamic line spacing and sentence structuring
words = chosen_trend.split()
lines = []
if len(words) > 3:
    lines.append(" ".join(words[:2]))
    lines.append(" ".join(words[2:]))
else:
    lines.append(chosen_trend)

# Compute vertical coordinate offset balances based on row volume count
y_offset = 2400 if len(lines) == 1 else 2100
for line in lines:
    draw.text((2250, y_offset), line, font=font, fill=current_vibe["color"], anchor="mm")
    y_offset += current_vibe["spacing"]

buf = io.BytesIO()
img.save(buf, format="PNG")
byte_im = buf.getvalue()

st.success(f"✅ 4500 x 5400 px Vibe-Matched Transparent PNG Compiled for Slot #{selected_slot}.")

st.download_button(
    label=f"📥 Download Print-Ready PNG for '{chosen_trend}'",
    data=byte_im,
    file_name=f"{chosen_trend.lower().replace(' ', '_')}_amazon_design.png",
    mime="image/png",
    type="primary",
    key=f"dl_{selected_slot}"
)

st.markdown("---")
st.subheader("📝 Step 3: Copy-and-Paste Amazon Merch SEO Metadata Pack")

seo_title = f"{chosen_trend} Shirt Vintage Retro T-Shirt"
seo_brand = f"{chosen_trend} Apparel Collective"
seo_b1 = f"Stand out with this unique premium-style {chosen_trend} t-shirt. Features a custom high-contrast graphic layout that fits perfectly into casual everyday outfits, streetwear looks, or active wear."
seo_b2 = f"The ultimate graphic design selection for fans and apparel collectors. This vintage-inspired {chosen_trend} layout makes an incredible gift for birthdays, holidays, or special group events."

col1, col2 = st.columns(2)
with col1:
    st.text_input("📋 Product Title", value=seo_title[:60], key=f"title_{selected_slot}")
with col2:
    st.text_input("📋 Brand Name", value=seo_brand[:60], key=f"brand_{selected_slot}")

st.text_area("📋 Feature Bullet 1", value=seo_b1, height=65, key=f"b1_{selected_slot}")
st.text_area("📋 Feature Bullet 2", value=seo_b2, height=65, key=f"b2_{selected_slot}")
