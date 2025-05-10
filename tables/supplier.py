import streamlit as st
import pandas as pd
from db import get_connection

class SupplierTable:
    def render(self):
        st.markdown("<div class='neon-title'>📦 Supplier Table</div>", unsafe_allow_html=True)
        self.insert_form()
        self.view_records()
        self.update_record()
        self.delete_record()

    def insert_form(self):
        st.subheader("Add a New Supplier")
        sid = st.number_input("Supplier ID", step=1)
        name = st.text_input("Supplier Name")
        contact = st.text_input("Contact Info")

        if st.button("Insert Supplier"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Supplier VALUES (%s, %s, %s)", (sid, name, contact))
                conn.commit()
                st.success("✅ Supplier added successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()

    def view_records(self):
        st.subheader("View All Suppliers")
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Supplier", conn)
        st.dataframe(df)
        conn.close()

    def update_record(self):
        st.subheader("Update Supplier Record")

    # Connect and load supplier data
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Supplier", conn)

        # Search bar by Supplier ID
        search_id = st.text_input("Search by Supplier ID")

        if search_id.isdigit():
            supplier_id = int(search_id)
            filtered_df = df[df["SupplierID"] == supplier_id]
        else:
            filtered_df = df

        # Show supplier table under search bar
        st.markdown("Click a row below to select a supplier to update:")
        selected_rows = st.data_editor(
            filtered_df,
            use_container_width=True,
            disabled=True,
            num_rows="dynamic",
            key="supplier_update_editor"
        )

        if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
            selected_supplier = selected_rows.iloc[0]

            st.markdown("Edit Supplier Details")
            supplier_id = int(selected_supplier["SupplierID"])  # ✅ fix type error
            name = st.text_input("Supplier Name", selected_supplier["Name"])
            contact = st.text_input("Contact Info", selected_supplier["Contact"])

            if st.button("Update Supplier Record"):
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE Supplier SET Name = %s, Contact = %s WHERE SupplierID = %s
                    """, (name, contact, supplier_id))
                    conn.commit()
                    st.success(f"Updated supplier with ID {supplier_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
        else:
            st.info("No supplier selected.")
            conn.close()


    def delete_record(self):
        st.subheader("Delete Supplier")
        sid = st.number_input("Supplier ID to Delete", step=1)
        if st.button("Delete Supplier"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Supplier WHERE SupplierID = %s", (sid,))
                conn.commit()
                st.success(f"🗑️ Deleted supplier with ID {sid}.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()
