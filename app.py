import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import PyPDF2

st.set_page_config(page_title="Spanish Reader", layout="wide")

st.title("📖 Spanish Vocabulary Reader")

# -----------------------
# Επιλογή input
# -----------------------
option = st.radio("Διάλεξε τρόπο εισαγωγής:", ["Paste Text", "Upload File"])

text = ""

# -----------------------
# Paste
# -----------------------
if option == "Paste Text":
    text = st.text_area("Επικόλλησε ισπανικό κείμενο εδώ:")

# -----------------------
# Upload
# -----------------------
elif option == "Upload File":
    uploaded_file = st.file_uploader("Ανέβασε αρχείο (.txt ή .pdf)", type=["txt", "pdf"])

    if uploaded_file:
        if uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            pages = []
            for page in reader.pages:
                pages.append(page.extract_text())
            text = "\n".join(pages)

# -----------------------
# Γλώσσα μετάφρασης
# -----------------------
lang = st.selectbox("Μετάφραση σε:", ["Greek", "English"])

target_lang = "el" if lang == "Greek" else "en"

# -----------------------
# CSV storage
# -----------------------
if "words_data" not in st.session_state:
    st.session_state.words_data = []

# -----------------------
# Εμφάνιση λέξεων
# -----------------------
if text:
    st.subheader("📌 Κάνε click σε λέξη:")

    words = text.split()

    cols = st.columns(8)

    for i, word in enumerate(words):
        clean_word = word.strip(".,;:!?¡¿()\"'")

        if clean_word == "":
            continue

        col = cols[i % 8]

        if col.button(clean_word):
            try:
                translation = GoogleTranslator(source='auto', target=target_lang).translate(clean_word)
            except:
                translation = "Error"

            st.success(f"{clean_word} → {translation}")

            st.session_state.words_data.append({
                "word": clean_word,
                "translation": translation
            })

# -----------------------
# Download CSV
# -----------------------
if st.session_state.words_data:
    df = pd.DataFrame(st.session_state.words_data)

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="💾 Κατέβασε τις λέξεις (CSV)",
        data=csv,
        file_name="unknown_words.csv",
        mime="text/csv"
    )

# -----------------------
# Clear button
# -----------------------
if st.button("❌ Καθαρισμός λέξεων"):
    st.session_state.words_data = []
