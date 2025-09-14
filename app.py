import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_bot():
    return pipeline("text-generation", model="gpt2")

bot = load_bot()

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

st.title("🤖 مساعد ذكي بسيط")

user_input = st.text_input("🧑‍💼 اكتب أمر أو سؤال:")

if st.button("إرسال"):
    if user_input.startswith("مهمة:"):
        task = user_input.split("مهمة:")[1].strip()
        st.session_state.tasks.append(task)
        st.success(f"✅ أضفت المهمة: {task}")

    elif user_input.startswith("مصروف:"):
        try:
            desc, amount = user_input.split("مصروف:")[1].split("=")
            st.session_state.expenses.append({
                "الوصف": desc.strip(),
                "المبلغ": float(amount.strip())
            })
            st.success(f"💸 أضفت المصروف: {desc.strip()} = {amount.strip()} ريال")
        except:
            st.error("⚠️ تأكد من التنسيق: مصروف: وصف = مبلغ")

    elif "اعرض المهام" in user_input:
        st.subheader("📋 المهام:")
        if st.session_state.tasks:
            for t in st.session_state.tasks:
                st.write("🔹", t)
        else:
            st.info("لا توجد مهام.")

    elif "اعرض المصروفات" in user_input:
        st.subheader("💰 المصروفات:")
        if st.session_state.expenses:
            for e in st.session_state.expenses:
                st.write(f"{e['الوصف']}: {e['المبلغ']} ريال")
        else:
            st.info("لا توجد مصروفات.")

    else:
        st.write("🤖 المساعد:", bot(user_input, max_length=100, num_return_sequences=1)[0]['generated_text'].replace(user_input, "").strip())

