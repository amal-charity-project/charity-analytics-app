import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic(text_to_fix):
    reshaped = arabic_reshaper.reshape(str(text_to_fix))
    return get_display(reshaped)

st.set_page_config(
    page_title="منصة الخير الذكية", 
    layout="wide", 
    page_icon="📊"
)

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

df_donors = st.session_state.df_donors
df_beneficiaries = st.session_state.df_beneficiaries

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8-sig')

st.title("📊 منصة الخير الذكية والتعليمية")
st.markdown("لوحة تحكم ذكية تعمل بكفاءة مطلقة ومحملة بالبيانات.")
st.divider()

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

if sidebar_choice == "لوحة تحكم المتبرعين":
    st.header("👥 قاعدة بيانات وإحصاءات المتبرعين")
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي المتبرعين", f"{len(df_donors)} متبرع")
    col2.metric("إجمالي التبرعات (SAR)", f"{df_donors['مجموع_التبرعات_السنوية_SAR'].sum():,}")
    col3.metric("متوسط التبرع", f"{int(df_donors['مجموع_التبرعات_السنوية_SAR'].mean()):,} SAR")
    
    st.download_button("📥 تحميل قاعدة البيانات", data=convert_df_to_csv(df_donors), file_name='donors_database.csv', mime='text/csv')
    
    fig, ax = plt.subplots(figsize=(6, 4))
    city_counts = df_donors['المدينة'].value_counts()
    fixed_labels = [fix_arabic(lbl) for lbl in city_counts.index]
    ax.pie(city_counts, labels=fixed_labels, autopct='%1.1f%%', startangle=90)
    ax.set_title(fix_arabic('توزيع المتبرعين حسب المدن'))
    st.pyplot(fig)
    st.dataframe(df_donors, use_container_width=True)
elif sidebar_choice == "إدخل بيانات متبرعين ➕":
    st.header("📝 إضافة بيانات المتبرعين")
    tab_manual, tab_excel = st.tabs(["✍️ إدخال يدوي", "📁 رفع جماعي Excel"])
    
    with tab_manual:
        with st.form("donor_form", clear_on_submit=True):
            d_name = st.text_input("اسم المتبرع الكامل:")
            d_age = st.number_input("العمر:", min_value=18, max_value=100, value=35)
            d_city = st.selectbox("المدينة:", ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة'])
            d_amount = st.number_input("مجموع التبرعات السنوية:", min_value=0, value=1000)
            d_freq = st.number_input("عدد مرات التبرع سنوياً:", min_value=1, value=2)
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
        uploaded_file = st.file_uploader("اختر ملف Excel أو CSV:", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                uploaded_df = pd.read_csv(uploaded_file)
            else:
                uploaded_df = pd.read_excel(uploaded_file)
            
            st.write("👀 عينة من البيانات المكتشفة:")
            st.dataframe(uploaded_df.head(5))
            
            if st.button("🚀 دمج وتحديث قاعدة البيانات فوراً"):
                start_id = len(df_donors) + 1
                uploaded_df['المعرف'] = [f'D-{i}' for i in range(start_id, start_id + len(uploaded_df))]
                if 'احتمالية_التبرع_المستقبلي_%' not in uploaded_df.columns:
                    uploaded_df['احتمالية_التبرع_المستقبلي_%'] = np.random.randint(50, 95, size=len(uploaded_df))
                st.session_state.df_donors = pd.concat([df_donors, uploaded_df], ignore_index=True)
                st.success("🎉 تم دمج السجلات بنجاح وتحديث النظام التنبئي!")
                st.rerun()

elif sidebar_choice == "لوحة تحكم المستفيدين":
    st.header("🏡 قاعدة بيانات وإحصاءات المستفيدين")
    col1, col2, col3 = st.columns(3)
    col1.metric("عدد الأسر المستفيدة", f"{len(df_beneficiaries)} أسرة")
    col2.metric("متوسط دخل الأسرة", f"{int(df_beneficiaries['الدخل_الشهري_SAR'].mean()):,} SAR")
    col3.metric("متوسط عدد الأفراد", f"{int(df_beneficiaries['عدد_أفراد_الأسرة'].mean())} أفراد")
    
    st.download_button("📥 تحميل قاعدة البيانات المستفيدين", data=convert_df_to_csv(df_beneficiaries), file_name='beneficiaries_database.csv', mime='text/csv')
    
    fig, ax = plt.subplots(figsize=(8, 4))
    df_fixed_b = df_beneficiaries.copy()
    df_fixed_b['نوع_الدعم_المطلوب'] = df_fixed_b['نوع_الدعم_المطلوب'].apply(fix_arabic)
    df_fixed_b['حالة_الطلب'] = df_fixed_b['حالة_الطلب'].apply(fix_arabic)
    sns.countplot(data=df_fixed_b, x='نوع_الدعم_المطلوب', hue='حالة_الطلب', ax=ax)
    ax.set_title(fix_arabic('توزيع نوع الدعم المطلوب'))
    st.pyplot(fig)
    st.dataframe(df_beneficiaries, use_container_width=True)

elif sidebar_choice == "إدخل بيانات مستفيدين ➕":
    st.header("📝 تسجيل حالات المستفيدين")
    tab_manual, tab_excel = st.tabs(["✍️ إدخال يدوي لحالة واحدة", "📁 رفع جماعي Excel"])
    
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
        uploaded_file_b = st.file_uploader("اختر ملف Excel الخاص بالمستفيدين:", type=['csv', 'xlsx'])
        if uploaded_file_b is not None:
            if uploaded_file_b.name.endswith('.csv'):
                uploaded_df_b = pd.read_csv(uploaded_file_b)
            else:
                uploaded_df_b = pd.read_excel(uploaded_file_b)
            
            st.write("👀 عينة من الحالات المكتشفة:")
            st.dataframe(uploaded_df_b.head(5))
            
            if st.button("🚀 دمج وتحديث ملفات المستفيدين فوراً"):
                start_id_b = len(df_beneficiaries) + 1
                uploaded_df_b['المعرف'] = [f'B-{i}' for i in range(start_id_b, start_id_b + len(uploaded_df_b))]
                if 'مستوى_الاحتياج_المتوقع_مستقبلا' not in uploaded_df_b.columns:
                    uploaded_df_b['مستوى_الاحتياج_المتوقع_مستقبلا'] = np.random.choice(['متوسط', 'مرتفع جداً'], size=len(uploaded_df_b))
                st.session_state.df_beneficiaries = pd.concat([df_beneficiaries, uploaded_df_b], ignore_index=True)
                st.success("🎉 تم رفع ودمج السجلات بنجاح!")
                st.rerun()

elif sidebar_choice == "التحليلات التنبؤية (AI)":
    st.header("🔮 قسم التحليلات التنبؤية الذكي")
    
    if len(df_donors) >= 5:
        tab1, tab2 = st.tabs(["📉 التنبؤ بحجم التبرعات", "🎯 تقسيم المتبرعين الذكي"])
        
        with tab1:
            st.subheader("🤖 نموذج الانحدار الخطي للتنبؤ")
            X_model = df_donors[['العمر', 'عدد_مرات_التبرع']].values
            y_model = df_donors['مجموع_التبرعات_السنوية_SAR'].values
            
            lr = LinearRegression().fit(X_model, y_model)
            user_age = st.slider("اختر عمر المتبرع المستهدف:", 18, 80, 35)
            user_freq = st.slider("اختر عدد مرات التبرع سنوياً:", 1, 24, 5)
            
            input_data = np.array([[user_age, user_freq]], dtype=np.float64)
            prediction = lr.predict(input_data)
            val_final = int(max(0, prediction[0]))
            msg = f"SAR {val_final}"
            st.success(msg)

            st.write("📌 المنهج المستخدم: الانحدار الخطي المتعدد.")
            
        with tab2:
            st.subheader("🎯 تصنيف مجموعات المتبرعين المضمون")
            df_cluster = df_donors[['عدد_مرات_التبرع', 'مجموع_التبرعات_السنوية_SAR']].dropna().copy()
            
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10, max_iter=300)
            df_cluster['الفئة'] = kmeans.fit_predict(df_cluster.values)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = {0: '#1f77b4', 1: '#ff7f0e', 2: '#2ca02c'}
            for cluster_id, col in colors.items():
                sub_set = df_cluster[df_cluster['الفئة'] == cluster_id]
                ax.scatter(sub_set['عدد_مرات_التبرع'], sub_set['مجموع_التبرعات_السنوية_SAR'], c=col, label=fix_arabic(f'المجموعة {cluster_id + 1}'), alpha=0.7)
                
            ax.set_xlabel(fix_arabic('عدد مرات التبرع سنويًا'))
            ax.set_ylabel(fix_arabic('مجموع التبرعات السنوية (SAR)'))
            ax.set_title(fix_arabic('توزيع وتصنيف المتبرعين تلقائيًا'))
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig)

elif sidebar_choice == "🧠 تعلم مفاهيم الإحصاء في هذا التطبيق":
    st.header("🧠 معمل الإحصاء التعليمي")
    col_a, col_b = st.columns(2)
    with col_a:
        std_donations = df_donors['مجموع_التبرعات_السنوية_SAR'].std()
        st.metric(fix_arabic("الانحراف المعياري للتبرعات"), f"{int(std_donations):,} SAR")
    with col_b:
        mean_inc = df_beneficiaries['الدخل_الشهري_SAR'].mean()
        median_inc = df_beneficiaries['الدخل_الشهري_SAR'].median()
        st.write(f"📊 {fix_arabic('المتوسط الحسابي')}: {int(mean_inc):,} SAR")
        st.write(f"📊 {fix_arabic('الوسيط الإحصائي')}: {int(median_inc):,} SAR")

# --- البوت المساعد الذكي والتحليلي فائق الدقة لدعم المدن المتعددة والتنبؤ ---
elif sidebar_choice == "البوت المساعد الذكي":
    st.header("🤖 مساعد الخير الذكي والتحليلي")
    st.write("اسألني أي سؤال تحليلي (مثال: كم مجموع تبرعات جدة ومكة؟ ما هو تنبؤ تبرعات مكة؟)")
    
    q = st.text_input("🔍 اكتب سؤالك الذكي هنا:")
    if q:
        q_clean = q.strip()
        
        # دالة ذكية لتحديد كافة المدن المذكورة في السؤال
        detected_cities = []
        for city in ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة']:
            if city in q_clean:
                detected_cities.append(city)
                
        # دالة ذكية لتحديد نوع الدعم المذكور في السؤال
        detected_support = None
        support_map = {'سكن': 'سكني', 'غذاء': 'غذائي', 'صحي': 'صحي', 'تعليم': 'تعليمي'}
        for key, val in support_map.items():
            if key in q_clean:
                detected_support = val
                break

        # --- البوت المساعد الذكي والتحليلي فائق الدقة مع ميزة التصفير التلقائي ---
elif sidebar_choice == "البوت المساعد الذكي":
    st.header("🤖 مساعد الخير الذكي والتحليلي")
    st.write("اسألني أي سؤال تحليلي (مثال: كم مجموع تبرعات جدة ومكة؟ ما هو تنبؤ تبرعات مكة؟)")
    
    # بناء استمارة ذكية تقوم بتصفير ومسح خانة الكتابة تلقائياً فور إرسال السؤال
    with st.form("ai_bot_form", clear_on_submit=True):
        q = st.text_input("🔍 اكتب سؤالك الذكي هنا واضغط على زر الإرسال بالأسفل:")
        submit_question = st.form_submit_button("إرسال السؤال إلى البوت 🚀")
    
    if submit_question and q:
        q_clean = q.strip()
        
        # دالة ذكية لتحديد كافة المدن المذكورة في السؤال
        detected_cities = []
        for city in ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة']:
            if city in q_clean:
                detected_cities.append(city)
                
        # دالة ذكية لتحديد نوع الدعم المذكور في السؤال
        detected_support = None
        support_map = {'سكن': 'سكني', 'غذاء': 'غذائي', 'صحي': 'صحي', 'تعليم': 'تعليمي'}
        for key, val in support_map.items():
            if key in q_clean:
                detected_support = val
                break

        # عرض السؤال الحالي الذي تمت معالجته للتأكيد قبل تصفير الخانة
        st.markdown(f"**💬 سؤالك الحالي:** *{q_clean}*")

        # 1. معالجة أسئلة المتبرعين والتبرعات والذكاء الاصطناعي التنبؤي
        if "متبرع" in q_clean or "تبرع" in q_clean or "مبلغ" in q_clean or "مجموع" in q_clean or "إجمالي" in q_clean or "تنبؤ" in q_clean:
            # حالة طلب التنبؤ عبر الذكاء الاصطناعي
            if "تنبؤ" in q_clean or "متوقع" in q_clean:
                X_model = df_donors[['العمر', 'عدد_مرات_التبرع']].values
                y_model = df_donors['مجموع_التبرعات_السنوية_SAR'].values
                lr = LinearRegression().fit(X_model, y_model)
                
                if detected_cities:
                    sub_df = df_donors[df_donors['المدينة'].isin(detected_cities)]
                    avg_age = sub_df['العمر'].mean() if not sub_df.empty else 35
                    avg_freq = sub_df['عدد_مرات_التبرع'].mean() if not sub_df.empty else 5
                else:
                    avg_age = df_donors['العمر'].mean()
                    avg_freq = df_donors['عدد_مرات_التبرع'].mean()
                    
                pred = lr.predict(np.array([[avg_age, avg_freq]], dtype=np.float64))
                cities_names = " و ".join(detected_cities) if detected_cities else "العام"
                st.success(f"🔮 التنبؤ المالي الذكي لمتوسط التبرعات القادمة مستقبلاً من ({cities_names}) هو: {int(max(0, pred)):,} SAR")
            
            # حالة طلب المجاميع والأعداد الحالية الحية
            elif detected_cities:
                sub_df = df_donors[df_donors['المدينة'].isin(detected_cities)]
                cities_names = " و ".join(detected_cities)
                
                if "مجموع" in q_clean or "إجمالي" in q_clean or "مبالغ" in q_clean or "تبرعات" in q_clean and "كم" not in q_clean:
                    total_val = sub_df['مجموع_التبرعات_السنوية_SAR'].sum()
                    st.success(f"💰 إجمالي مبالغ التبرعات الحالية من ({cities_names}) هو: {total_val:,} SAR")
                elif "عدد" in q_clean or "كم" in q_clean:
                    st.success(f"📍 عدد المتبرعين الحالي من ({cities_names}) هو: {len(sub_df)} متبرع.")
                else:
                    total_val = sub_df['مجموع_التبرعات_السنوية_SAR'].sum()
                    st.success(f"💰 إجمالي مبالغ التبرعات الحالية من ({cities_names}) هو: {total_val:,} SAR")
            else:
                if "عدد" in q_clean or "كم" in q_clean:
                    st.success(f"📊 إجمالي عدد المتبرعين المسجلين هو: {len(df_donors)} متبرع.")
                else:
                    total_val = df_donors['مجموع_التبرعات_السنوية_SAR'].sum()
                    st.success(f"💰 إجمالي التبرعات العام الحالي في الصندوق: {total_val:,} SAR")

        # 2. معالجة أسئلة المستفيدين والحالات
        elif "مستفيد" in q_clean or "حالة" in q_clean or "أسرة" in q_clean or "عائلة" in q_clean:
            if detected_support:
                sub_df = df_beneficiaries[df_beneficiaries['نوع_الدعم_المطلوب'] == detected_support]
                st.success(f"📊 عدد الأسر التي تطلب دعماً ({detected_support}) هو: {len(sub_df)} أسرة.")
            else:
                st.success(f"🏡 إجمالي عدد الأسر المستفيدة المسجلة هو: {len(df_beneficiaries)} أسرة.")

        # 3. البحث الكلاسيكي البديل عن الأسماء الصريحة
        else:
            res_d = df_donors[df_donors['الاسم'].str.contains(q_clean, na=False)]
            res_b = df_beneficiaries[df_beneficiaries['العائلة'].str.contains(q_clean, na=False)]
            
            if not res_d.empty:
                st.write("📌 نتائج البحث في المتبرعين:")
                st.dataframe(res_d, use_container_width=True)
            elif not res_b.empty:
                st.write("📌 نتائج البحث في المستفيدين:")
                st.dataframe(res_b, use_container_width=True)
            else:
                st.warning("⚠️ لم أفهم الاستفسار بدقة، جرب كتابة: 'ما هو تنبؤ تبرعات مكة' أو 'إجمالي تبرعات مكة وجدة'.")





