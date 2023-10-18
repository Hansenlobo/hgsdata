import plost
import os
import requests
import pandas as pd
import streamlit as st
from datetime import date
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()

# Initial Setup
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

table_name="dts"

supabase_url = os.getenv("supabase_url")
supabase_key = os.getenv("supabase_key")



while True:
    current_time = datetime.now()
    formatted_time = current_time.strftime("%d-%m-%Y %H:%M")
    st.title(f"My HGS Sales Dashboard  ({formatted_time})")
    break

st.write("Sales Value (Credit):")
# Todays Transactions
current_datetime = datetime.now()
start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = current_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
start_time = start_of_day.isoformat()
end_time = end_of_day.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{start_time}&created_at=lte.{end_time}&Transaction Type=eq.Credited"
response = requests.get(url, headers={"apikey": supabase_key})

if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase.{response.text}")
    sum_b=0


# Today-1 Transactions
yesterday = current_datetime - timedelta(days=1)
start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{start_of_yesterday}&created_at=lte.{end_of_yesterday}&Transaction Type=eq.Credited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_yesterday = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_yesterday=0


# Current Month Transactions
current_datetime = datetime.now()
start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
next_month = current_datetime.replace(day=1, month=current_datetime.month + 1)
if next_month.month == 1:
    next_month = next_month.replace(year=current_datetime.year + 1)
start_time = start_of_month.isoformat()
end_time = next_month.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{start_time}&created_at=lt.{end_time}&Transaction Type=eq.Credited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_month = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")

# Last month
current_datetime = datetime.now()
start_of_current_month = current_datetime.replace(day=1)
start_of_last_month = (start_of_current_month - timedelta(days=1)).replace(day=1)
end_of_last_month = start_of_current_month - timedelta(days=1)
start_time = start_of_last_month.isoformat()
end_time = end_of_last_month.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{start_time}&created_at=lt.{end_time}&Transaction Type=eq.Credited"
response = requests.get(url, headers={"apikey": supabase_key})

if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_last_month = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_last_month=0

# current week
current_datetime = datetime.now()
current_week_start = current_datetime - timedelta(days=current_datetime.weekday(), hours=current_datetime.hour, minutes=current_datetime.minute, seconds=current_datetime.second)
current_week_end = current_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
current_week_start_iso = current_week_start.isoformat()
current_week_end_iso = current_week_end.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{current_week_start_iso}&created_at=lt.{current_week_end_iso}&Transaction Type=eq.Credited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_week = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_week=0

# Last week
current_datetime = datetime.now()
current_week_start = current_datetime - timedelta(days=current_datetime.weekday(), hours=current_datetime.hour, minutes=current_datetime.minute, seconds=current_datetime.second)
current_week_end = current_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
last_week_start = current_week_start - timedelta(days=7)
last_week_end = last_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
last_week_start_iso = last_week_start.isoformat()
last_week_end_iso = last_week_end.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{last_week_start_iso}&created_at=lt.{last_week_end_iso}&Transaction Type=eq.Credited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_last_week = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_last_week=0


# last Year
current_datetime = datetime.now()
last_year_start = datetime(current_datetime.year - 1, 1, 1)
last_year_end = datetime(current_datetime.year - 1, 12, 31, 23, 59, 59)
last_year_start_iso = last_year_start.isoformat()
last_year_end_iso = last_year_end.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{last_year_start_iso}&created_at=lt.{last_year_end_iso}&Transaction Type=eq.Credited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_last_year = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_last_year=0

# Current Year
current_datetime = datetime.now()
current_year_start = current_datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
next_year_start = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0, 0)
current_year_end = next_year_start - timedelta(seconds=1)
current_year_start_iso = current_year_start.isoformat()
current_year_end_iso = current_year_end.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{current_year_start_iso}&created_at=lt.{current_year_end_iso}&Transaction Type=eq.Credited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_year = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_year=0





col1, col2, col3, col4 = st.columns(4)
box_style = """
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    margin: 10px;
    text-align: center;
"""
# Define CSS styles for positive and negative values
positive_style = 'color: green; font-weight: bold;'
negative_style = 'color: red; font-weight: bold;'

def calculate_percentage_change(old_value, new_value):
    if old_value == 0:
        percentage_change = ((new_value - 1) / 1) * 100
        return ""  # Avoid division by zero
    percentage_change = ((new_value - old_value) / old_value) * 100
    return str(round(percentage_change))+"%"

with col1:
    st.markdown(f'<div style="{box_style}"><b style="font-size: 18px">Today\'s Sales:</b><br><b style="font-size: 36px">Rs. {sum_b}</b><br><span style="{positive_style if sum_b - sum_b_yesterday > 0 else negative_style}">{calculate_percentage_change(sum_b_yesterday,sum_b)}</span> </div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{box_style}"><b style="font-size: 18px">This Week Sales:</b><br><b style="font-size: 36px">Rs. {sum_b_week}</b><br><span style="{positive_style if sum_b_week - sum_b_last_week > 0 else negative_style}">{calculate_percentage_change(sum_b_last_week,sum_b_week)}</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{box_style}"><b style="font-size: 18px">This Month Sales:</b><br><b style="font-size: 36px">Rs. {sum_b_month}</b><br><span style="{positive_style if sum_b_month - sum_b_last_month > 0 else negative_style}">{calculate_percentage_change(sum_b_last_month,sum_b_month)}</span></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{box_style}"><b style="font-size: 18px">This Year Sales:</b><br><b style="font-size: 36px">Rs. {sum_b_year}</b><br><span style="{positive_style if sum_b_year - sum_b_last_year > 0 else negative_style}">{calculate_percentage_change(sum_b_last_year,sum_b_year)}</span></div>', unsafe_allow_html=True)




st.write("Sales Value (Debit):")
# Todays Transactions
current_datetime = datetime.now()
start_of_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = current_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
start_time = start_of_day.isoformat()
end_time = end_of_day.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{start_time}&created_at=lte.{end_time}&Transaction Type=eq.Debited"
response = requests.get(url, headers={"apikey": supabase_key})

if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase.{response.text}")
    sum_b=0


# Today-1 Transactions
yesterday = current_datetime - timedelta(days=1)
start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{start_of_yesterday}&created_at=lte.{end_of_yesterday}&Transaction Type=eq.Debited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_yesterday = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_yesterday=0


# Current Month Transactions
current_datetime = datetime.now()
start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
next_month = current_datetime.replace(day=1, month=current_datetime.month + 1)
if next_month.month == 1:
    next_month = next_month.replace(year=current_datetime.year + 1)
start_time = start_of_month.isoformat()
end_time = next_month.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{start_time}&created_at=lt.{end_time}&Transaction Type=eq.Debited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_month = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")

# Last month
current_datetime = datetime.now()
start_of_current_month = current_datetime.replace(day=1)
start_of_last_month = (start_of_current_month - timedelta(days=1)).replace(day=1)
end_of_last_month = start_of_current_month - timedelta(days=1)
start_time = start_of_last_month.isoformat()
end_time = end_of_last_month.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{start_time}&created_at=lt.{end_time}&Transaction Type=eq.Debited"
response = requests.get(url, headers={"apikey": supabase_key})

if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_last_month = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_last_month=0

# current week
current_datetime = datetime.now()
current_week_start = current_datetime - timedelta(days=current_datetime.weekday(), hours=current_datetime.hour, minutes=current_datetime.minute, seconds=current_datetime.second)
current_week_end = current_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
current_week_start_iso = current_week_start.isoformat()
current_week_end_iso = current_week_end.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{current_week_start_iso}&created_at=lt.{current_week_end_iso}&Transaction Type=eq.Debited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_week = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_week=0

# Last week
current_datetime = datetime.now()
current_week_start = current_datetime - timedelta(days=current_datetime.weekday(), hours=current_datetime.hour, minutes=current_datetime.minute, seconds=current_datetime.second)
current_week_end = current_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
last_week_start = current_week_start - timedelta(days=7)
last_week_end = last_week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
last_week_start_iso = last_week_start.isoformat()
last_week_end_iso = last_week_end.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{last_week_start_iso}&created_at=lt.{last_week_end_iso}&Transaction Type=eq.Debited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_last_week = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_last_week=0


# last Year
current_datetime = datetime.now()
last_year_start = datetime(current_datetime.year - 1, 1, 1)
last_year_end = datetime(current_datetime.year - 1, 12, 31, 23, 59, 59)
last_year_start_iso = last_year_start.isoformat()
last_year_end_iso = last_year_end.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{last_year_start_iso}&created_at=lt.{last_year_end_iso}&Transaction Type=eq.Debited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_last_year = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_last_year=0

# Current Year
current_datetime = datetime.now()
current_year_start = current_datetime.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
next_year_start = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0, 0)
current_year_end = next_year_start - timedelta(seconds=1)
current_year_start_iso = current_year_start.isoformat()
current_year_end_iso = current_year_end.isoformat()
url = f"{supabase_url}/rest/v1/{table_name}?created_at=gte.{current_year_start_iso}&created_at=lt.{current_year_end_iso}&Transaction Type=eq.Debited"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    
    valid_values = [item['Amount'] for item in data if item['Amount'].isdigit()]
    sum_b_year = sum(map(int, valid_values))
else:
    st.write(f"Error fetching data from Supabase. Response Text: {response.text}")
    sum_b_year=0





col1, col2, col3, col4 = st.columns(4)
box_style = """
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    margin: 10px;
    text-align: center;
"""
# Define CSS styles for positive and negative values
positive_style = 'color: green; font-weight: bold;'
negative_style = 'color: red; font-weight: bold;'

def calculate_percentage_change(old_value, new_value):
    if old_value == 0:
        percentage_change = ((new_value - 1) / 1) * 100
        return ""  # Avoid division by zero
    percentage_change = ((new_value - old_value) / old_value) * 100
    return str(round(percentage_change))+"%"

with col1:
    st.markdown(f'<div style="{box_style}"><b style="font-size: 18px">Today\'s Sales:</b><br><b style="font-size: 36px">Rs. {sum_b}</b><br><span style="{positive_style if sum_b - sum_b_yesterday > 0 else negative_style}">{calculate_percentage_change(sum_b_yesterday,sum_b)}</span> </div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="{box_style}"><b style="font-size: 18px">This Week Sales:</b><br><b style="font-size: 36px">Rs. {sum_b_week}</b><br><span style="{positive_style if sum_b_week - sum_b_last_week > 0 else negative_style}">{calculate_percentage_change(sum_b_last_week,sum_b_week)}</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div style="{box_style}"><b style="font-size: 18px">This Month Sales:</b><br><b style="font-size: 36px">Rs. {sum_b_month}</b><br><span style="{positive_style if sum_b_month - sum_b_last_month > 0 else negative_style}">{calculate_percentage_change(sum_b_last_month,sum_b_month)}</span></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div style="{box_style}"><b style="font-size: 18px">This Year Sales:</b><br><b style="font-size: 36px">Rs. {sum_b_year}</b><br><span style="{positive_style if sum_b_year - sum_b_last_year > 0 else negative_style}">{calculate_percentage_change(sum_b_last_year,sum_b_year)}</span></div>', unsafe_allow_html=True)





# Table - Full Data

url = f"{supabase_url}/rest/v1/dts"
response = requests.get(url, headers={"apikey": supabase_key})
if response.status_code == 200:
    data = response.json()
    data = sorted(data, key=lambda x: datetime.fromisoformat(x.get("created_at")), reverse=True)
    for row in data:
        if "created_at" in row:
            row["created_at"] = datetime.fromisoformat(row["created_at"]).strftime("%d-%m-%Y %H:%M")
        if "created_at" in row:
            row["Amount"] = "Rs. "+row["Amount"]
    st.write(f"Data from the 'Sales' table:")
    for row in data:
        row.pop("id", None)

    st.table(data)
else:
    st.write(f"Error fetching data from the 'dts' table. Response Text: {response.text}")




