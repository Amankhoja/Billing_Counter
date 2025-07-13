import streamlit as st
import urllib.parse

st.set_page_config(page_title="Billing Counter", layout="centered")

st.markdown("<h1 style='text-align:center;'>💰 Billing Counter Closure Tool</h1>", unsafe_allow_html=True)
st.markdown("Enter the count of each denomination to close the billing counter. This tool will calculate how much to remove to keep <strong>exactly $150</strong> in the drawer.", unsafe_allow_html=True)
st.divider()

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

with st.form("cash_form"):
    st.subheader("📥 Step 1: Enter Denominations")

    for value_str, label in denominations.items():
        value = float(value_str)
        user_counts[value] = st.number_input(label, min_value=0, step=1, key=label)

    submitted = st.form_submit_button("✅ Calculate")

if submitted:
    for denom, count in user_counts.items():
        total_amount += denom * count

    st.success(f"🧾 Total Cash: **${total_amount:.2f}**")

    if total_amount < 150:
        st.warning("You don't need to remove anything. Total is under $150.")
    else:
        to_remove = {}
        remaining_to_remove = total_amount - 150

        for denom in sorted(user_counts.keys(), reverse=True):
            available = user_counts[denom]
            max_remove = min(int(remaining_to_remove // denom), available)
            if max_remove > 0:
                to_remove[denom] = max_remove
                remaining_to_remove -= max_remove * denom
                remaining_to_remove = round(remaining_to_remove, 2)

        report = f"💰 Total Cash Before Closing: ${total_amount:.2f}\n📋 Denomination Breakdown:\n"
        for denom, count in user_counts.items():
            if count > 0:
                report += f"- {denominations[f'{denom:.2f}']}: {count}\n"
        report += f"\n🧾 Total Removed to Keep $150: ${total_amount - 150:.2f}"

        with st.expander("📦 Breakdown to REMOVE"):
            for denom, count in to_remove.items():
                st.write(f"{denominations[f'{denom:.2f}']}: Remove {count}")
            if remaining_to_remove > 0:
                st.warning(f"⚠️ Could not reach exactly $150. ${remaining_to_remove:.2f} leftover.")

        st.subheader("📤 Message for Manager")
        st.code(report, language="text")

        encoded_msg = urllib.parse.quote(report)
        whatsapp_url = f"https://wa.me/?text={encoded_msg}"
        st.markdown(f"📲 [Send to Manager on WhatsApp]({whatsapp_url})", unsafe_allow_html=True)

st.divider()
st.caption("Optimized for mobile | Created with ❤️ using Streamlit")
