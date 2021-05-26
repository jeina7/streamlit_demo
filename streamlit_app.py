import streamlit as st
import pandas as pd


df = pd.read_csv("sample.csv").drop("Unnamed: 0", axis=1)
df["ba_mean"] = df["ba_mean"].astype(int)
df["last_daily_budget"] = df["last_daily_budget"].astype(int)
df["daily_spend"] = df["daily_spend"].astype(int)
df["running_t_count"] = df["running_t_count"].astype(int)
df = df[df["running_t_count"] > 12]
maxppc_display = max(df["max_ppc"].unique())
maxppc_bizboard = min(df["max_ppc"].unique())

dt = st.sidebar.date_input("날짜를 선택하세요")
df = df[df["p_dt"] == str(dt)]

maxppc_option = st.sidebar.radio(
    "MaxPPC",
    [
        "all",
        f"display ({int(maxppc_display)})",
        f"bizboard ({int(maxppc_bizboard)})",
    ],
)
maxppc_threshold = max(maxppc_display, maxppc_bizboard)
if maxppc_option == f"display ({int(maxppc_display)})":
    maxppc_threshold = maxppc_display
    df = df[df["max_ppc"] == maxppc_threshold]
elif maxppc_option == f"bizboard ({int(maxppc_bizboard)})":
    maxppc_threshold = maxppc_bizboard
    df = df[df["max_ppc"] == maxppc_threshold]

spend_rate_threshold = st.sidebar.select_slider(
    "하루 평균 소진율이 아래보다 작은 그룹을 보고싶어요.",
    options=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
)
df = df[df["daily_spend_rate"] <= spend_rate_threshold]

ba_threshold = st.sidebar.select_slider(
    "하루 평균 BA가 아래보다 작은 그룹을 보고싶어요.",
    options=range(0, int(maxppc_threshold) + 10, 10),
)
df = df[df["ba_mean"] < ba_threshold]

budget_threshold = st.sidebar.radio(
    "하루 평균 예산이 아래보다 큰 그룹을 보고싶어요.",
    ["all", "100만", "500만", "1000만", "5000만", "1억"],
)

if budget_threshold == "all":
    budget_threshold = 0
elif budget_threshold == "100만":
    budget_threshold = 1e6
elif budget_threshold == "500만":
    budget_threshold = 5e6
elif budget_threshold == "1000만":
    budget_threshold = 1e7
elif budget_threshold == "5000만":
    budget_threshold = 5e7
elif budget_threshold == "1억":
    budget_threshold = 1e8
df = df[df["last_daily_budget"] > budget_threshold]

st.write(
    f"""
# {dt}
"""
)
df = df.drop("p_dt", axis=1)
st.write(df.shape[0], "개의 그룹이 선택되었습니다.")
st.dataframe(df.reset_index(drop=True), height=500)
