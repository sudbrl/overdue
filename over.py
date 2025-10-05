# ------------------------------------------------------------------
#  STREAMLIT UI  (professional multi-file look)
# ------------------------------------------------------------------
st.set_page_config(page_title="Payment Due Report", layout="wide")

st.markdown("""
<style>
    /* ---------- page ----------
    .block-container { padding-top: 1rem; }
    .main-header { background:#0e1117; padding:1.2rem 0; border-radius:12px; margin-bottom:2rem; }
    .main-header h2 { color:#fafafa; text-align:center; margin:0; font-family:'Source Sans Pro',sans-serif; }
    /* ---------- upload ----------
    .uploadedFile { border:1px solid #e0e0e0; border-radius:8px; padding:1rem 1.2rem; margin:.6rem 0;
                    background:#fff; box-shadow:0 1px 3px rgba(0,0,0,.05); display:flex;
                    align-items:center; justify-content:space-between; }
    .fileName { font-weight:600; color:#303133; }
    /* ---------- download ----------
    .stDownloadButton > button { background:#0066cc; color:white; border:none;
                                 border-radius:8px; padding:.5rem 1.2rem; font-weight:600; }
    .stDownloadButton > button:hover { background:#0052a3; }
</style>""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h2>Payment Due Report Generator</h2></div>', unsafe_allow_html=True)

st.subheader("1. Drop your Excel files below")
st.caption("Up to 10 files · Sheet1 must contain the required columns")

uploaded_files = st.file_uploader(
    label="",
    type=["xlsx"],
    accept_multiple_files=True,
    key="uploader"
)

if uploaded_files:
    if len(uploaded_files) > 10:
        st.error("You can upload a maximum of 10 files at once.")
        st.stop()

    st.subheader("2. Download ready reports")
    for upl in uploaded_files:
        try:
            df_out = build_report(upl.getvalue())
            excel_bytes = style_excel(df_out)

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f'<div class="uploadedFile"><span class="fileName">📄 {upl.name}</span></div>',
                    unsafe_allow_html=True,
                )
            with col2:
                st.download_button(
                    label="📥 Download",
                    data=excel_bytes,
                    file_name=f"{Path(upl.name).stem}_Payment_Due_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dl_{upl.name}",  # unique key prevents duplicate widgets
                )
        except Exception as e:
            st.error(f"Processing **{upl.name}** failed: {e}")

    # explicit clean-up (even though we only used RAM)
    temp_dir = tempfile.gettempdir()
    for f in os.listdir(temp_dir):
        if f.startswith("tmp") and f.endswith(".xlsx"):
            try:
                os.remove(os.path.join(temp_dir, f))
            except:  # noqa
                pass
