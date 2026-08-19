import streamlit as st
import time

# पेज सेटअप
st.set_page_config(page_title="Instant AI Interior", page_icon="⚡", layout="wide")

# CSS: स्मूथ ट्रांज़िशन और फास्ट UI
st.markdown("""
<style>
    div[data-baseweb="tab-list"] { gap: 10px; }
    button[data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
        padding: 10px 20px;
        border-radius: 8px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# स्टेट इनिशियलाइज़ेशन
if "layouts" not in st.session_state:
    st.session_state.layouts = []

# क्लाइंट-साइड 0-लैग नेविगेशन टैब्स (1-क्लिक इंस्टेंट स्विच)
tab_design, tab_gallery, tab_settings = st.tabs([
    "✨ नया डिज़ाइन बनाएं", 
    "🖼️ सेव की गई गैलरी", 
    "⚙️ सेटिंग्स"
])

# --- TAB 1: DESIGN STUDIO ---
with tab_design:
    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.subheader("1. इनपुट और विकल्प")
        uploaded_file = st.file_uploader("कमरे की खाली फोटो डालें", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="अपलोड की गई फोटो", use_container_width=True)

        # 1-क्लिक चॉइस बटन्स (Pills / Segmented Controls)
        st.markdown("**सोफ़ा स्टाइल:**")
        sofa_choice = st.pills(
            "सोफ़ा स्टाइल",
            ["L-Shape Corner", "3+1+1 Classic", "Curved Lounge", "Modular 2-Seater"],
            default="L-Shape Corner",
            label_visibility="collapsed"
        )

        st.markdown("**मंदिर का प्रकार व बैकड्रॉप:**")
        mandir_choice = st.pills(
            "मंदिर स्टाइल",
            ["Wood + Warm LED", "White Marble Arch", "Floating Jaali Unit", "Corner Glass Setup"],
            default="Wood + Warm LED",
            label_visibility="collapsed"
        )

        generate_btn = st.button("🚀 4 अलग-अलग लेआउट बनाएं")

    with col_right:
        st.subheader("2. AI लेआउट परिणाम")
        
        # फ्रैग्मेंट: जनरेशन केवल इसी ब्लॉक को प्रोसेस करेगा, पूरा पेज स्टेबल रहेगा
        @st.fragment
        def render_layouts(clicked):
            if clicked:
                if not uploaded_file:
                    st.warning("कृपया पहले कमरे की फोटो अपलोड करें!")
                    return
                
                with st.spinner("AI 4 अलग-अलग दिशाओं के लेआउट तैयार कर रहा है..."):
                    time.sleep(1.5)  # API Call Simulation
                    st.session_state.layouts = [
                        {"title": f"लेआउट 1 (East Wall): {sofa_choice} + North {mandir_choice}", "img": "https://picsum.photos/seed/lay1/600/400"},
                        {"title": f"लेआउट 2 (West Wall): {sofa_choice} + Corner {mandir_choice}", "img": "https://picsum.photos/seed/lay2/600/400"},
                        {"title": f"लेआउट 3 (Center Setup): {sofa_choice} + East {mandir_choice}", "img": "https://picsum.photos/seed/lay3/600/400"},
                        {"title": f"लेआउट 4 (Compact Plan): {sofa_choice} + Floating {mandir_choice}", "img": "https://picsum.photos/seed/lay4/600/400"}
                    ]

            if st.session_state.layouts:
                g_col1, g_col2 = st.columns(2)
                for idx, item in enumerate(st.session_state.layouts):
                    target = g_col1 if idx % 2 == 0 else g_col2
                    with target:
                        st.image(item["img"], caption=item["title"], use_container_width=True)
            else:
                st.info("विकल्प चुनकर '4 अलग-अलग लेआउट बनाएं' पर क्लिक करें।")

        render_layouts(generate_btn)

# --- TAB 2: GALLERY ---
with tab_gallery:
    st.subheader("गैलरी और डाउनलोड्स")
    if st.session_state.layouts:
        cols = st.columns(4)
        for idx, item in enumerate(st.session_state.layouts):
            with cols[idx]:
                st.image(item["img"], caption=f"Variant #{idx+1}", use_container_width=True)
                st.download_button(f"डाउनलोड #{idx+1}", data=b"dummy_bytes", file_name=f"layout_{idx+1}.jpg")
    else:
        st.caption("कोई सेव किया हुआ लेआउट उपलब्ध नहीं है।")

# --- TAB 3: SETTINGS ---
with tab_settings:
    st.subheader("API और क्लाउड सेटिंग्स")
    st.text_input("Replicate / Fal.ai API Key", type="password")
    st.toggle("हाई-रिज़ॉल्यूशन 4K रेंडरिंग चालू करें", value=True)
