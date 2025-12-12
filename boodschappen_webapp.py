import streamlit as st
import json
import os
from collections import Counter

# ---------------------------
# Bestanden voor opslag
# ---------------------------
BESTAND = "boodschappenlijst.json"
HISTORY_BESTAND = "koopgeschiedenis.json"

# ---------------------------
# Data laden en opslaan
# ---------------------------
def laad_data():
    if not os.path.exists(BESTAND):
        with open(BESTAND, "w") as f:
            json.dump([], f)
    if not os.path.exists(HISTORY_BESTAND):
        with open(HISTORY_BESTAND, "w") as f:
            json.dump([], f)
    with open(BESTAND, "r") as f:
        lijst = json.load(f)
    with open(HISTORY_BESTAND, "r") as f:
        geschiedenis = json.load(f)
    return lijst, geschiedenis

def sla_data_op(lijst, geschiedenis):
    with open(BESTAND, "w") as f:
        json.dump(lijst, f, indent=4)
    with open(HISTORY_BESTAND, "w") as f:
        json.dump(geschiedenis, f, indent=4)

# ---------------------------
# Suggesties
# ---------------------------
def suggesties(geschiedenis, huidige_lijst):
    counter = Counter(geschiedenis)
    veel_gekocht = [p for p,_ in counter.most_common(5)]
    return [p for p in veel_gekocht if p not in huidige_lijst]

# ---------------------------
# Streamlit pagina instellingen
# ---------------------------
st.set_page_config(page_title="Slimme Boodschappenlijst", layout="wide")

st.title("🛒 Slimme Boodschappenlijst")

# Session state voor herladen
if 'refresh' not in st.session_state:
    st.session_state['refresh'] = False

lijst, geschiedenis = laad_data()

# ---------------------------
# Sidebar voor toevoegen
# ---------------------------
st.sidebar.header("Product toevoegen")
nieuw_product = st.sidebar.text_input("Nieuw product")
if st.sidebar.button("Toevoegen"):
    if nieuw_product.strip():
        lijst.append(nieuw_product.strip())
        geschiedenis.append(nieuw_product.strip())
        sla_data_op(lijst, geschiedenis)
        st.success(f"{nieuw_product.strip()} toegevoegd!")
        st.session_state['refresh'] = not st.session_state['refresh']

# ---------------------------
# Boodschappenlijst tonen
# ---------------------------
st.subheader("📋 Jouw boodschappenlijst")
if not lijst:
    st.info("Je lijst is nog leeg!")
else:
    for i, prod in enumerate(lijst):
        col1, col2, col3 = st.columns([5,1,1])
        col1.markdown(f"**{i+1}. {prod}**")
        
        # Product wijzigen
        wijzig_key = f"wijzig_{i}"
        if col2.button("✏️", key=wijzig_key):
            nieuw = st.text_input(f"Wijzig product {prod}", key=f"input_{i}")
            if st.button("Bevestig wijziging", key=f"confirm_{i}"):
                if nieuw.strip():
                    lijst[i] = nieuw.strip()
                    sla_data_op(lijst, geschiedenis)
                    st.session_state['refresh'] = not st.session_state['refresh']
        
        # Product verwijderen
        del_key = f"del_{i}"
        if col3.button("❌", key=del_key):
            lijst.pop(i)
            sla_data_op(lijst, geschiedenis)
            st.session_state['refresh'] = not st.session_state['refresh']

# ---------------------------
# Suggesties
# ---------------------------
st.subheader("💡 Suggesties voor je lijst")
sug = suggesties(geschiedenis, lijst)
if sug:
    for i, s in enumerate(sug):
        if st.button(f"Voeg toe: {s}", key=f"sug_{i}"):
            lijst.append(s)
            sla_data_op(lijst, geschiedenis)
            st.session_state['refresh'] = not st.session_state['refresh']
else:
    st.info("Geen suggesties op dit moment.")

# ---------------------------
# Extra styling / kleuren
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #fdf6e3;
}
h1, h2, h3 {
    color: #073642;
}
</style>
""", unsafe_allow_html=True)
