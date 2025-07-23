import streamlit as st
import pandas as pd
import mysql.connector

config = {
    'host'    :'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
    'port'    : 4000,
    'user'    :'n4Chu4sX3kRNKGe.root',
    'password':'dgn21fITQBuAvfcM',
    'database':'students_data',
    'ssl_disabled':False,
    'ssl_ca':r'C:\Users\HP\OneDrive\Documents\ca.pem'
}

db=mysql.connector.connect(**config)
cursor = db.cursor()
'''
st.title("Placement Eligiblity App")
query = st.text_area("write your query")
st.code("select * from students",language="SQL")
if st.button("submit"):
    df=pd.read_sql(query,con=db)
    st.dataframe(df)'''

st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("🎓 Placement Eligibility & Insights App")

# ----------------- Eligibility Filter UI -----------------
st.header("🔍 Student Eligibility Filter")

# Define dropdown values
problem_options = list(range(0, 260, 10))  # 0, 10, 20, ..., 250
softskill_options = list(range(0, 110, 5))  # 0, 5, ..., 100

# Dropdowns
min_problems = st.selectbox("Select Minimum Problems Solved", problem_options, index=5)  # default = 50
min_soft_skill = st.selectbox("Select Minimum Avg Soft Skill Score", softskill_options, index=15)  # default = 75

# Eligibility Query
eligibility_query = f"""
SELECT s.student_id, s.name, s.email, s.city, p.problems_solved,
       ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6, 2) AS avg_soft_skills
FROM students s
JOIN programming p ON s.student_id = p.student_id
JOIN soft_skills ss ON s.student_id = ss.student_id
WHERE p.problems_solved >= {min_problems}
  AND (ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6 >= {min_soft_skill}
"""

if st.button("🔍 Show Eligible Students"):
    df = pd.read_sql(eligibility_query, con=db)
    st.success(f"{len(df)} eligible student(s) found.")
    st.dataframe(df)


# ----------------- Insights Section -----------------
st.header("📊 Insights from Student Database")

queries = {
    "1.  Average Programming Score by Year": """
         SELECT s.graduation_year AS year,
           AVG(p.problems_solved) AS avg_problems_solved,
           AVG(p.latest_project_score) AS avg_project_score,
           AVG(p.assessments_completed) AS avg_assessments,
           AVG(p.certifications_earned) AS avg_certifications
          FROM students s
          JOIN programming p ON s.student_id = p.student_id
          GROUP BY s.graduation_year
          ORDER BY s.graduation_year;
    """,

    "2. Top 5 Students Ready for Placement": """
        SELECT s.name, p.problems_solved,
        ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6, 2) AS avg_skills
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        ORDER BY p.problems_solved DESC, avg_skills DESC
        LIMIT 5
    """,

    "3. Soft Skills Distribution": """
        SELECT
          'communication' AS skill, AVG(communication) AS average FROM soft_skills
        UNION ALL
        SELECT 'teamwork', AVG(teamwork) FROM soft_skills
        UNION ALL
        SELECT 'presentation', AVG(presentation) FROM soft_skills
        UNION ALL
        SELECT 'leadership', AVG(leadership) FROM soft_skills
        UNION ALL
        SELECT 'critical_thinking', AVG(critical_thinking) FROM soft_skills
        UNION ALL
        SELECT 'interpersonal_skills', AVG(interpersonal_skills) FROM soft_skills
    """,

    "4. Number of Students per City": """
        SELECT city, COUNT(*) AS total_students
        FROM students
        GROUP BY city
        ORDER BY total_students DESC
    """,

    "5. Students with >200 Problems Solved": """
        SELECT s.name, p.problems_solved
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        WHERE p.problems_solved > 200
    """,

    "6. Students with Perfect Communication Score": """
        SELECT s.name, ss.communication
        FROM students s
        JOIN soft_skills ss ON s.student_id = ss.student_id
        WHERE ss.communication = 100
    """,

    "7. Students from Each Batch with Max Soft Skills": """
        SELECT s.course_batch, s.name,
        (ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills) AS total_skills
        FROM students s
        JOIN soft_skills ss ON s.student_id = ss.student_id
        ORDER BY s.course_batch, total_skills DESC
    """,

    "8. Average Soft Skill Score by Batch": """
         SELECT 
            s.course_batch,
            ROUND(AVG((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6), 2) AS avg_soft_skills
         FROM students s
           JOIN soft_skills ss ON s.student_id = ss.student_id
           GROUP BY s.course_batch
           ORDER BY s.course_batch;
    """  ,

    "9. Students with 100 in Any Soft Skill": """
        SELECT s.student_id AS s_id, s.name AS s_name,
               ss.communication, ss.teamwork, ss.presentation,
               ss.leadership, ss.critical_thinking, ss.interpersonal_skills
        FROM students s
        JOIN soft_skills ss ON s.student_id = ss.student_id
        WHERE 100 IN (
            ss.communication, ss.teamwork, ss.presentation,
            ss.leadership, ss.critical_thinking, ss.interpersonal_skills
        )
    """,

    "10. Average Problems Solved per City": """
        SELECT s.city, AVG(p.problems_solved) AS avg_problems
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        GROUP BY s.city
        ORDER BY avg_problems DESC
    """
}

# Query selector
selected_query = st.selectbox("📌 Choose an insight query", list(queries.keys()))

if st.button("Run Query"):
    result_df = pd.read_sql(queries[selected_query], con=db)
    st.write(f"📄 Query: {selected_query}")
    st.dataframe(result_df)