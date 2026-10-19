import sqlite3
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Smart Book Exchange", page_icon="📚", layout="centered"
)

st.title("📚 Smart Book Exchange Platform")
st.write(
    "Middle-class aur underprivileged students ke liye safe, fair-price book"
    " sharing."
)

# Database Initialization (SQLite)
DB_NAME = "books_data.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_title TEXT NOT NULL,
        class_grade INTEGER NOT NULL,
        mrp REAL NOT NULL,
        book_condition TEXT NOT NULL,
        resale_price REAL NOT NULL,
        status TEXT DEFAULT 'AVAILABLE',
        seller_email TEXT,
        pickup_area TEXT,
        buyer_email TEXT
    );
    """)
  conn.commit()
  conn.close()


# Initialize DB on load
init_db()

# 3 Tabs Setup
tab1, tab2, tab3 = st.tabs([
    "➕ Nayi Book List Karein",
    "📖 Available Books Dekhein",
    "📊 Data Science & Analytics",
])

# --- TAB 1: SELLER FORM ---
with tab1:
  st.subheader("Kitab aur Pickup Details Dalein")

  col_a, col_b = st.columns(2)
  with col_a:
    title = st.text_input("Kitab ka Naam (Title):")
    grade = st.selectbox("Class chunein:", [9, 10, 11, 12])
    mrp = st.number_input("Asli MRP (₹):", min_value=10.0, step=10.0)

  with col_b:
    cond = st.selectbox("Condition kaisi hai?", ["Good", "Average"])
    seller_email = st.text_input("Aapka Email (Seller Email):")
    pickup_area = st.text_input(
        "Aapka Area / Colony (e.g. Civil Lines, Nai Basti):"
    )

  if st.button("Calculate & List Book"):
    if not title.strip() or not seller_email.strip() or not pickup_area.strip():
      st.error("Kripya Kitab ka naam, Email aur Area sabhi zaroor bharein!")
    else:
      rate = 0.50 if cond == "Good" else 0.40
      fair_price = round(mrp * rate, 2)

      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      query = """
            INSERT INTO books (book_title, class_grade, mrp, book_condition, resale_price, seller_email, pickup_area)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
      cursor.execute(
          query,
          (title, grade, mrp, cond, fair_price, seller_email, pickup_area),
      )
      conn.commit()
      conn.close()

      st.success(f"✅ '{title}' successfully list ho gayi!")
      st.info(f"💰 Resale Price: ₹{fair_price} | Pickup Area: {pickup_area}")

# --- TAB 2: BUYER PORTAL ---
with tab2:
  st.subheader("📖 Kitabein Khareedein (Buyer Portal)")

  selected_class = st.selectbox(
      "Apni Class Filter Karein:", ["All", 9, 10, 11, 12]
  )

  conn = sqlite3.connect(DB_NAME)
  if selected_class == "All":
    query = "SELECT * FROM books WHERE status = 'AVAILABLE'"
    df = pd.read_sql(query, conn)
  else:
    query = (
        "SELECT * FROM books WHERE status = 'AVAILABLE' AND class_grade ="
        f" {selected_class}"
    )
    df = pd.read_sql(query, conn)
  conn.close()

  df.columns = [c.lower() for c in df.columns]

  if not df.empty:
    df["mrp"] = pd.to_numeric(df["mrp"], errors="coerce")
    df["resale_price"] = pd.to_numeric(df["resale_price"], errors="coerce")

    total_savings = (df["mrp"] - df["resale_price"]).sum()
    st.metric(
        "Total Student Savings Available", f"₹{round(total_savings, 2)}"
    )
    st.divider()

    for index, row in df.iterrows():
      with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
          st.markdown(f"### 📚 {row['book_title']}")
          st.write(
              f"**Class:** {row['class_grade']} | **Condition:**"
              f" {row['book_condition']}"
          )
          st.write(f"📍 **Pickup Area:** {row.get('pickup_area', 'Local Area')}")
          st.write(
              f"💰 **Price: ₹{row['resale_price']}** *(Asli MRP: ₹{row['mrp']})*"
          )

        with col2:
          buyer_email_input = st.text_input(
              "Apna Email daalein:", key=f"email_{row['book_id']}"
          )
          if st.button("Confirm & Claim", key=f"buy_{row['book_id']}"):
            if not buyer_email_input.strip():
              st.warning("Pehle apna email daalein!")
            else:
              up_conn = sqlite3.connect(DB_NAME)
              up_cursor = up_conn.cursor()
              update_query = (
                  "UPDATE books SET status = 'SOLD', buyer_email = ? WHERE"
                  " book_id = ?"
              )
              up_cursor.execute(
                  update_query, (buyer_email_input, row["book_id"])
              )
              up_conn.commit()
              up_conn.close()

              st.success("🎉 Order Confirmed!")
              st.info(
                  f"Seller ka Email: **{row.get('seller_email')}**\n\nPickup"
                  f" Area: **{row.get('pickup_area')}**\n\nInse email par"
                  " coordinate karein."
              )
              st.rerun()

        st.write("---")
  else:
    st.info("Abhi is class ke liye koi book available nahi hai.")

# --- TAB 3: DATA SCIENCE & ANALYTICS DASHBOARD ---
with tab3:
  st.subheader("📈 Platform Data Analytics & Community Insights")

  conn = sqlite3.connect(DB_NAME)
  df_all = pd.read_sql("SELECT * FROM books", conn)
  conn.close()

  if not df_all.empty:
    df_all.columns = [c.lower() for c in df_all.columns]
    df_all["mrp"] = pd.to_numeric(df_all["mrp"], errors="coerce")
    df_all["resale_price"] = pd.to_numeric(
        df_all["resale_price"], errors="coerce"
    )
    df_all["savings"] = df_all["mrp"] - df_all["resale_price"]

    # Key Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    total_books = len(df_all)
    sold_books = len(df_all[df_all["status"] == "SOLD"])
    total_community_savings = df_all["savings"].sum()

    col_m1.metric("Total Books Logged", total_books)
    col_m2.metric("Exchanges (Sold)", sold_books)
    col_m3.metric(
        "Total Community Savings", f"₹{round(total_community_savings, 2)}"
    )

    st.divider()

    # Chart 1: Class-wise Distribution
    st.markdown("#### 📚 Book Distribution by Class")
    class_counts = df_all["class_grade"].value_counts().sort_index()
    st.bar_chart(class_counts)

    # Chart 2: Inventory Status Breakdown
    st.markdown("#### 🔄 Inventory Flow (Status)")
    status_counts = df_all["status"].value_counts()
    st.bar_chart(status_counts)

    # Statistical Summary
    st.markdown("#### 📐 Statistical Summary (Pricing & Savings)")
    stats_df = df_all[["mrp", "resale_price", "savings"]].describe().round(2)
    st.dataframe(stats_df, use_container_width=True)

  else:
    st.info("Analytics generate karne ke liye pehle kuch books list karein.")