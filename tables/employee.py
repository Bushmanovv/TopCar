import streamlit as st
import pandas as pd
from db import get_connection

class EmployeeTable:
    def render(self):
        st.markdown("<div class='neon-title'>👨‍💼 Employee Table</div>", unsafe_allow_html=True)
        self.insert_form()
        self.view_records()
        self.update_record()
        self.delete_record()

    def insert_form(self):
        st.subheader("Add a New Employee")
        eid = st.number_input("Employee ID", step=1)
        name = st.text_input("Name")
        dob = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Phone Number")
        base = st.number_input("Base Salary")
        commission = st.number_input("Sales Commission")
        raise_amt = st.number_input("Childs Raise")
        branch_id = st.number_input("Branch ID", step=1)

        if st.button("Insert Employee"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("""INSERT INTO Employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (eid, name, dob, gender, phone, base, commission, raise_amt, branch_id))
                conn.commit()
                st.success("✅ Employee added successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()

    def view_records(self):
        st.subheader("View All Employees")
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Employee", conn)
        st.dataframe(df)
        conn.close()

    def update_record(self):
        st.subheader("Update Employee Record")

        # Load employee data
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Employee", conn)

        # Load branch names
        branches = pd.read_sql("SELECT BranchID, City FROM Branch", get_connection())
        branch_map = dict(zip(branches["City"], branches["BranchID"]))

        # Search bar by EmployeeID
        search_id = st.text_input("Search by Employee ID")

        if search_id.isdigit():
            emp_id = int(search_id)
            filtered_df = df[df["EmployeeID"] == emp_id]
        else:
            filtered_df = df

        # Show employee table
        st.markdown("Click a row below to select an employee to update:")
        selected_rows = st.data_editor(
            filtered_df,
            use_container_width=True,
            disabled=True,
            num_rows="dynamic",
            key="employee_update_editor"
        )

        if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
            selected_emp = selected_rows.iloc[0]

            st.markdown("Edit Employee Details")
            emp_id = int(selected_emp["EmployeeID"])
            name = st.text_input("Name", selected_emp["Name"])
            dob = st.date_input("Date of Birth", pd.to_datetime(selected_emp["DOB"]))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(selected_emp["Gender"]))
            phone = st.text_input("Phone Number", selected_emp["Phone"])
            base = st.number_input("Base Salary", value=float(selected_emp["BaseSalary"]))
            commission = st.number_input("Sales Commission", value=float(selected_emp["SalesCommission"]))
            raise_amt = st.number_input("Childs Raise", value=float(selected_emp["ChildsRaise"]))
            branch_name = st.selectbox("Branch", list(branch_map.keys()), index=list(branch_map.values()).index(int(selected_emp["BranchID"])))
            branch_id = branch_map[branch_name]

            if st.button("Update Employee Record"):
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE Employee
                        SET Name=%s, DOB=%s, Gender=%s, Phone=%s,
                            BaseSalary=%s, SalesCommission=%s, ChildsRaise=%s, BranchID=%s
                        WHERE EmployeeID = %s
                    """, (name, dob, gender, phone, base, commission, raise_amt, branch_id, emp_id))
                    conn.commit()
                    st.success(f"Updated employee with ID {emp_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
        else:
            st.info("No employee selected.")
            conn.close()

    def delete_record(self):
        st.subheader("Delete Employee")
        eid = st.number_input("Employee ID to Delete", step=1)
        if st.button("Delete Employee"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Employee WHERE EmployeeID = %s", (eid,))
                conn.commit()
                st.success(f"🗑️ Deleted employee with ID {eid}.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()
