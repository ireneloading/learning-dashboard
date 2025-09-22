import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---- App Setup ----
st.set_page_config(page_title="Learning Dashboard", layout="centered")
st.title("📚 Learning Dashboard")
st.write("Track your lessons, note what you learned, and visualize your progress.")

# ---- State Management ----
if "course" not in st.session_state:
    st.session_state.course = None
if "lessons" not in st.session_state:
    st.session_state.lessons = []

# ---- Add Course ----
st.header("➕ Add a New Course")
with st.form("course_form"):
    course_title = st.text_input("Course Title")
    lessons_input = st.text_area("Lessons (one per line)", height=150)
    submit = st.form_submit_button("Add Course")

    if submit and course_title and lessons_input:
        st.session_state.course = course_title
        lessons = lessons_input.strip().split("\n")
        st.session_state.lessons = [{
            "lesson": lesson,
            "completed": False,
            "needs_revision": False,
            "what_learned": ""
        } for lesson in lessons]
        st.success(f"Course '{course_title}' added with {len(lessons)} lessons.")

# ---- Show Lessons ----
if st.session_state.course and st.session_state.lessons:
    st.header(f"📘 {st.session_state.course}")

    for i, lesson in enumerate(st.session_state.lessons):
        st.subheader(f"Lesson {i+1}: {lesson['lesson']}")
        lesson["completed"] = st.checkbox("✅ Completed", value=lesson["completed"], key=f"comp_{i}")
        lesson["needs_revision"] = st.checkbox("🔁 Needs Revision", value=lesson["needs_revision"], key=f"rev_{i}")
        lesson["what_learned"] = st.text_area("📝 What I Learned", value=lesson["what_learned"], key=f"note_{i}")

    # ---- Visual Progress ----
    st.subheader("📊 Progress Overview")
    total = len(st.session_state.lessons)
    completed = sum(1 for l in st.session_state.lessons if l["completed"])
    needs_revision = sum(1 for l in st.session_state.lessons if l["needs_revision"])
    remaining = total - completed - needs_revision

    st.progress(completed / total)
    st.markdown(f"**{completed}/{total} lessons completed**")

    fig, ax = plt.subplots()
    ax.pie(
        [completed, needs_revision, remaining],
        labels=["Completed", "Needs Revision", "Remaining"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

    # ---- Download ----
    st.subheader("📥 Export Progress")
    df = pd.DataFrame(st.session_state.lessons)
    df.insert(0, "Course", st.session_state.course)
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "learning_progress.csv", "text/csv")

else:
    st.info("Start by entering a course and listing lessons.")
