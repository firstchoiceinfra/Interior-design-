import streamlit as st
import time

# पेज कॉन्फ़िगरेशन
st.set_page_config(
    page_title="AI Interior & Mandir Designer",
    page_icon="🛋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. कस्टम CSS - आधुनिक लुक और स्मूथ ट्रांजिशन के लिए
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(90deg, #f59e0b, #ea580c);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. स्टेट मैनेजमेंट (ताकि डेटा कभी रीलोड पर गायब न हो)
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "नया डिज़ाइन बनाएं"
if "results" not in st.session_state:
    st.session_state.results = []

# 3. लैग-फ्री साइडबार (Persistent Sidebar)
with st.sidebar:
    st.markdown("## ✨ **AI Studio**")
    st.caption("स्मार्ट इंटीरियर व मंदिर प्लानर")
    st.divider()
    
    # यह मेनू कभी रीलोड नहीं होगा
    selected_page = st.radio(
        "नेविगेशन",
        ["नया डिज़ाइन बनाएं", "गैलरी (Saved Designs)", "सेटिंग्स"],
        label_visibility="collapsed"
    )
    st.session_state.active_tab = selected_page

# 4. मुख्य कंटेंट (इंस्टेंट स्विचिंग)
if st.session_state.active_tab == "नया डिज़ाइन बनाएं":
    st.title("🛋️ ऑटोमैटिक AI इंटीरियर डिज़ाइनर")
    st.write("अपने हॉल/कमरे की खाली फोटो डालें, फर्नीचर व मंदिर चुनें और 4 अलग-अलग लेआउट देखें।")

    col1, col2, col3 = st.columns([1.2, 1, 1])

    with col1:
        st.subheader("1. फोटो अपलोड करें")
        uploaded_file = st.file_uploader("कमरे की फोटो चुनें", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="आपकी ओरिजिनल फोटो", use_container_width=True)

    with col2:
        st.subheader("2. सोफ़ा स्टाइल")
        sofa_type = st.selectbox(
            "सोफ़ा का प्रकार चुनें:",
            ["L-Shape Corner Sofa (लक्ज़री)", "3+1+1 Classic Setup", "Curved Modern Lounge", "Compact 2-Seater + Recliner"]
        )

    with col3:
        st.subheader("3. मंदिर व लाइटिंग")
        mandir_type = st.selectbox(
            "मंदिर का प्रकार चुनें:",
            ["लकड़ी का नक्काशीदार मंदिर + वॉर्म LED", "व्हाइट मार्बल मंदिर + गोल्डन आर्क", "वॉल-माउंटेड फ्लोटिंग मंदिर", "जालीदार बैकड्रॉप + स्पॉटलाइट्स"]
        )

    st.markdown("---")

    # जनरेट बटन
    if st.button("🚀 4 अलग-अलग लेआउट जनरेट करें (East, West, North, Corner)", use_container_width=True):
        if not uploaded_file:
            st.warning("⚠️ कृपया पहले अपने कमरे की फोटो अपलोड करें!")
        else:
            with st.spinner("AI चारों दिशाओं के 4 अलग-अलग लेआउट तैयार कर रहा है..."):
                time.sleep(2)  # यहाँ आपकी AI API (Fal.ai / Replicate) कॉल होगी
                
                # 4 लेआउट्स का डेमो रिस्पॉन्स
                st.session_state.results = [
                    {"title": "लेआउट 1: सोफ़ा East Wall + मंदिर North-East (ईशान कोण)", "img": "https://picsum.photos/seed/layout1/800/600"},
                    {"title": "लेआउट 2: सोफ़ा West Side (ओपन हॉल लुक) + मंदिर East Wall", "img": "https://picsum.photos/seed/layout2/800/600"},
                    {"title": "लेआउट 3: सेंटर सोफ़ा सिटिंग + सेपरेट मंदिर कॉर्नर", "img": "https://picsum.photos/seed/layout3/800/600"},
                    {"title": "लेआउट 4: कॉम्पैक्ट L-कॉर्नर + वॉल-माउंटेड बैकलिट मंदिर", "img": "https://picsum.photos/seed/layout4/800/600"},
                ]
            st.success("✅ 4 नए लेआउट तैयार हैं!")

    # 4 लेआउट्स का ग्रिड डिस्प्ले
    if st.session_state.results:
        st.subheader("✨ आपके लिए जनरेट किए गए 4 विकल्प:")
        res_col1, res_col2 = st.columns(2)
        
        for idx, item in enumerate(st.session_state.results):
            target_col = res_col1 if idx % 2 == 0 else res_col2
            with target_col:
                st.image(item["img"], caption=item["title"], use_container_width=True)
                st.download_button(f"📥 डाउनलोड {idx+1}", data=b"dummy", file_name=f"layout_{idx+1}.jpg")

elif st.session_state.active_tab == "गैलरी (Saved Designs)":
    st.title("🖼️ आपकी सेव की गई डिज़ाइन्स")
    if st.session_state.results:
        for idx, item in enumerate(st.session_state.results):
            st.image(item["img"], caption=item["title"], width=400)
    else:
        st.info("अभी कोई सेव किया हुआ डिज़ाइन नहीं है।")

elif st.session_state.active_tab == "सेटिंग्स":
    st.title("⚙️ सेटिंग्स")
    st.text_input("AI API Key (Replicate / Fal.ai):", type="password")
