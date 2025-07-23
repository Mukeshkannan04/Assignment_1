from faker import Faker
import pandas as pd
import random


class StudentDataGenerator:
    def __init__(self, total_students=500):
        self.fake = Faker()
        self.total_students = total_students
        self.students_df = None

    def generate_students(self):
        students = []
        for i in range(1, self.total_students + 1):
            students.append({
                'student_id': i,
                'name': self.fake.name(),
                'age': random.randint(18, 40),
                'gender': random.choice(['Male', 'Female', 'Others']),
                'email': self.fake.email(),
                'phone': self.fake.phone_number(),
                'enrollment_year': random.randint(2019, 2023),
                'course_batch':random.choice(['DS-JAN','DS-APR','DS-JUL','DS-OCT']),
                'city': self.fake.city(),
                'graduation_year': random.randint(2023, 2026)
            })
        self.students_df = pd.DataFrame(students)
        return self.students_df

    def generate_programming(self):
        if self.students_df is None:
            raise Exception("Students data must be generated first.")
        
        programming = []
        for student_id in self.students_df['student_id']:
            programming.append({
                'programming_id': student_id,
                'student_id': student_id,
                'language': random.choice(['Python', 'SQL', 'JavaScript']),
                'problems_solved': random.randint(0, 250),
                'assessments_completed': random.randint(0, 10),
                'mini_projects': random.randint(0, 5),
                'certifications_earned': random.randint(0, 3),
                'latest_project_score': random.randint(50, 100)
            })
        return pd.DataFrame(programming)

    def generate_soft_skills(self):
        if self.students_df is None:
            raise Exception("Students data must be generated first.")
        
        soft_skills = []
        for student_id in self.students_df['student_id']:
            soft_skills.append({
                'soft_skill_id': student_id,
                'student_id': student_id,
                'communication': random.randint(50, 100),
                'teamwork': random.randint(50, 100),
                'presentation': random.randint(50, 100),
                'leadership': random.randint(50, 100),
                'critical_thinking': random.randint(50, 100),
                'interpersonal_skills': random.randint(50, 100)
            })
        return pd.DataFrame(soft_skills)

    def generate_placements(self):
        if self.students_df is None:
            raise Exception("Students data must be generated first.")
        
        placements = []
        for student_id in self.students_df['student_id']:
            status = random.choice(['Ready', 'Not Ready', 'Placed'])
            company = self.fake.company() if status == 'Placed' else None
            package = round(random.uniform(3, 15), 2) if status == 'Placed' else None
            placement_date = self.fake.date_between(start_date='-1y', end_date='today') if status == 'Placed' else None

            placements.append({
                'placement_id': student_id,
                'student_id': student_id,
                'mock_interview_score': random.randint(30, 100),
                'internships_completed': random.randint(0, 3),
                'placement_status': status,
                'company_name': company,
                'placement_package': package,
                'interview_rounds_cleared': random.randint(0, 5),
                'placement_date': placement_date
            })
        return pd.DataFrame(placements)


#-------------------------------------------------------------
# Pushing the above data sql database

from sqlalchemy import create_engine


class DatabaseManager:
    def __init__(self, user, password, host, port, db_name, ca_cert_path=None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.ca_cert_path = ca_cert_path
        self.engine = self._create_engine()

    def _create_engine(self):
        connection_string = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

        if self.ca_cert_path:  # TiDB Cloud (requires SSL)
            return create_engine(
                connection_string,
                connect_args={"ssl": {"ca": self.ca_cert_path}}
            )
        else:  # Local MySQL
            return create_engine(connection_string)

    def push_dataframe(self, df, table_name):
        df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)
        print(f"✅ {table_name} table pushed successfully.")



# Assuming your StudentDataGenerator class is already imported

# 1. Generate the data
generator = StudentDataGenerator(total_students=500)
students_df = generator.generate_students()
programming_df = generator.generate_programming()
soft_skills_df = generator.generate_soft_skills()
placements_df = generator.generate_placements()

# 2. Set your DB details (choose MySQL or TiDB Cloud)
# ✅ For TiDB Cloud
db = DatabaseManager(
    user="n4Chu4sX3kRNKGe.root",
    password="dgn21fITQBuAvfcM",
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port="4000",
    db_name="students_data",
    ca_cert_path=r"C:\Users\HP\OneDrive\Documents\ca.pem"  # Replace with actual path
)


# 3. Push data to database
db.push_dataframe(students_df, 'students')
db.push_dataframe(programming_df, 'programming')
db.push_dataframe(soft_skills_df, 'soft_skills')
db.push_dataframe(placements_df, 'placements')


