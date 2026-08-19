import streamlit as st
import replicate
import tempfile
import os
from PIL import Image

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(
    page_title="AI Interior & Mandir Planner", 
    page_icon="🛋️", 
    layout="wide"
)

# कस्टम स्टाइलिंग (लैग-फ्री और मॉडर्न लुक)
st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f8fafc; }
    div[data-baseweb="tab-list"] { gap: 8px; margin-bottom: 20px; }
    button[data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
        padding: 8px 16px;
        border-radius: 8px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #f59e0b, #ea580c);
        color: white;
        font-weight: bold;
        padding: 12px;
        border-radius: 8px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# 2. स्टेट इनिशियलाइज़ेशन
if "generated_layouts" not in st.session_state:
    st.session_state.generated_layouts = []

# 3. AI जनरेशन फंक्शन (एरर-फ्री फ़ाइल हैंडलिंग के साथ)
def run_interior_ai(image_file, sofa_style, mandir_style, api_token):
    os.environ["REPLICATE_API_TOKEN"] = api_token
    
    # इमेज को अस्थायी फ़ाइल में सेव करना ताकि API एरर न दे
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(image_file.getvalue())
        tmp_path = tmp_file.name

    # 4 अलग-अलग लेआउट प्रॉम्प्ट्स
    prompts = [
        f"Interior architecture photography of living room, placing luxury {sofa_style} along East wall, elegant {mandir_style} with warm golden backlight in North-East corner, modern Indian apartment, warm spotlights, 8k realistic",
        f"Modern hall interior, {sofa_style} arranged along West wall creating spacious walking aisle, divine {mandir_style} placed on elevated platform, architectural lighting, photo realistic",
        f"Cozy hall arrangement, centered {sofa_style} with coffee table, dedicated partition with {mandir_style} and brass diyas, ambient warm interior lights",
        f"Sleek minimalist living room, compact {sofa_style} against main wall, wall-mounted {mandir_style} with intricate backlit jaali, 8k render"
    ]

    results = []
    
    try:
        for idx, prompt_text in enumerate(prompts):
            with open(tmp_path, "rb") as file_handle:
                # वर्किंग SDXL ControlNet / Interior Reconstruct Model
                output = replicate.run(
                    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    input={
                        "image": file_handle,
                        "prompt": prompt_text,
                        "negative_prompt": "mountains, trees, outdoor, nature, blurry, deformed furniture, dark, bad quality",
                        "prompt_strength": 0.75,
                        "num_outputs": 1
                    }
                )
                
                # इमेज URL निकालना
                img_url = output[0] if isinstance(output, list) else str(output)
                results.append({
                    "title": f"लेआउट #{idx+1}",
                    "desc": prompt_text,
                    "url": img_url
                })
    finally:
        # प्रोसेस के बाद टेम्परेरी फाइल डिलीट करना
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
    return results

# 4. 0-लैग टैब नेविगेशन
tab_create, tab_gallery = st.tabs(["✨ नया लेआउट बनाएं", "🖼️ गैलरी व डाउनलोड्स"])

# --- TAB 1: CREATE ---
with tab_create:
    col_input, col_output = st.columns([1, 1.2], gap="large")

    with col_input:
        st.subheader("1. सेटिंग्स व फोटो")
        
        # API Key इनपुट (सुरक्षित तरीके से)
        api_key = st.text_input(
            "Replicate API Token दर्ज करें:", 
            type="password", 
            help="replicate.com से अपनी r8_... वाली चाबी यहाँ डालें"
        )
        
        uploaded_file = st.file_uploader("कमरे/हॉल की खाली फोटो चुनें", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="आपकी ओरिजिनल फोटो", use_container_width=True)

        st.markdown("---")
        st.markdown("**सोफ़ा का प्रकार चुनें:**")
        sofa_choice = st.selectbox(
            "सोफ़ा स्टाइल",
            ["L-Shape Corner Sofa", "3+1+1 Classic Lounge", "Curved Modern Sofa", "2-Seater Modular Sofa"],
            label_visibility="collapsed"
        )

        st.markdown("**मंदिर का डिज़ाइन व बैकड्रॉप चुनें:**")
        mandir_choice = st.selectbox(
            "मंदिर स्टाइल",
            ["लकड़ी का नक्काशीदार मंदिर + वॉर्म LED", "व्हाइट मार्बल मंदिर + गोल्डन आर्क", "वॉल-माउंटेड फ्लोटिंग जालीदार मंदिर", "कॉम्पैक्ट वुडन मंदिर + पीतल दीया सेटअप"],
            label_visibility="collapsed"
        )

        generate_clicked = st.button("🚀 4 अलग-अलग लेआउट्स जनरेट करें")

    with col_output:
        st.subheader("2. AI लेआउट परिणाम")

        if generate_clicked:
            if not api_key:
                st.error("❌ कृपया पहले Replicate API Token दर्ज करें!")
            elif not uploaded_file:
                st.warning("⚠️ कृपया पहले अपने कमरे की फोटो अपलोड करें!")
            else:
                with st.spinner("AI 4 अलग-अलग दिशाओं के लेआउट तैयार कर रहा है (लगभग 10-15 सेकंड)..."):
                    try:
                        layouts = run_interior_ai(uploaded_file, sofa_choice, mandir_choice, api_key)
                        st.session_state.generated_layouts = layouts
                        st.success("✅ 4 लेआउट्स सफलतापूर्वक तैयार हो गए!")
                    except Exception as e:
                        st.error(f"एरर आया: {str(e)}")

        # परिणाम दिखाना
        if st.session_state.generated_layouts:
            g_col1, g_col2 = st.columns(2)
            for i, layout in enumerate(st.session_state.generated_layouts):
                target_col = g_col1 if i % 2 == 0 else g_col2
                with target_col:
                    st.image(layout["url"], caption=layout["title"], use_container_width=True)
        else:
            st.info("बाएं तरफ फोटो अपलोड करके 'जनरेट करें' बटन दबाएं।")

# --- TAB 2: GALLERY ---
with tab_gallery:
    st.subheader("सेव किए गए लेआउट्स")
    if st.session_state.generated_layouts:
        cols = st.columns(4)
        for i, layout in enumerate(st.session_state.generated_layouts):
            with cols[i]:
                st.image(layout["url"], caption=layout["title"], use_container_width=True)
    else:
        st.caption("अभी कोई लेआउट जनरेट नहीं हुआ है।")
