# 📚 Smart Book Exchange

Har saal naye session par kitabein khareedna middle-class families aur zarooratmand students ke liye kaafi mehenga padta hai. Dusri taraf, purane students apni pichli saal ki kitabein ya toh raddi mein bech dete hain ya wo ghar par dhool khati rehti hain.

Yeh project ek simple local platform hai jahan Class 9th se 12th ke students apni purani kitabein fair price par exchange kar sakte hain.

---

###  Yeh Project Kya Karta Hai?

1. **Fair Resale Price:** Kitab ki condition (Good / Average) dekh kar system khud ek sahi daam calculate karta hai, taaki na seller ka nuksan ho aur na buyer se zyada paise liye jayein.
2. **Safe Local Handover:** Koi online payment ya delivery charges ka jhanjhat nahi. Buyer aur seller ek hi mohalle ya school area ke hote hain, toh wo email ke zariye aapas mein coordinate karke aaram se kitab le-de sakte hain.
3. **Student Savings Tracker:** Platform par live dikhta hai ki purani kitabein lene se total kitne rupaye bache.

---

### Tech Stack (Maine Kya Use Kiya?)

- **Python:** Saara core logic aur pricing rules likhne ke liye.
- **MySQL:** Kitabon ka record, price, condition aur pickup area save karne ke liye.
- **Pandas:** Database se live data pull karke total bachat (savings) calculate karne ke liye.
- **Streamlit:** Ek aasan web interface banane ke liye jahan seller kitab list kare aur buyer apni class filter karke book claim kar sake.

---

###  Apne System Par Kaise Chalayein?

1. Saari zaroori libraries install karein:
   ```bash
   pip install streamlit pandas mysql-connector-python

2. MySQL Workbench mein `book_exchange` database aur `books` table banayein.

3. Code mein apna local MySQL password dalein aur run karein:
   ```bash
   python -m streamlit run app.py
   ```