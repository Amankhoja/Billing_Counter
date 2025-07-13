import streamlit as st
import urllib.parse

st.set_page_config(page_title="Billing Counter Closure", layout="centered")

st.title("💰 Billing Counter Closure Tool")

st.markdown("Enter the count of each denomination to close the billing counter. This tool will calculate how much to remove to keep **exactly $150** in the drawer.")

# Denominations
denominations = {
    "0.05": "5 cents",
    "0.10": "10 cents",
    "0.25": "25 cents",
    "1.00": "1 dollar",
    "2.00": "2 dollars",
    "5.00": "5 dollars",
    "10.00": "10 dollars",
    "20.00": "20 dollars",
    "50.00": "50 dollars"
}

user_counts = {}
total_amount = 0

st.subheader("🧮 Step 1: Enter Denomination Counts")

col1, col2 = st.columns(2)
for i, (value_str, label) in enumerate(denominations.items()):
    col = col1 if i % 2 == 0 else col2
    count = col.number_input(f"{label}:", min_value=0, step=1, key=label)
    value = float(value_str)
    user_counts[value] = count
    total_amount += count * value

st.markdown(f"### 🧾 Total Cash in Drawer: **${total_amount:.2f}**")

if total_amount < 150:
    st.warning("⚠️ Total cash is less than $150. No need to remove anything.")
else:
    st.subheader("🧹 Step 2: Remove Extra Cash to Keep $150")

    to_remove = {}
    remaining_to_remove = total_amount - 150

    # Sort in descending order
    for denom in sorted(user_counts.keys(), reverse=True):
        available = user_counts[denom]
        max_remove = min(int(remaining_to_remove // denom), available)
        if max_remove > 0:
            to_remove[denom] = max_remove
            remaining_to_remove -= max_remove * denom
            remaining_to_remove = round(remaining_to_remove, 2)

    with st.expander("📦 Breakdown to REMOVE"):
        for denom, count in to_remove.items():
            st.write(f"{denominations[f'{denom:.2f}']}: Remove {count}")
        st.write(f"**Total Removed: ${total_amount - 150:.2f}**")
        if remaining_to_remove > 0:
            st.warning(f"⚠️ Could not reach exactly $150. ${remaining_to_remove:.2f} leftover due to rounding.")

    st.subheader("📤 Final Report for Manager")

    # Prepare manager message with total and original counts (not remaining)
    report = f"Total Cash Before Closing: ${total_amount:.2f}\n"
    report += "📋 Denomination Breakdown:\n"
    for denom, count in user_counts.items():
        if count > 0:
            report += f"- {denominations[f'{denom:.2f}']}: {count}\n"
    report += f"\n🧾 Total Removed to Keep $150: ${total_amount - 150:.2f}"

    st.code(report, language="text")

    # WhatsApp sharing link
    encoded_msg = urllib.parse.quote(report)
    whatsapp_url = f"https://wa.me/?text={encoded_msg}"
    st.markdown(f"📲 [Send to Manager on WhatsApp]({whatsapp_url})", unsafe_allow_html=True)

st.markdown("---")
st.caption("Mobile-ready • Fast • Simple")
