import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import arabic_reshaper
from bidi.algorithm import get_display

# دالة إصلاح النصوص العربية في الرسوم البيانية
def fix_arabic(text_to_fix):
    reshaped_text = arabic_reshaper.reshape(str(text_to_fix))
    return get_display(reshaped_text)

# 1. إعدادات الصفحة الرئيسية واجهة عريضة
st.set_page_config(page_title="منصة الخير الذكية والتعليمية", layout="wide", page_icon="📊")

# 2. توليد البيانات الضخمة وتثبيتها بشكل مستقل تماماً في الذاكرة السحابية
if 'df_donors' not in st.session_state:
    np.random.seed(42)
    n_records = 1000
    st.session_state.df_donors = pd.DataFrame({
        'المعرف': [f'D-{i}' for i in range(1, n_records + 1)],
        'الاسم': [f'متبرع {i}' for i in range(1, n_records + 1)],
        'العمر': np.random.randint(22, 70, size=n_records),
        'المدينة': np.random.choice(['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة'], size=n_records),
        'مجموع_التبرعات_السنوية_SAR': np.random.randint(1000, 15000, size=n_records),
        'عدد_مرات_التبرع': np.random.randint(1, 12, size=n_records),
        'احتمالية_التبرع_المستقبلي_%': np.random.randint(40, 99, size=n_records)
    })

if 'df_beneficiaries' not in st.session_state:
    np.random.seed(42)
    n_records = 1000
    st.session_state.df_beneficiaries = pd.DataFrame({
        'المعرف': [f'B-{i}' for i in range(1, n_records + 1)],
        'العائلة': [f'عائلة {i}' for i in range(1, n_records + 1)],
        'عدد_أفراد_الأسرة': np.random.randint(2, 9, size=n_records),
        'الدخل_الشهري_SAR': np.random.randint(1500, 6500, size=n_records),
        'نوع_الدعم_المطلوب': np.random.choice(['سكني', 'غذائي', 'صحي', 'تعليمي'], size=n_records),
        'حالة_الطلب': np.random.choice(['مقبول', 'قيد الدراسة', 'مكتمل'], size=n_records),
        'مستوى_الاحتياج_المتوقع_مستقبلا': np.random.choice(['مرتفع جداً', 'متوسط', 'مستقر'], size=n_records)
    })

# استدعاء الجداول من الذاكرة المستقرة
df_donors = st.session_state.df_donors
df_beneficiaries = st.session_state.df_beneficiaries

# دالة تحويل البيانات للتصدير
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8-sig')

# 3. واجهة التطبيق الرئيسية
st.title("📊 منصة الخير الذكية والتعليمية لعلم الإحصاء")
st.markdown("لوحة تحكم ذكية تعمل بكفاءة مطلقة ومحملة بالبيانات وميزة الرفع الجماعي من ملفات Excel.")
st.divider()

# 4. القائمة الجانبية للتنقل
with st.sidebar:
    st.title("⚙️ خيارات النظام")
    sidebar_choice = st.radio(
        "📍 انتقل إلى:", 
        [
            "لوحة تحكم المتبرعين", 
            "إدخل بيانات متبرعين ➕",
            "لوحة تحكم المستفيدين", 
            "إدخل بيانات مستفيدين ➕",
            "التحليلات التنبؤية (AI)", 
            "🧠 تعلم مفاهيم الإحصاء في هذا التطبيق",
            "البوت المساعد الذكي"
        ]
    )

# --- لوحة تحكم المتبرعين ---
if sidebar_choice == "لوحة تحكم المتبرعين":
    st.header("👥 قاعدة بيانات وإحصاءات المتبرعين")
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي المتبرعين", f"{len(df_donors)} متبرع")
    col2.metric("إجمالي التبرعات (SAR)", f"{df_donors['مجموع_التبرعات_السنوية_SAR'].sum():,}")
    col3.metric("متوسط التبرع", f"{int(df_donors['مجموع_التبرعات_السنوية_SAR'].mean()):,} SAR")
    
    st.download_button("📥 تحميل قاعدة البيانات الحالية (Excel/CSV)", data=convert_df_to_csv(df_donors), file_name='donors_database.csv', mime='text/csv')
    
    fig, ax = plt.subplots(figsize=(6, 4))
    city_counts = df_donors['المدينة'].value_counts()
    fixed_labels = [fix_arabic(label) for label in city_counts.index]
    ax.pie(city_counts, labels=fixed_labels, autopct='%1.1f%%', startangle=90)
    ax.set_title(fix_arabic('توزيع المتبرعين حسب المدن'))
    st.pyplot(fig)
    st.dataframe(df_donors, use_container_width=True)

# --- إدخال متبرع جديد (يدوي أو عبر إكسيل) ---
elif sidebar_choice == "إدخل بيانات متبرعين ➕":
    st.header("📝 إضافة بيانات المتبرعين")
    tab_manual, tab_excel = st.tabs(["✍️ إدخال يدوي لمتبرع واحد", "📁 رفع جماعي عبر ملف Excel / CSV"])
    
    with tab_manual:
        with st.form("donor_form", clear_on_submit=True):
            d_name = st.text_input("اسم المتبرع الكامل:")
            d_age = st.number_input("العمر:", min_value=18, max_value=100, value=35)
            d_city = st.selectbox("المدينة:", ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة'])
            d_amount = st.number_input("مجموع التبرعات السنوية (SAR):", min_value=0, value=1000)
            d_freq = st.number_input("عدد مرات التبرع في السنة:", min_value=1, value=2)
            submit_donor = st.form_submit_button("حفظ المتبرع اليدوي 💾")
            
            if submit_donor and d_name:
                new_row = {
                    'المعرف': f'D-{len(df_donors)+1}', 'الاسم': d_name, 'العمر': int(d_age), 
                    'المدينة': d_city, 'مجموع_التبرعات_السنوية_SAR': int(d_amount), 
                    'عدد_مرات_التبرع': int(d_freq), 'احتمالية_التبرع_المستقبلي_%': 85
                }
                st.session_state.df_donors = pd.concat([df_donors, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✅ تم حفظ المتبرع {d_name} بنجاح!")
                st.rerun()
                
    with tab_excel:
        st.subheader("📥 ارفع ملف البيانات دفعة واحدة")
        st.markdown("تأكد أن يحتوي ملف الإكسيل على الأعمدة التالية تماماً لتفادي الأخطاء: `الاسم`, `العمر`, `المدينة`, `مجموع_التبرعات_السنوية_SAR`, `عدد_مرات_التبرع`")
        
        uploaded_file = st.file_uploader("اختر ملف Excel أو CSV الخاص بالمتبرعين:", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                uploaded_df = pd.read_csv(uploaded_file)
            else:
                uploaded_df = pd.read_excel(uploaded_file)
            
            st.write("👀 عينة من البيانات المكتشفة داخل ملفك:")
            st.dataframe(uploaded_df.head(5))
            
            if st.button("🚀 دمج وتحديث قاعدة البيانات السحابية فوراً"):
                start_id = len(df_donors) + 1
                uploaded_df['المعرف'] = [f'D-{i}' for i in range(start_id, start_id + len(uploaded_df))]
                if 'احتمالية_التبرع_المستقبلي_%' not in uploaded_df.columns:
                    uploaded_df['احتمالية_التبرع_المستقبلي_%'] = np.random.randint(50, 95, size=len(uploaded_df))
                
                st.session_state.df_donors = pd.concat([df_donors, uploaded_df], ignore_index=True)
                st.success(f"🎉 نجاح! تم رفع ودمج {len(uploaded_df)} سجل متبرع جديد بنجاح وتحديث النظام التنبئي!")
                st.rerun()

# --- لوحة تحكم المستفيدين ---
elif sidebar_choice == "لوحة تحكم المستفيدين":
    st.header("🏡 قاعدة بيانات وإحصاءات المستفيدين")
    col1, col2, col3 = st.columns(3)
    col1.metric("عدد الأسر المستفيدة", f"{len(df_beneficiaries)} أسرة")
    col2.metric("متوسط دخل الأسرة", f"{int(df_beneficiaries['الدخل_الشهري_SAR'].mean()):,} SAR")
    col3.metric("متوسط عدد الأفراد", f"{int(df_beneficiaries['عدد_أفراد_الأسرة'].mean())} أفراد")
    
    st.download_button("📥 تحميل قاعدة البيانات الحالية (Excel/CSV)", data=convert_df_to_csv(df_beneficiaries), file_name='beneficiaries_database.csv', mime='text/csv')
    
    fig, ax = plt.subplots(figsize=(8, 4))
    df_fixed_b = df_beneficiaries.copy()
    df_fixed_b['نوع_الدعم_المطلوب'] = df_fixed_b['نوع_الدعم_المطلوب'].apply(fix_arabic)
    df_fixed_b['حالة_الطلب'] = df_fixed_b['حالة_الطلب'].apply(fix_arabic)
    sns.countplot(data=df_fixed_b, x='نوع_الدعم_المطلوب', hue='حالة_الطلب', ax=ax)
    ax.set_title(fix_arabic('توزيع نوع الدعم المطلوب'))
    st.pyplot(fig)
    st.dataframe(df_beneficiaries, use_container_width=True)

# --- إدخال مستفيد جديد (يدوي أو عبر إكسيل) ---
elif sidebar_choice == "إدخل بيانات مستفيدين ➕":
    st.header("📝 تسجيل حالات المستفيدين")
    tab_manual, tab_excel = st.tabs(["✍️ إدخال يدوي لحالة واحدة", "📁 رفع جماعي عبر ملف Excel / CSV"])
    
    with tab_manual:
        with st.form("beneficiary_form", clear_on_submit=True):
            b_family = st.text_input("اسم العائلة / المستفيد الرئيسي:")
            b_members = st.slider("عدد أفراد الأسرة:", 1, 15, 5)
            b_income = st.number_input("الدخل الشهري الحالي (SAR):", min_value=0, value=2000)
            b_type = st.selectbox("نوع الدعم المطلوب:", ['سكني', 'غذائي', 'صحي', 'تعليمي'])
            b_status = st.selectbox("حالة الطلب الحالية:", ['قيد الدراسة', 'مقبول', 'مكتمل'])
            submit_beneficiary = st.form_submit_button("حفظ المستفيد اليدوي 💾")
            
            if submit_beneficiary and b_family:
                new_row = {
                    'المعرف': f'B-{len(df_beneficiaries)+1}', 'العائلة': b_family, 'عدد_أفراد_الأسرة': int(b_members),
                    'الدخل_الشهري_SAR': int(b_income), 'نوع_الدعم_المطلوب': b_type, 'حالة_الطلب': b_status, 'مستوى_الاحتياج_المتوقع_مستقبلا': 'متوسط'
                }
                st.session_state.df_beneficiaries = pd.concat([df_beneficiaries, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✅ تم تسجيل العائلة {b_family} بنجاح!")
                st.rerun()
                
    with tab_excel:
        st.subheader("📥 ارفع ملف الحالات دفعة واحدة")
        st.markdown("تأكد أن يحتوي الملف على الأعمدة التالية تماماً: `العائلة`, `عدد_أفراد_الأسرة`, `الدخل_الشهري_SAR`, `نوع_الدعم_المطلوب`, `حالة_الطلب`")
        
        uploaded_file_b = st.file_uploader("اختر ملف Excel أو CSV الخاص بالمستفيدين:", type=['csv', 'xlsx'])
        if uploaded_file_b is not None:
            if uploaded_file_b.name.endswith('.csv'):
                uploaded_df_b = pd.read_csv(uploaded_file_b)
            else:
                uploaded_df_b = pd.read_excel(uploaded_file_b)
            
            st.write("👀 عينة من الحالات المكتشفة داخل ملفك:")
            st.dataframe(uploaded_df_b.head(5))
            
