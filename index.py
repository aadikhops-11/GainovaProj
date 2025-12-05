import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Recommendation Model", layout="wide")

# Background styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: url("background1.jpg");
    background-size: cover;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.65);
    z-index: -1;
}
.card {
    background-color: rgba(17, 17, 17, 0.85);
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(255,255,255,0.15);
    transition: 0.2s;
}
.card:hover {
    transform: scale(1.03);
}
.card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 8px;
}
.card-title {
    font-size: 1.05rem;
    font-weight: bold;
    color: #fff;
    margin-top: 8px;
}
.card-text {
    color: #ccc;
    font-size: 0.9rem;
    margin-bottom: 3px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------
# Title & Search Bar
# -----------------------------
st.markdown("<h1 style='text-align:center; color:white;'>Recommendation Model</h1>", unsafe_allow_html=True)

query = st.text_input("Search products...", "").lower()


# -----------------------------
# Load CSV
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("all_electronics.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Ensure placeholder logic
df["image"] = df["image"].fillna("")
df["image"] = df["image"].apply(lambda x: x if str(x).strip() != "" else "placeholder.png")

# Apply search filter
if query:
    df = df[df["name"].str.lower().str.contains(query)]

# -----------------------------
# Pagination
# -----------------------------
PRODUCTS_PER_PAGE = 100

if "count" not in st.session_state:
    st.session_state.count = PRODUCTS_PER_PAGE

# Slice the dataframe
subset = df.head(st.session_state.count)

# -----------------------------
# Display Cards
# -----------------------------
cols = st.columns(4)

for idx, row in subset.iterrows():
    col = cols[idx % 4]

    with col:
        st.markdown(
            f"""
            <div class="card">
                <img src="{row['image']}" onerror="this.src='placeholder.png'">
                <div class="card-title">{row['name']}</div>
                <div class="card-text">⭐ Rating: {row.get('rating', 'N/A')}</div>
                <div class="card-text">👥 Reviews: {row.get('numRatings', 0)}</div>
                <div class="card-text">💰 Price: ₹{row.get('discountPrice', '-')}</div>
                <div class="card-text"><s>₹{row.get('actualPrice', '-')}</s></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Clickable product link
        if pd.notna(row.get("link")) and str(row["link"]).strip() != "":
            st.link_button("View Product", row["link"])

        st.write("")


# -----------------------------
# Load More Button
# -----------------------------
if st.session_state.count < len(df):
    if st.button("Load More"):
        st.session_state.count += PRODUCTS_PER_PAGE
        st.rerun()
