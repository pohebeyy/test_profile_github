import requests
import streamlit as st

PROJECT_TYPES = {
    "Веб-приложение": 0,
    "Бот или API": 1,
    "Анализ данных / ML": 2,
    "Игра / интерактив": 3,
    "Другое": 4,
}

st.title("Оценка GitHub-профиля")
st.write("Модель оценивает, насколько профиль выглядит живым,")

with st.form("project_form"):
    repos = st.number_input("Репозиториев в профиле", min_value=0, value=8)
    stars = st.number_input("Звезд на GitHub", min_value=0, value=3)
    followers = st.number_input("Подписчиков", min_value=0, value=2)
    recent_commits = st.number_input("Коммитов за 30 дней", min_value=0, value=6)
    project_type = st.selectbox("Тип проекта", list(PROJECT_TYPES.keys()))
    has_readme = st.checkbox("Есть README")
    has_demo = st.checkbox("Есть демо или скриншоты")
    has_tests = st.checkbox("Есть тесты")
    submit = st.form_submit_button("Оценить")

if submit:
    data = {
        "repos": repos,
        "stars": stars,
        "followers": followers,
        "recent_commits": recent_commits,
        "project_type": PROJECT_TYPES[project_type],
        "has_readme": has_readme,
        "has_demo": has_demo,
        "has_tests": has_tests,
    }

    response = requests.post("http://127.0.0.1:8001/score", json=data, timeout=10)
    response.raise_for_status()
    result = response.json()

    probability = result["probability"] * 100
    st.metric("Вероятность сильного проекта", f"{probability:.0f}%")

    if result["strong_project"]:
        st.success("профиль выглядит сильно: его можно смело показывать.")
    else:
        st.warning("профиль пока слабый")
