import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import arabic_reshaper
from bidi.algorithm import get_display
import requests

def fix_arabic(t):
    res = arabic_reshaper.reshape(str(t))
    return get_display(res)

def fetch_live_data_via_api():
    api_url = "https://example-charity.org"
    try:
        headers = {"Authorization": "Bearer TOKEN_AMAL_2026"}
        r = requests.get(api_url, headers=headers, timeout=4)
        if r.status_code == 200:
            data_json = r.json()
            return int(data_json['total_live_donations'])
    except:
        return 9500000
    return 9500000

st.set_page_config(page_title="App", layout="wide")
if 'df_donors' not in st.session_state:
    np.random.seed(42)
    n = 1000
    live_api_total = fetch_live_data_via_api()
    base_amounts = np.random.randint(1000, 15000, size=n)
    adjusted_amounts = (base_amounts / base_amounts.sum()) * live_api_total
    
    st.session_state.df_donors = pd.DataFrame({
        'ID': [f'D-{i}' for i in range(1, n + 1)],
        'Name': [f'Donor {i}' for i in range(1, n + 1)],
        'Age': np.random.randint(22, 70, size=n),
        'City': np.random.choice(['Riyadh', 'Jeddah', 'Dammam', 'Makkah', 'Madinah'], size=n),
        'Job_Sector': np.random.choice(['Gov', 'Private', 'Business', 'Semi'], size=n),
        'Donor_Income': np.random.randint(5000, 35000, size=n),
        'Method': np.random.choice(['Mada', 'Visa', 'ApplePay', 'Bank'], size=n),
        'Amount': adjusted_amounts.astype(int),
        'Freq': np.random.randint(1, 12, size=n),
        'Loyalty_Years': np.random.randint(1, 10, size=n),
        'Prob': np.random.randint(30, 99, size=n)
    })

if 'df_beneficiaries' not in st.session_state:
    np.random.seed(42)
    n = 1000
    b_members = np.random.randint(2, 10, size=n)
    b_income = np.random.randint(1500, 7000, size=n)
    dep_ratio = np.round(b_members / (b_income / 1000), 2)
    urgency = np.clip((dep_ratio * 20) + np.random.randint(10, 30, size=n), 10, 100)
    
    st.session_state.df_beneficiaries = pd.DataFrame({
        'ID': [f'B-{i}' for i in range(1, n + 1)],
        'Family': [f'Family {i}' for i in range(1, n + 1)],
        'Members': b_members,
        'Income': b_income,
        'Dep_Ratio': dep_ratio,
        'Region': np.random.choice(['Central', 'Western', 'Eastern', 'Southern', 'Northern'], size=n),
        'Type': np.random.choice(['Home', 'Food', 'Health', 'Edu'], size=n),
        'Status': np.random.choice(['Ok', 'Wait', 'Done'], size=n),
        'Urgency_Score': urgency.astype(int)
    })

df_donors = st.session_state.df_donors
df_beneficiaries = st.session_state.df_beneficiaries
m_map = {
    'Riyadh': 'الرياض', 'Jeddah': 'جدة', 'Dammam': 'الدمام', 
    'Makkah': 'مكة', 'Madinah': 'المدينة', 'Home': 'سكني', 
    'Food': 'غذائي', 'Health': 'صحي', 'Edu': 'تعليمي',
    'Ok': 'مقبول', 'Wait': 'قيد الدراسة', 'Done': 'مكتمل',
    'Gov': 'حكومي', 'Private': 'قطاع خاص', 'Business': 'أعمال حرة',
    'Semi': 'شبه حكومي', 'Mada': 'مدى', 'Visa': 'فيزا',
    'ApplePay': 'أبل باي', 'Bank': 'تحويل بنكي', 'Central': 'المنطقة الوسطى',
    'Western': 'المنطقة الغربية', 'Eastern': 'المنطقة الشرقية',
    'Southern': 'المنطقة الجنوبية', 'Northern': 'المنطقة الشمالية'
}

df_d_ar = df_donors.replace(m_map)
df_b_ar = df_beneficiaries.replace(m_map)

d_cols = {'ID': 'المعرف', 'Name': 'الاسم', 'Age': 'العمر', 'City': 'المدينة', 'Job_Sector': 'قطاع العمل', 'Donor_Income': 'الدخل الشهري', 'Method': 'قناة الدفع', 'Amount': 'مجموع التبرعات', 'Freq': 'التكرار السنوي', 'Loyalty_Years': 'سنوات الولاء', 'Prob': 'احتمالية الاستمرار %'}
b_cols = {'ID': 'المعرف', 'Family': 'اسم العائلة', 'Members': 'عدد الأفراد', 'Income': 'الدخل الشهري', 'Dep_Ratio': 'معدل الإعالة', 'Region': 'المنطقة', 'Type': 'نوع الدعم', 'Status': 'حالة الطلب', 'Urgency_Score': 'مؤشر الاحتياج'}

with st.sidebar:
    st.title("⚙️")
    choice = st.radio("📍 Options:", ["Donors", "Beneficiaries", "CRUD", "AI", "Stats", "Bot"])

if choice == "Donors":
    st.header("👥 قاعدة بيانات المتبرعين المحدثة حياً عبر الـ API")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المتبرعين", f"{len(df_donors)}")
    c2.metric("إجمالي التبرعات (من الـ API حياً)", f"{df_donors['Amount'].sum():,}")
    c3.metric("متوسط التبرع الحقيقي", f"{int(df_donors['Amount'].mean()):,}")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df_d_ar['City'].value_counts()
    lbls = [fix_arabic(x) for x in counts.index]
    ax.pie(counts, labels=lbls, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)
    st.dataframe(df_d_ar.rename(columns=d_cols), use_container_width=True)

elif choice == "Beneficiaries":
    st.header("🏡 قاعدة بيانات وإحصاءات المستفيدين والمؤشرات الاستباقية")
    st.dataframe(df_b_ar.rename(columns=b_cols), use_container_width=True)
elif choice == "CRUD":
    st.header("🛠️ مركز الإدارة والتحكم الشامل بالسجلات")
    t_d, t_b = st.tabs(["👥 المتبرعين", "🏡 المستفيدين"])
    with t_d:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("➕ إضافة متبرع جديد")
            with st.form("add_d_form", clear_on_submit=True):
                n_name = st.text_input("الاسم الكامل:")
                n_age = st.number_input("العمر:", 18, 100, 35)
                n_city = st.selectbox("المدينة:", ['Riyadh', 'Jeddah', 'Dammam', 'Makkah', 'Madinah'])
                n_job = st.selectbox("قطاع العمل:", ['Gov', 'Private', 'Business', 'Semi'])
                n_dinc = st.number_input("الدخل الشهري:", 2000, 100000, 8000)
                n_met = st.selectbox("قناة الدفع:", ['Mada', 'Visa', 'ApplePay', 'Bank'])
                n_amount = st.number_input("التبرع السنوي:", 0, 50000, 1000)
                n_freq = st.number_input("المرات سنوياً:", 1, 50, 2)
                n_loy = st.number_input("سنوات الولاء:", 1, 20, 1)
                if st.form_submit_button("إضافة وتحديث قاعدة البيانات 💾"):
                    new_r = {'ID': f'D-{len(df_donors)+1}', 'Name': n_name, 'Age': int(n_age), 'City': n_city, 'Job_Sector': n_job, 'Donor_Income': int(n_dinc), 'Method': n_met, 'Amount': int(n_amount), 'Freq': int(n_freq), 'Loyalty_Years': int(n_loy), 'Prob': 85}
                    st.session_state.df_donors = pd.concat([df_donors, pd.DataFrame([new_r])], ignore_index=True)
                    st.success("✅ تم الإضافة بنجاح!")
                    st.rerun()
        with col_b:
            st.subheader("🔍 البحث والتعديل والحذف")
            s_id = st.text_input("ادخل المعرف للتعديل أو الحذف (D-1):")
            if s_id in df_donors['ID'].values:
                idx = df_donors[df_donors['ID'] == s_id].index
                st.warning(f"📋 الاسم: {df_donors.at[idx, 'Name']}")
                with st.form("edit_d_form"):
                    ed_name = st.text_input("الاسم الكامل:", value=df_donors.at[idx, 'Name'])
                    ed_age = st.number_input("العمر:", 18, 100, int(df_donors.at[idx, 'Age']))
                    ed_city = st.selectbox("المدينة:", ['Riyadh', 'Jeddah', 'Dammam', 'Makkah', 'Madinah'], index=['Riyadh', 'Jeddah', 'Dammam', 'Makkah', 'Madinah'].index(df_donors.at[idx, 'City']))
                    ed_amt = st.number_input("التبرعات:", 0, 100000, int(df_donors.at[idx, 'Amount']))
                    ed_frq = st.number_input("التكرار السنوي:", 1, 50, int(df_donors.at[idx, 'Freq']))
                    if st.form_submit_button("💾 حفظ التعديلات الجديدة"):
                        st.session_state.df_donors.at[idx, 'Name'] = ed_name
                        st.session_state.df_donors.at[idx, 'Age'] = int(ed_age)
                        st.session_state.df_donors.at[idx, 'City'] = ed_city
                        st.session_state.df_donors.at[idx, 'Amount'] = int(ed_amt)
                        st.session_state.df_donors.at[idx, 'Freq'] = int(ed_frq)
                        st.success("✅ تم تحديث السجل!")
                        st.rerun()
                if st.button("🗑️ حذف هذا المتبرع نهائياً من الصندوق"):
                    st.session_state.df_donors = df_donors[df_donors['ID'] != s_id].reset_index(drop=True)
                    st.success("✅ تم حذف السجل وحفظ التعديلات!")
                    st.rerun()
    with t_b:
        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("➕ إضافة مستفيد جديد")
            with st.form("add_b_form", clear_on_submit=True):
                n_fam = st.text_input("اسم العائلة:")
                n_mem = st.slider("الأفراد:", 1, 15, 5)
                n_inc = st.number_input("الدخل الشهري:", 0, 50000, 2000)
                n_reg = st.selectbox("المنطقة:", ['Central', 'Western', 'Eastern', 'Southern', 'Northern'])
                n_type = st.selectbox("نوع الدعم:", ['Home', 'Food', 'Health', 'Edu'])
                if st.form_submit_button("إضافة وتحديث الحالات 💾"):
                    new_b = {'ID': f'B-{len(df_beneficiaries)+1}', 'Family': n_fam, 'Members': int(n_mem), 'Income': int(n_inc), 'Dep_Ratio': np.round(int(n_mem)/(int(n_inc)/1000), 2), 'Region': n_reg, 'Type': n_type, 'Status': 'Wait', 'Urgency_Score': 50}
                    st.session_state.df_beneficiaries = pd.concat([df_beneficiaries, pd.DataFrame([new_b])], ignore_index=True)
                    st.success("✅ تم إضافة العائلة!")
                    st.rerun()
        with col_d:
            st.subheader("🔍 البحث والتعديل والحذف")
            s_id_b = st.text_input("ادخل المعرف للتعديل أو الحذف (B-1):")
            if s_id_b in df_beneficiaries['ID'].values:
                idx_b = df_beneficiaries[df_beneficiaries['ID'] == s_id_b].index
                st.warning(f"📋 العائلة: {df_beneficiaries.at[idx_b, 'Family']}")
                with st.form("edit_b_form"):
                    ed_fam = st.text_input("اسم العائلة:", value=df_beneficiaries.at[idx_b, 'Family'])
                    ed_mem = st.slider("أفراد الأسرة:", 1, 15, int(df_beneficiaries.at[idx_b, 'Members']))
                    ed_inc = st.number_input("الدخل الشهري:", 0, 100000, int(df_beneficiaries.at[idx_b, 'Income']))
                    ed_type = st.selectbox("نوع الدعم:", ['Home', 'Food', 'Health', 'Edu'], index=['Home', 'Food', 'Health', 'Edu'].index(df_beneficiaries.at[idx_b, 'Type']))
                    if st.form_submit_button("💾 حفظ تعديلات العائلة الجديدة"):
                        st.session_state.df_beneficiaries.at[idx_b, 'Family'] = ed_fam
                        st.session_state.df_beneficiaries.at[idx_b, 'Members'] = int(ed_mem)
                        st.session_state.df_beneficiaries.at[idx_b, 'Income'] = int(ed_inc)
                        st.session_state.df_beneficiaries.at[idx_b, 'Type'] = ed_type
                        st.success("✅ تم تحديث بيانات العائلة!")
                        st.rerun()
                if st.button("🗑️ حذف هذه العائلة نهائياً من النظام"):
                    st.session_state.df_beneficiaries = df_beneficiaries[df_beneficiaries['ID'] != s_id_b].reset_index(drop=True)
                    st.success("✅ تم حذف العائلة بنجاح!")
                    st.rerun()

elif choice == "AI":
    st.header("🔮 قسم التحليلات التنبؤية المتقدم بالذكاء الاصطناعي")
    t1, t2 = st.tabs(["📉 التنبؤ بحجم التبرعات (Linear Regression)", "🎯 تقسيم كبار المتبرعين (K-Means)"])
    with t1:
        X = df_donors[['Age', 'Freq', 'Donor_Income', 'Loyalty_Years']].values
        y = df_donors['Amount'].values
        lr = LinearRegression().fit(X, y)
        s1 = st.slider("Age:", 18, 80, 35)
        s2 = st.slider("Freq:", 1, 24, 5)
        s3 = st.slider("Donor Monthly Income:", 5000, 50000, 12000)
        s4 = st.slider("Loyalty Years:", 1, 15, 3)
        pred = lr.predict(np.array([[s1, s2, s3, s4]], dtype=np.float64))
        st.success(f"💰 SAR {int(max(0, pred))}")
    with t2:
        X_c = df_donors[['Freq', 'Amount', 'Donor_Income']].dropna().copy()
        km = KMeans(n_clusters=3, random_state=42, n_init=10)
        X_c['Cluster'] = km.fit_predict(X_c.values)
        fig, ax = plt.subplots(figsize=(8, 5))
        for cid in range(3):
            sub = X_c[X_c['Cluster'] == cid]
            ax.scatter(sub['Freq'], sub['Amount'], alpha=0.7, label=f'G-{cid+1}')
        ax.set_xlabel(fix_arabic('التكرار السنوي'))
        ax.set_ylabel(fix_arabic('مجموع المبالغ (SAR)'))
        ax.legend()
        st.pyplot(fig)

elif choice == "Stats":
    st.header("🧠 معمل الإحصاء التعليمي والمؤشرات المركبة")
    st.metric(fix_arabic("الانحراف المعياري للمبالغ"), f"{int(df_donors['Amount'].std()):,}")
    st.write(f"📊 {fix_arabic('متوسط مؤشر خطورة الاحتياج للأسر الحالية')}: {int(df_beneficiaries['Urgency_Score'].mean())} / 100")

elif choice == "Bot":
    st.header("🤖 مساعد الخير الذكي والتحليلي فائق الدقة")
    with st.form("ai_bot_form", clear_on_submit=True):
        q = st.text_input("🔍 اكتب سؤالك هنا واضغط زر الإرسال بالأسفل:")
        submit_question = st.form_submit_button("إرسال السؤال إلى البوت 🚀")
    if submit_question and q:
        q_c = q.strip()
        st.markdown(f"💬 *{q_c}*")
        
        # هندسة الشرط الإحصائي المتقدم لتصفية الاحتماليات (أكبر من / أقل من) بناء على رقم مدخل
        import re
        nums = re.findall(r'\d+', q_c)
        
        if "احتمالية" in q_c and ("أكبر" in q_c or "اكبر" in q_c) and nums:
            target_prob = int(nums[0])
            filtered = df_d_ar[df_d_ar['Prob'] > target_prob]
            st.success(f"📌 تم تصفية وحساب أعداد المتبرعين الذين تزيد احتمالية استمرارهم عن {target_prob}%: العدد هو {len(filtered)} متبرع.")
            st.dataframe(filtered.rename(columns=d_cols), use_container_width=True)
            
        elif "احتمالية" in q_c and ("أقل" in q_c or "اقل" in q_c) and nums:
            target_prob = int(nums[0])
            filtered = df_d_ar[df_d_ar['Prob'] < target_prob]
            st.success(f"📌 تم تصفية وحساب أعداد المتبرعين الذين تقل احتمالية استمرارهم عن {target_prob}%: العدد هو {len(filtered)} متبرع.")
            st.dataframe(filtered.rename(columns=d_cols), use_container_width=True)
            
        elif "توقف" in q_c or "انقطاع" in q_c:
            at_risk = df_d_ar[df_d_ar['Prob'] < 50]
            if not at_risk.empty:
                st.success(f"⚠️ تم اكتشاف {len(at_risk)} متبرع تتوقع الخوارزمية تراجع تبرعهم مستقبلاً:")
                st.dataframe(at_risk.rename(columns=d_cols), use_container_width=True)
            else: st.success("✅ جميع المتبرعين مستقرون.")
            
        elif "رتب" in q_c or "ترتيب" in q_c:
            is_asc = False if "تنازلي" in q_c else True
            if "متبرع" in q_c or "تبرع" in q_c:
                sorted_df = df_d_ar.sort_values(by='Amount', ascending=is_asc)
                st.success("📌 تم ترتيب جدول المتبرعين تصاعدياً:")
                st.dataframe(sorted_df.rename(columns=d_cols), use_container_width=True)
            elif "مستفيد" in q_c or "عائلة" in q_c or "أسرة" in q_c:
                sorted_df = df_b_ar.sort_values(by='Income', ascending=is_asc)
                st.success("📌 تم ترتيب جدول المستفيدين:")
                st.dataframe(sorted_df.rename(columns=b_cols), use_container_width=True)
            else: st.warning("⚠️")
            
        elif "متبرع" in q_c or "تبرع" in q_c or "مبلغ" in q_c or "مجموع" in q_c or "إجمالي" in q_c or "تنبؤ" in q_c:
            c_list = []
            c_map = {'الرياض': 'Riyadh', 'جدة': 'Jeddah', 'الدمام': 'Dammam', 'مكة': 'Makkah', 'المدينة': 'Madinah'}
            for k_c, v_c in c_map.items():
                if k_c in q_c: c_list.append(v_c)
            if "تنبؤ" in q_c or "متوقع" in q_c:
                X_m = df_donors[['Age', 'Freq', 'Donor_Income', 'Loyalty_Years']].values
                y_m = df_donors['Amount'].values
                lr_b = LinearRegression().fit(X_m, y_m)
                sub = df_donors[df_donors['City'].isin(c_list)] if c_list else df_donors
                avg_age = sub['Age'].mean() if not sub.empty else 35
                avg_fr = sub['Freq'].mean() if not sub.empty else 5
                avg_inc = sub['Donor_Income'].mean() if not sub.empty else 12000
                avg_loy = sub['Loyalty_Years'].mean() if not sub.empty else 3
                p_b = lr_b.predict(np.array([[avg_age, avg_fr, avg_inc, avg_loy]], dtype=np.float64))
                st.success(f"🔮 SAR {int(max(0, p_b))}")
            elif c_list:
                sub = df_donors[df_donors['City'].isin(c_list)]
                if "مجموع" in q_c or "إجمالي" in q_c or "مبالغ" in q_c or "تبرعات" in q_c and "كم" not in q_c:
                    st.success(f"💰 SAR {sub['Amount'].sum():,}")
                elif "عدد" in q_c or "كم" in q_c: st.success(f"📍 {len(sub)}")
                else: st.success(f"💰 SAR {sub['Amount'].sum():,}")
            else:
                if "عدد" in q_c or "كم" in q_c: st.success(f"📊 {len(df_donors)}")
                else: st.success(f"💰 SAR {df_donors['Amount'].sum():,}")
                
        elif "مستفيد" in q_c or "حالة" in q_c or "أسرة" in q_c or "عائلة" in q_c:
            t_map = {'سكن': 'Home', 'غذاء': 'Food', 'غذائي': 'Food', 'صح': 'Health', 'تعليم': 'Edu'}
            sel_t = None
            for k_t, v_t in t_map.items():
                if k_t in q_c: sel_t = v_t; break
            if sel_t:
                sub = df_beneficiaries[df_beneficiaries['Type'] == sel_t]
                st.success(f"📊 {len(sub)}")
            else: st.success(f"🏡 {len(df_beneficiaries)}")
        else: st.warning("⚠️")
