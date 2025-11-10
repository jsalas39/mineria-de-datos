import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="University Dashboard", layout="wide")

st.title("University Data Dashboard")

df = pd.read_csv('university_student_data.csv')
df.columns = df.columns.str.strip()

year = st.sidebar.selectbox("Select Year:", sorted(df['Year'].unique()))
term = st.sidebar.selectbox("Select Term:", sorted(df['Term'].unique()))
department = st.sidebar.selectbox(
    "Select Department:",
    ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
)

filtered_df = df[(df['Year'] == year) & (df['Term'] == term)]

st.subheader(f"Year: {year} | Term: {term} | Department: {department.split()[0]}")

col1, col2, col3 = st.columns(3)
col1.metric("Retention Rate", f"{filtered_df['Retention Rate (%)'].mean():.2f}%")
col2.metric("Satisfaction Score", f"{filtered_df['Student Satisfaction (%)'].mean():.2f}")
col3.metric("Total Enrolled", int(filtered_df[department].sum()))

st.write("### Retention Rate Trends Over Time")
retention = df.groupby('Year')['Retention Rate (%)'].mean().reset_index()
fig1, ax1 = plt.subplots(figsize=(8,5))
sns.lineplot(data=retention, x='Year', y='Retention Rate (%)', marker='o', ax=ax1)
ax1.set_title('Retention Rate Trends Over Time')
st.pyplot(fig1)

st.write("### Student Satisfaction by Year")
satisfaction = df.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(8,5))
sns.barplot(data=satisfaction, x='Year', y='Student Satisfaction (%)', palette='mako', ax=ax2)
ax2.set_title('Student Satisfaction by Year')
st.pyplot(fig2)

st.write("### Comparison: Spring vs Fall (Retention Rate)")
term_comparison = df.groupby('Term')['Retention Rate (%)'].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(6,4))
sns.barplot(data=term_comparison, x='Term', y='Retention Rate (%)', palette='Set2', ax=ax3)
ax3.set_title('Comparison: Spring vs Fall Terms')
st.pyplot(fig3)

st.write("### Department Enrollment Comparison")
departments = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
dept_totals = df[departments].sum().reset_index()
dept_totals.columns = ['Department', 'Total Enrolled']

fig4, ax4 = plt.subplots(figsize=(7,4))
sns.barplot(data=dept_totals, x='Department', y='Total Enrolled', palette='coolwarm', ax=ax4)
ax4.set_title('Total Enrollment by Department')
plt.xticks(rotation=20)
st.pyplot(fig4)

st.success("Dashboard loaded successfully!")
