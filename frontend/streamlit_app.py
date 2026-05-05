import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Business Copilot",
    page_icon="📈",
    layout="wide"
)

# -------------------------
# SESSION STATE
# -------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# -------------------------
# HELPERS
# -------------------------
def login_user(email, password):
    try:
        res = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}


def register_user(email, password):
    try:
        res = requests.post(
            f"{BASE_URL}/auth/register",
            json={"email": email, "password": password}
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}


def upload_file(file, token):
    try:
        files = {"file": file}
        params = {"token": token}

        res = requests.post(
            f"{BASE_URL}/upload/",
            files=files,
            params=params
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}


def ask_ai(user_id, query):
    try:
        res = requests.post(
            f"{BASE_URL}/chat/",
            json={
                "user_id": user_id,
                "query": query
            }
        )
        return res.json()
    except Exception as e:
        return {"error": str(e)}


# -------------------------
# SIDEBAR NAV
# -------------------------
st.sidebar.title("AI Business Copilot")

page = st.sidebar.radio(
    "Navigate",
    ["Login", "Upload", "Dashboard", "Copilot Chat"]
)

st.sidebar.markdown("---")
if st.session_state.user_id:
    st.sidebar.success(f"Logged in")
    st.sidebar.caption(f"User ID: {st.session_state.user_id}")


# -------------------------
# LOGIN PAGE
# -------------------------
if page == "Login":
    st.title("🚀 AI Business Copilot")
    st.subheader("Login or Register")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register"):
            result = register_user(email, password)
            if "message" in result:
                st.success(result["message"])
            else:
                st.error(result)

    with col2:
        if st.button("Login"):
            result = login_user(email, password)

            if "access_token" in result:
                st.session_state.token = result["access_token"]

                # decode user id from login response
                if "user" in result and "user_id" in result["user"]:
                    st.session_state.user_id = result["user"]["user_id"]

                st.success("Login successful!")
            else:
                st.error(result)


# -------------------------
# UPLOAD PAGE
# -------------------------
elif page == "Upload":
    st.title("📂 Upload Business Data")

    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

        if st.button("Analyze Business"):
            if uploaded_file is None:
                st.warning("Please upload a CSV file.")
            else:
                with st.spinner("Analyzing your business..."):
                    result = upload_file(uploaded_file, st.session_state.token)

                if "analysis" in result:
                    st.session_state.analysis = result["analysis"]
                    st.success("Business analysis completed!")
                    st.json(result["analysis"])
                else:
                    st.error(result)


# -------------------------
# DASHBOARD PAGE
# -------------------------
elif page == "Dashboard":
    st.title("📊 Business Dashboard")

    if st.session_state.analysis is None:
        st.warning("Upload and analyze data first.")
    else:
        analysis = st.session_state.analysis

        st.subheader("Key Metrics")

        metrics = analysis.get("metrics", {})

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Revenue", metrics.get("total_revenue", 0))
            st.metric("Avg Revenue", metrics.get("average_revenue", 0))

        with col2:
            st.metric("Top Location", metrics.get("top_location", "N/A"))
            st.metric("Customers", metrics.get("total_customers", 0))

        with col3:
            st.metric("Avg Discount", metrics.get("average_discount", 0))

        st.markdown("---")
        st.subheader("AI Insights")

        for insight in analysis.get("insights", []):
            st.success(insight)


# -------------------------
# CHAT PAGE
# -------------------------
elif page == "Copilot Chat":
    st.title("🤖 AI Strategy Copilot")

    if not st.session_state.user_id:
        st.warning("Please login first.")
    else:
        query = st.text_input("Ask your business question")

        if st.button("Ask AI"):
            if not query:
                st.warning("Enter a question first.")
            else:
                with st.spinner("Thinking..."):
                    result = ask_ai(st.session_state.user_id, query)

                if "answer" in result:
                    st.subheader("Answer")
                    st.write(result["answer"])

                    st.subheader("Context Used")
                    st.json(result.get("context", []))
                else:
                    st.error(result)