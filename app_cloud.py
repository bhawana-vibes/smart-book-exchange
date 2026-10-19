import streamlit as st
import pandas as pd
import sqlite3

# Page Configuration
st.set_page_config(page_title="Smart Book Exchange", page_icon="📚", layout="centered")

st.title("📚 Smart Book Exchange Platform")
st.write("Middle-class aur underprivileged students ke liye safe, fair-price book sharing.")

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

tab1, tab2 = st.tabs(["➕ Nayi Book List Karein", "📖 Available Books Dekhein"])

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
        pickup_area = st.text_input("Aapka Area / Colony (e.g. Civil Lines, Nai Basti):")

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
            cursor.execute(query, (title, grade, mrp, cond, fair_price, seller_email, pickup_area))
            conn.commit()
            conn.close()

            st.success(f"✅ '{title}' successfully list ho gayi!")
            st.info(f"💰 Resale Price: ₹{fair_price} | Pickup Area: {pickup_area}")

# --- TAB 2: BUYER PORTAL ---
with tab2:
    st.subheader("📖 Kitabein Khareedein (Buyer Portal)")

    selected_class = st.selectbox("Apni Class Filter Karein:", ["All", 9, 10, 11, 12])

    conn = sqlite3.connect(DB_NAME)
    if selected_class == "All":
        query = "SELECT * FROM books WHERE status = 'AVAILABLE'"
        df = pd.read_sql(query, conn)
    else:
        query = f"SELECT * FROM books WHERE status = 'AVAILABLE' AND class_grade = {selected_class}"
        df = pd.read_sql(query, conn)
    conn.close()

    df.columns = [c.lower() for c in df.columns]

    if not df.empty:
        df['mrp'] = pd.to_numeric(df['mrp'], errors='coerce')
        df['resale_price'] = pd.to_numeric(df['resale_price'], errors='coerce')

        total_savings = (df['mrp'] - df['resale_price']).sum()
        st.metric("Total Student Savings Available", f"₹{round(total_savings, 2)}")
        st.divider()

        for index, row in df.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"### 📚 {row['book_title']}")
                    st.write(f"**Class:** {row['class_grade']} | **Condition:** {row['book_condition']}")
                    st.write(f"📍 **Pickup Area:** {row.get('pickup_area', 'Local Area')}")
                    st.write(f"💰 **Price: ₹{row['resale_price']}** *(Asli MRP: ₹{row['mrp']})*")

                with col2:
                    buyer_email_input = st.text_input("Apna Email daalein:", key=f"email_{row['book_id']}")
                    if st.button("Confirm & Claim", key=f"buy_{row['book_id']}"):
                        if not buyer_email_input.strip():
                            st.warning("Pehle apna email daalein!")
                        else:
                            up_conn = sqlite3.connect(DB_NAME)
                            up_cursor = up_conn.cursor()
                            update_query = "UPDATE books SET status = 'SOLD', buyer_email = ? WHERE book_id = ?"
                            up_cursor.execute(update_query, (buyer_email_input, row['book_id']))
                            up_conn.commit()
                            up_conn.close()

                            st.success("🎉 Order Confirmed!")
                            st.info(f"Seller ka Email: **{row.get('seller_email')}**\n\nPickup Area: **{row.get('pickup_area')}**\n\nInse email par coordinate karein.")
                            st.rerun()

                st.write("---")
    else:
        st.info("Abhi is class ke liye koi book available nahi hai.")