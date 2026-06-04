import streamlit as st
import time
from agent import Agent

# =====================================
# PAGE CONFIG (MUST BE FIRST)
# =====================================

st.set_page_config(
    page_title="Nexus AI",
    page_icon="⚡",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

/* Main page */
.block-container {
    padding-top: 0rem;
    max-width: 900px;
}

/* Sidebar */
[data-testid="stSidebar"] .block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
}

/* Remove extra top margin in sidebar */
[data-testid="stSidebar"] {
    padding-top: 0rem;
}

/* Chat messages */
.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================

st.markdown("""
<div style='text-align:center;'>

<h1 style='
margin-top:0px;
margin-bottom:0px;
font-size:60px;
background: linear-gradient(90deg,#4F46E5,#06B6D4);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
'>
Nexus AI
</h1>

<p style='
margin-top:0px;
font-size:18px;
color:#888;
'>
Chat • Analyze • Calculate • Explore
</p>

</div>
""", unsafe_allow_html=True)

# =====================================
# AGENT
# =====================================

agent = Agent()

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.markdown(
        "<div style='margin-top:-80px'></div>",
        unsafe_allow_html=True
    )

    st.markdown("## 📂 Documents")

    uploaded_file = st.file_uploader(
        "Upload a file",
        type=["xlsx", "py", "pdf"]
    )

    st.divider()

    st.markdown("## ⚡ Agent Status")

    st.success("🟢 Online")

    st.write("### Available Tools")

    st.write("➕ Calculator")
    st.write("📊 Excel")
    st.write("🐍 Python")
    st.write("📄 PDF")
    st.write("🌐 Web Search")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================
# CHAT HISTORY
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )

# =====================================
# CHAT INPUT
# =====================================

question = st.chat_input(
    "Ask anything..."
)

# =====================================
# USER MESSAGE
# =====================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    file_name = None

    # Save uploaded file locally
    if uploaded_file:

        file_name = uploaded_file.name

        with open(
            file_name,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

    # =====================================
    # THINKING ANIMATION
    # =====================================

    with st.spinner(
        "🤔 Nexus AI is thinking..."
    ):

        result = agent.answer(
            question,
            file_name
        )

    # =====================================
    # ASSISTANT RESPONSE
    # =====================================

    with st.chat_message("assistant"):

        st.info(
            f"🔧 Tool Used: {result['tool']}"
        )

        st.caption(
            f"🧠 {result['reason']}"
        )

        placeholder = st.empty()

        final_text = ""

        for char in result["answer"]:

            final_text += char

            placeholder.markdown(
                final_text
            )

            time.sleep(0.01)

    # =====================================
    # SAVE CHAT HISTORY
    # =====================================

    history_text = f"""
🔧 **Tool Used:** {result['tool']}

🧠 **Reason:** {result['reason']}

✅ **Answer:** {result['answer']}
"""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": history_text
        }
    )