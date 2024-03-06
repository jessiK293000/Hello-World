import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Task Tracker",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"  # Expand sidebar by default
)

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=['Task', 'Deadline', 'Status'])

def add_task(task, deadline):
    """Add a new task to the DataFrame."""
    new_entry = pd.DataFrame([{'Task': task, 'Deadline': deadline, 'Status': 'To Do'}])
    st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)

def mark_task_done(task_index):
    """Mark a task as done."""
    if not st.session_state.df.empty:
        st.session_state.df.at[task_index, 'Status'] = 'Erledigt'

def delete_task(task_index):
    """Delete a task from the DataFrame."""
    if not st.session_state.df.empty:
        st.session_state.df.drop(task_index, inplace=True)
        st.session_state.df.reset_index(drop=True, inplace=True)

def display_tasks():
    """Display the tasks in the app."""
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
        for index, row in st.session_state.df.iterrows():
            if st.button(f"Task {index + 1} erledigt"):
                mark_task_done(index)
                st.experimental_rerun()  # Rerun the app to update the display
            if st.button(f"Delete Task {index + 1}"):
                delete_task(index)
                st.experimental_rerun()  # Rerun the app to update the display
    else:
        st.write("No tasks to display.")

def main():
    st.title("Task Tracker")
    init_dataframe()
    with st.sidebar:
        st.header("Add New Task")
        task = st.text_input("Task")
        deadline = st.date_input("Deadline", min_value=datetime.today())
        add_button = st.button("Add Task")

        if add_button:
            add_task(task, deadline)

    # Text elements: Title and Header
    st.markdown(
        "<h1 style='color: #333; background-color: #f39c12; padding: 10px; font-weight: bold;'>Behalte den Überblick über deine Aufgaben.</h1>",
        unsafe_allow_html=True
    )
    st.write("Hier kannst du deine Aufgaben organisieren und verfolgen.")

    # Data elements: Display tasks in a dataframe
    display_tasks()

    # Input Widgets: Text input and date input for adding new tasks
    # Optional: Filter by status
    status_filter = st.sidebar.selectbox("Filter by Status", ["All", "To Do", "Erledigt"])
    if status_filter != "All":
        st.session_state.df = st.session_state.df[st.session_state.df['Status'] == status_filter]

    # Optional: Sort by deadline
    sort_by_deadline = st.sidebar.checkbox("Sort by Deadline")
    if sort_by_deadline:
        st.session_state.df['Deadline'] = pd.to_datetime(st.session_state.df['Deadline'])
        st.session_state.df = st.session_state.df.sort_values(by='Deadline')

    # Chart elements: Display task status counts as a pie chart
    st.markdown(
        "<h2 style='color: #333; background-color: #3498db; padding: 10px; font-weight: bold;'>Aufgabenstatus</h2>",
        unsafe_allow_html=True
    )
    task_status_counts = st.session_state.df['Status'].value_counts()
    st.write(task_status_counts)
    task_status_counts_df = pd.DataFrame({"Status": task_status_counts.index, "Count": task_status_counts.values})
    st.bar_chart(task_status_counts_df.set_index('Status'))

    # Optional: Chat elements
    st.markdown(
        "<h2 style='color: #333; background-color: #e74c3c; padding: 10px; font-weight: bold;'>Chat mit Mitschülern</h2>",
        unsafe_allow_html=True
    )
    st.write("Bereich, um mit anderen Mitschülern über die Aufgaben zu kommunizieren.")

if __name__ == "__main__":
    main()

