import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import arabic_reshaper
from bidi.algorithm import get_display

def fix_arabic(t):
    res = arabic_reshaper.reshape(str(t))
    return get_display(res)

st.set_page_config(
    page_title="App", 
    layout="wide"
)

if 'df_donors' not in st.session_state:
    np.random.seed(42)
    n = 1000
    st.session_state.df_donors = pd.DataFrame({
        'ID': [f'D-{i}' for i in range(1, n + 1)],
        'Name': [f'Donor {i}' for i in range(1, n + 1)],
        'Age': np.random.randint(22, 70, size=n),
        'City': np.random.choice(['Riyadh', 'Jeddah', 'Dammam', 'Makkah', 'Madinah'], size=n),
        'Amount': np.random.randint(1000, 15000, size=n),
        'Freq': np.random.randint(1, 12, size=n),
        'Prob': np.random.randint(40, 99, size=n)
    })
if 'df_beneficiaries' not in st.session_state:
    np.random.seed(42)
    n = 1000
    st.session_state.df_beneficiaries = pd.DataFrame({
        'ID': [f'B-{i}' for i in range(1, n + 1)],
        'Family': [f'Family {i}' for i in range(1, n + 1)],
        'Members': np.random.randint(2, 9, size=n),
        'Income': np.random.randint(1500, 6500, size=n),
        'Type': np.random.choice(['Home', 'Food', 'Health', 'Edu'], size=n),
        'Status': np.random.choice(['Ok', 'Wait', 'Done'], size=n),
        'Need': np.random.choice(['High', 'Med', 'Stable'], size=n)
    })

df_donors = st.session_state.df_donors
df_beneficiaries = st.session_state.df_beneficiaries

# قاموس المترجم الذكي لمنع تداخل النصوص العربية
m_map = {
    'Riyadh': 'الرياض', 'Jeddah': 'جدة', 'Dammam': 'الدمام', 
    'Makkah': 'مكة', 'Madinah': 'المدينة', 'Home': 'سكني', 
    'Food': 'غذائي', 'Health': 'صحي', 'Edu': 'تعليمي',
    'Ok': 'مقبول', 'Wait': 'قيد الدراسة', 'Done': 'مكتمل'
}

df_d_ar = df_donors.replace(m_map)
df_b_ar = df_beneficiaries.replace(m_map)

with st.sidebar:
    st.title("⚙️")
    choice = st.radio(
        "📍 Options:", 
        ["Donors", "Beneficiaries", "CRUD", "AI", "Stats", "Bot"]
    )
if choice == "Donors":
    st.header("👥 قاعدة بيانات وإحصاءات المتبرعين")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي المتبرعين", f"{len(df_donors)}")
    c2.metric("إجمالي التبرعات", f"{df_donors['Amount'].sum():,}")
    c3.metric("متوسط التبرع", f"{int(df_donors['Amount'].mean()):,}")
    
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df_d_ar['City'].value_counts()
    lbls = [fix_arabic(x) for x in counts.index]
    ax.pie(counts, labels=lbls, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig)
    st.dataframe(df_d_ar, use_container_width=True)

elif choice == "Beneficiaries":
    st.header("🏡 قاعدة بيانات وإحصاءات المستفيدين")
    st.dataframe(df_b_ar, use_container_width=True)
elif choice == "CRUD":
    st.header("🛠️ مركز التحكم وإدارة البيانات السحابية")
    tab1, tab2 = st.tabs(["👥 المتبرعين", "🏡 المستفيدين"])
    with tab1:
        opt = st.selectbox("Action:", ["View/Delete", "Add ➕"])
        if opt == "Add ➕":
            with st.form("f1", clear_on_submit=True):
                v1 = st.text_input("الاسم:")
                v2 = st.number_input("العمر:", 18, 100, 35)
                v3 = st.selectbox("المدينة:", ['Riyadh', 'Jeddah', 'Dammam', 'Makkah', 'Madinah'])
                v4 = st.number_input("التبرع:", 0, 50000, 1000)
                v5 = st.number_input("التكرار:", 1, 50, 2)
                if st.form_submit_button("Save"):
                    row = {'ID': f'D-{len(df_donors)+1}', 'Name': v1, 'Age': int(v2), 'City': v3, 'Amount': int(v4), 'Freq': int(v5), 'Prob': 80}
                    st.session_state.df_donors = pd.concat([df_donors, pd.DataFrame([row])], ignore_index=True)
                    st.rerun()
        else:
            del_id = st.text_input("اكتب معرف المتبرع لحذفه (D-1):")
            if st.button("حذف المتبرع نهائياً"):
                st.session_state.df_donors = df_donors[df_donors['ID'] != del_id].reset_index(drop=True)
                st.rerun()
                
    with tab2:
        opt2 = st.selectbox("Action:", ["View/Delete", "Add ➕"], key="b_act")
        if opt2 == "Add ➕":
            with st.form("f2", clear_on_submit=True):
                b1 = st.text_input("العائلة:")
                b2 = st.slider("الأفراد:", 1, 15, 5)
                b3 = st.number_input("الدخل:", 0, 50000, 2000)
                b4 = st.selectbox("الدعم:", ['Home', 'Food', 'Health', 'Edu'])
                if st.form_submit_button("Save"):
                    row2 = {'ID': f'B-{len(df_beneficiaries)+1}', 'Family': b1, 'Members': int(b2), 'Income': int(b3), 'Type': b4, 'Status': 'Wait', 'Need': 'Med'}
                    st.session_state.df_beneficiaries = pd.concat([df_beneficiaries, pd.DataFrame([row2])], ignore_index=True)
                    st.rerun()
        else:
            del_b = st.text_input("اكتب معرف العائلة لحذفها (B-1):")
            if st.button("حذف العائلة نهائياً"):
                st.session_state.df_beneficiaries = df_beneficiaries[df_beneficiaries['ID'] != del_b].reset_index(drop=True)
                st.rerun()
elif choice == "AI":
    st.header("🔮 قسم التحليلات التنبؤية الذكي")
    t1, t2 = st.tabs(["📉 Linear Regression", "🎯 K-Means"])
    with t1:
        X = df_donors[['Age', 'Freq']].values
        y = df_donors['Amount'].values
        lr = LinearRegression().fit(X, y)
        s1 = st.slider("Age:", 18, 80, 35)
        s2 = st.slider("Freq:", 1, 24, 5)
        pred = lr.predict(np.array([[s1, s2]], dtype=np.float64))
        st.success(f"💰 SAR {int(max(0, pred))}")
    with t2:
        X_c = df_donors[['Freq', 'Amount']].dropna().copy()
        km = KMeans(n_clusters=3, random_state=42, n_init=10)
        X_c['Cluster'] = km.fit_predict(X_c.values)
        fig, ax = plt.subplots(figsize=(8, 5))
        for cid in [0, 1, 2]:
            sub = X_c[X_c['Cluster'] == cid]
            ax.scatter(sub['Freq'], sub['Amount'], alpha=0.7, label=f'G-{cid+1}')
        st.pyplot(fig)

elif choice == "Stats":
    st.header("🧠 معمل الإحصاء التعليمي")
    st.metric(fix_arabic("الانحراف المعياري"), f"{int(df_donors['Amount'].std()):,}")

elif choice == "Bot":
    st.header("🤖 مساعد الخير الذكي والتحليلي")
    q = st.text_input("🔍 اكتب سؤالك هنا واضغط Enter:")
    if q:
        q_c = q.strip()
        st.markdown(f"💬 *{q_c}*")
        if "مستفيد" in q_c and "سكن" in q_c:
            sub = df_beneficiaries[df_beneficiaries['Type'] == 'Home']
            st.success(f"🏡 {len(sub)}")
        elif "مستفيد" in q_c:
            st.success(f"🏡 {len(df_beneficiaries)}")
        elif "متبرع" in q_c and "مكة" in q_c:
            sub = df_donors[df_donors['City'] == 'Makkah']
            st.success(f"📍 {len(sub)}")
        elif "متبرع" in q_c:
            st.success(f"📊 {len(df_donors)}")
        elif "مكة" in q_c:
            val = df_donors[df_donors['City'] == 'Makkah']['Amount'].sum()
            st.success(f"💰 {val:,} SAR")
        else:
            st.warning("⚠️")
