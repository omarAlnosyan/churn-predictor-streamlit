import streamlit as st
import pickle
from sklearn.feature_extraction import DictVectorizer

# إعداد الصفحة
st.set_page_config(page_title="وَبَر", layout="centered")

# تنسيق واجهة داكنة متطورة
st.markdown("""
    <style>
    html, body, .main, .block-container, [class*="css"] {
        background-color: #071a2d !important;
        color: #f0f8ff !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: 19px;
    }
    h1 {
        font-size: 48px;
        color: #ffffff;
        font-weight: 900;
        text-align: center;
    }
    .stButton>button {
        background-color: #144272;
        color: white;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-size: 18px;
        margin-top: 10px;
        font-weight: bold;
        border: 1px solid #fff;
    }
    .stButton>button:hover {
        background-color: #205295;
        color: #fff;
        border-color: #b0d4ff;
    }
    .stSelectbox>div>div, .stNumberInput input {
        background-color: #102840;
        color: white;
        border-radius: 8px;
    }
.stSelectbox label, .stNumberInput label, .stTextInput label {
        color: #f0f8ff !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# تحميل النموذج
model_file = 'model_C=1.0.bin'
with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

# نظام تنقل بالزر
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# التنقل بالزر
if st.session_state.page == 'welcome':
    st.title("وَبَر")
    st.markdown("""
    <div style='text-align:center;'>
        <p style='font-size:22px;'>📞 في شركات الاتصالات، من الطبيعي إن بعض العملاء يفكرون يغيرون مزود الخدمة</p>
        <p style='font-size:22px;'>📊 هذا النموذج يساعدك تتوقع من ممكن يترك الخدمة من خلال بياناته</p>
        
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🚀 جرب النموذج الآن"):
        st.session_state.page = 'predict'
        st.rerun()

elif st.session_state.page == 'predict':
    st.title("🧠 أدخل بيانات العميل")
    st.markdown("""
<p style='text-align:center; font-size:22px; background-color:#121829; padding:10px 20px; border-radius:12px; display:inline-block;'>🧠 هنا تقدر تختار بيانات العميل اللي يتعامل مع جهتك، وتشوف هل ممكن يغادر الخدمة أو لا... خلنا نشوف 🤔🤔</p>
""", unsafe_allow_html=True)

    with st.form("churn_form"):
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox('الجنس', ['أنثى', 'ذكر'])
            seniorcitizen = st.selectbox('هل هو كبير سن؟', ['نعم', 'لا'])
            partner = st.selectbox('هل عنده شريك؟', ['نعم', 'لا'])
            dependents = st.selectbox('هل عنده معالين؟', ['نعم', 'لا'])
            phoneservice = st.selectbox('هل يستخدم الهاتف؟', ['نعم', 'لا'])
            multiplelines = st.selectbox('خطوط متعددة؟', ['نعم', 'لا', 'لا يوجد'])
            internetservice = st.selectbox('نوع الإنترنت', ['DSL', 'ألياف بصرية', 'لا يوجد'])

        with col2:
            onlinesecurity = st.selectbox('أمان الإنترنت', ['نعم', 'لا', 'لا يوجد إنترنت'])
            onlinebackup = st.selectbox('نسخ احتياطي؟', ['نعم', 'لا', 'لا يوجد إنترنت'])
            deviceprotection = st.selectbox('حماية الأجهزة؟', ['نعم', 'لا', 'لا يوجد إنترنت'])
            techsupport = st.selectbox('دعم فني؟', ['نعم', 'لا', 'لا يوجد إنترنت'])
            streamingtv = st.selectbox('بث تلفزيوني؟', ['نعم', 'لا', 'لا يوجد إنترنت'])
            streamingmovies = st.selectbox('أفلام؟', ['نعم', 'لا', 'لا يوجد إنترنت'])

        contract = st.selectbox('نوع العقد', ['month-to-month', 'one_year', 'two_year'])
        paperlessbilling = st.selectbox('فاتورة بدون ورق؟', ['yes', 'no'])
        paymentmethod = st.selectbox('طريقة الدفع', [
            'electronic_check', 'mailed_check', 'bank_transfer_(automatic)', 'credit_card_(automatic)'])
        tenure = st.number_input('مدة الاشتراك (بالأشهر)', min_value=0)
        monthlycharges = st.number_input('المبلغ الشهري', min_value=0.0)
        totalcharges = st.number_input('إجمالي المبلغ المدفوع', min_value=0.0)

        submitted = st.form_submit_button("🔮 احسب نسبة المغادرة")

        if submitted:
            customer = {
                'gender': gender,
                'seniorcitizen': seniorcitizen,
                'partner': partner,
                'dependents': 'نعم' if dependents == 'yes' else 'لا',
                'phoneservice': 'نعم' if phoneservice == 'yes' else 'لا',
                'multiplelines': 'لا يوجد خطوط إضافية' if multiplelines == 'no_phone_service' else ('نعم' if multiplelines == 'yes' else 'لا'),
                'internetservice': 'لا يوجد' if internetservice == 'no' else ('DSL' if internetservice == 'dsl' else 'ألياف بصرية'),
                'onlinesecurity': 'لا يوجد إنترنت' if onlinesecurity == 'no_internet_service' else ('نعم' if onlinesecurity == 'yes' else 'لا'),
                'onlinebackup': 'لا يوجد إنترنت' if onlinebackup == 'no_internet_service' else ('نعم' if onlinebackup == 'yes' else 'لا'),
                'deviceprotection': 'لا يوجد إنترنت' if deviceprotection == 'no_internet_service' else ('نعم' if deviceprotection == 'yes' else 'لا'),
                'techsupport': 'لا يوجد إنترنت' if techsupport == 'no_internet_service' else ('نعم' if techsupport == 'yes' else 'لا'),
                'streamingtv': 'لا يوجد إنترنت' if streamingtv == 'no_internet_service' else ('نعم' if streamingtv == 'yes' else 'لا'),
                'streamingmovies': 'لا يوجد إنترنت' if streamingmovies == 'no_internet_service' else ('نعم' if streamingmovies == 'yes' else 'لا'),
                'contract': 'شهري' if contract == 'month-to-month' else ('سنة' if contract == 'one_year' else 'سنتين'),
                'paperlessbilling': 'نعم' if paperlessbilling == 'yes' else 'لا',
                'paymentmethod': 'شيك إلكتروني' if paymentmethod == 'electronic_check' else ('شيك بالبريد' if paymentmethod == 'mailed_check' else ('تحويل تلقائي' if paymentmethod == 'bank_transfer_(automatic)' else 'بطاقة ائتمان')),
                'tenure': tenure,
                'monthlycharges': monthlycharges,
                'totalcharges': totalcharges
            }
            X = dv.transform([customer])
            y_pred = model.predict_proba(X)[0, 1]
            st.markdown(f"<h3 style='color:#00ff88;'>🔔 نسبة احتمالية مغادرة العميل: {y_pred:.2%}</h3>", unsafe_allow_html=True)

    if st.button("⬅️ العودة للواجهة الرئيسية"):
        st.session_state.page = 'welcome'
        st.rerun()
