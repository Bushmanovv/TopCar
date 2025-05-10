import streamlit as st
import pandas as pd
from db import get_connection

class BranchTable:
    def render(self):
        st.markdown("<div class='neon-title'>🏢 Branch Table</div>", unsafe_allow_html=True)
        self.insert_form()
        self.view_records()
        self.update_record()
        self.delete_record()

    def insert_form(self):
        st.subheader("Add a New Branch")
        bid = st.number_input("Branch ID", step=1)
        city = st.text_input("City")
        address = st.text_input("Address")

        if st.button("Insert Branch"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Branch VALUES (%s, %s, %s)", (bid, city, address))
                conn.commit()
                st.success("✅ Branch added successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()

    def view_records(self):
        st.subheader("View All Branches")
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Branch", conn)
        st.dataframe(df)
        conn.close()

    def update_record(self):
        st.subheader("Update Branch Record")

        # Load branch data
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Branch", conn)

        # Search by BranchID
        search_id = st.text_input("Search by Branch ID")

        if search_id.isdigit():
            branch_id = int(search_id)
            filtered_df = df[df["BranchID"] == branch_id]
        else:
            filtered_df = df

        # Display branch table
        st.markdown("Click a row below to select a branch to update:")
        selected_rows = st.data_editor(
            filtered_df,
            use_container_width=True,
            disabled=True,
            num_rows="dynamic",
            key="branch_update_editor"
        )

        if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
            selected_branch = selected_rows.iloc[0]

            st.markdown("Edit Branch Details")
            branch_id = int(selected_branch["BranchID"])  # ensure it's Python int
            city = st.text_input("City", selected_branch["City"])
            address = st.text_input("Address", selected_branch["Address"])

            if st.button("Update Branch Record"):
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE Branch SET City = %s, Address = %s WHERE BranchID = %s
                    """, (city, address, branch_id))
                    conn.commit()
                    st.success(f"Updated branch with ID {branch_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
        else:
            st.info("No branch selected.")
            conn.close()

    def delete_record(self):
        st.subheader("Delete Branch")
        bid = st.number_input("Branch ID to Delete", step=1)
        if st.button("Delete Branch"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Branch WHERE BranchID = %s", (bid,))
                conn.commit()
                st.success(f"🗑️ Deleted branch with ID {bid}.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()
