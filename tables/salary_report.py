import streamlit as st
import pandas as pd
from db import get_connection

class SalaryReportTable:
    def render(self):
        st.markdown("<div class='neon-title'>💰 Salary Report Table</div>", unsafe_allow_html=True)
        self.insert_form()
        self.view_records()
        self.update_record()
        self.delete_record()

    def insert_form(self):
        st.subheader("Add a New Salary Report")
        employee_id = st.number_input("Employee ID", step=1)
        month = st.selectbox("Month", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"])
        year = st.number_input("Year", min_value=2000, max_value=2030, step=1)
        total_salary = st.number_input("Total Salary")

        if st.button("Insert Salary Report"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO SalaryReport (EmployeeID, Month, Year, TotalSalary)
                    VALUES (%s, %s, %s, %s)
                """, (employee_id, month, year, total_salary))
                conn.commit()
                st.success("✅ Salary report added successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()

    def view_records(self):
        st.subheader("View All Salary Reports")
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM SalaryReport", conn)
        st.dataframe(df)
        conn.close()

    def update_record(self):
        st.subheader("Update Salary Report")

        conn = get_connection()
        df = pd.read_sql("SELECT * FROM SalaryReport", conn)

        search_id = st.text_input("Search by Report ID")

        if search_id.isdigit():
            report_id = int(search_id)
            filtered_df = df[df["ReportID"] == report_id]
        else:
            filtered_df = df

        st.markdown("Click a row below to select a salary report to update:")
        selected_rows = st.data_editor(
            filtered_df,
            use_container_width=True,
            disabled=True,
            num_rows="dynamic",
            key="salary_update_editor"
        )

        if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
            report = selected_rows.iloc[0]

            st.markdown("Edit Salary Report Fields")
            report_id = int(report["ReportID"])
            employee_id = st.number_input("Employee ID", step=1, value=int(report["EmployeeID"]))
            month = st.selectbox("Month", [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ], index=["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"].index(report["Month"]))
            year = st.number_input("Year", min_value=2000, max_value=2030, value=int(report["Year"]))
            total_salary = st.number_input("Total Salary", value=float(report["TotalSalary"]))

            if st.button("Update Salary Report"):
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE SalaryReport SET EmployeeID=%s, Month=%s, Year=%s, TotalSalary=%s
                        WHERE ReportID=%s
                    """, (employee_id, month, year, total_salary, report_id))
                    conn.commit()
                    st.success(f"Updated salary report with ID {report_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
        else:
            st.info("No salary report selected.")
            conn.close()

    def delete_record(self):
        st.subheader("Delete Salary Report")
        report_id = st.number_input("Report ID to Delete", step=1)
        if st.button("Delete Report"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM SalaryReport WHERE ReportID = %s", (report_id,))
                conn.commit()
                st.success(f"🗑️ Deleted report with ID {report_id}.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()
