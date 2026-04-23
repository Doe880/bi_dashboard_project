import hmac
import streamlit as st


def _credentials() -> tuple[str, str]:
    default_user = "admin"
    default_password = "change_me_123"
    secrets = st.secrets if hasattr(st, "secrets") else {}
    username = secrets.get("APP_USERNAME", default_user)
    password = secrets.get("APP_PASSWORD", default_password)
    return username, password


def check_auth() -> None:
    if st.session_state.get("authenticated", False):
        return

    app_user, app_password = _credentials()

    st.title("🔐 Закрытый доступ")
    st.write("Введите логин и пароль для входа в BI-панель.")

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        submitted = st.form_submit_button("Войти", use_container_width=True)

    if submitted:
        is_valid = hmac.compare_digest(username, app_user) and hmac.compare_digest(password, app_password)
        if is_valid:
            st.session_state.authenticated = True
            st.success("Авторизация успешна")
            st.rerun()
        st.error("Неверный логин или пароль")

    st.stop()