import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Screen_time_2022.csv")
    df["Date"] = pd.to_datetime(df["Date"])  # Ensure Date is in datetime format
    return df

df = load_data()

# ---- UI DESIGN ----
st.title("📱 Real-Time Screen Time Tracker")
st.subheader("Analyze Your Screen Time & Get Smart Recommendations")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
selected_date = st.sidebar.date_input("Select Date", df["Date"].max())

# Filter data for selected date
filtered_data = df[df["Date"] == pd.to_datetime(selected_date)]

# ---- VISUALIZATIONS ----
st.markdown("### 📊 Screen Time Breakdown")

# Pie Chart: Usage Distribution by App
fig, ax = plt.subplots()
app_usage = filtered_data.groupby("App")["Usage"].sum()
ax.pie(app_usage, labels=app_usage.index, autopct='%1.1f%%', startangle=140)
ax.set_title("Screen Time Distribution by App")
st.pyplot(fig)

# Bar Chart: Top Apps by Usage
st.markdown("### ⏳ Top Apps by Usage")
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=filtered_data, x="Usage", y="App", palette="coolwarm", ax=ax)
ax.set_xlabel("Minutes Spent")
ax.set_ylabel("App Name")
st.pyplot(fig)

# ---- TEXT-BASED OUTPUT FOR MOST FREQUENTLY OPENED APPS ----
st.markdown("### 🔄 Most Frequently Opened Apps")
sorted_apps = filtered_data.sort_values(by="Times opened", ascending=False)
for index, row in sorted_apps.iterrows():
    st.write(f"📂 **{row['App']}** was opened **{row['Times opened']}** times.")

# Scatter Plot: Times Opened vs. Usage
st.markdown("### ⏳ Does Opening an App More Mean More Usage?")
fig, ax = plt.subplots(figsize=(6, 4))
sns.scatterplot(data=filtered_data, x="Times opened", y="Usage", hue="App", size="Usage", sizes=(20, 200), ax=ax)
ax.set_xlabel("Times opened")
ax.set_ylabel("Minutes Spent")
ax.set_title("Most Opened vs. Time Spent on App")
st.pyplot(fig)

# ---- RECOMMENDATIONS ----
st.markdown("### 💡 Smart Insights & Recommendations")

total_time = filtered_data["Usage"].sum()
total_notifications = filtered_data["Notifications"].sum()

if total_time > 300:
    st.warning(f"⚠️ High Screen Time Alert! You spent {total_time} minutes on your phone today.")
elif total_time > 180:
    st.info(f"🔄 Moderate Usage ({total_time} min). Consider taking short breaks!")
else:
    st.success(f"✅ Low Screen Time ({total_time} min). Keep up the balance!")

# Most frequently opened app
most_opened_app = filtered_data.loc[filtered_data["Times opened"].idxmax()]
st.warning(f"📂 You opened **{most_opened_app['App']}** {most_opened_app['Times opened']} times today! Is it necessary?")

st.markdown("### 📌 App-Specific Insights")
for _, row in filtered_data.iterrows():
    if row["Times opened"] > 50:
        st.warning(f"🔄 **{row['App']}** was opened {row['Times opened']} times today. Consider reducing interruptions!")
    if row["Usage"] > 60:
        st.warning(f"📱 You spent {row['Usage']} min on **{row['App']}**. Try taking breaks!")

st.markdown("##### 🚀 Stay mindful of your screen time and balance productivity with breaks!")  
