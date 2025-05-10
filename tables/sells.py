import streamlit as st
import pandas as pd
from db import get_connection

class SellsTable:
    def render(self):
        st.markdown("<div class='neon-title'>📈 Sells Table</div>", unsafe_allow_html=True)
        self.insert_form()
        self.view_records()
        self.update_record()
        self.delete_record()

    def insert_form(self):
        st.subheader("Add a New Sale")
        vin = st.text_input("Car VIN")
        employee_id = st.number_input("Employee ID", step=1)
        customer_id = st.number_input("Customer ID", step=1)
        date_of_sale = st.date_input("Date of Sale")

        if st.button("Insert Sale"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO Sells (VIN, EmployeeID, CustomerID, DateOfSale)
                    VALUES (%s, %s, %s, %s)
                """, (vin, employee_id, customer_id, date_of_sale))
                conn.commit()
                st.success("✅ Sale recorded successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()

    def view_records(self):
        st.subheader("View All Sales")
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Sells", conn)
        st.dataframe(df)
        conn.close()

    def update_record(self):
        st.subheader("Update Sale Record")

        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Sells", conn)

        search_vin = st.text_input("Search by VIN")

        if search_vin:
            filtered_df = df[df["VIN"].str.contains(search_vin, case=False, na=False)]
        else:
            filtered_df = df

        st.markdown("Click a row below to select a sale to update:")
        selected_rows = st.data_editor(
            filtered_df,
            use_container_width=True,
            disabled=True,
            num_rows="dynamic",
            key="sells_update_editor"
        )

        if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
            sale = selected_rows.iloc[0]

            st.markdown("Edit Sale Details")
            vin = sale["VIN"]
            employee_id = st.number_input("Employee ID", step=1, value=int(sale["EmployeeID"]))
            customer_id = st.number_input("Customer ID", step=1, value=int(sale["CustomerID"]))
            date_of_sale = st.date_input("Date of Sale", pd.to_datetime(sale["DateOfSale"]))

            if st.button("Update Sale Record"):
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE Sells
                        SET EmployeeID=%s, CustomerID=%s, DateOfSale=%s
                        WHERE VIN=%s AND EmployeeID=%s AND CustomerID=%s
                    """, (employee_id, customer_id, date_of_sale, vin, sale["EmployeeID"], sale["CustomerID"]))
                    conn.commit()
                    st.success(f"Updated sale for VIN {vin}")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
        else:
            st.info("No sale record selected.")
            conn.close()

    def delete_record(self):
        st.subheader("Delete Sale Record")
        vin = st.text_input("VIN to Delete")
        employee_id = st.number_input("Employee ID", step=1)
        customer_id = st.number_input("Customer ID", step=1)
        if st.button("Delete Sale"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("""
                    DELETE FROM Sells
                    WHERE VIN = %s AND EmployeeID = %s AND CustomerID = %s
                """, (vin, employee_id, customer_id))
                conn.commit()
                st.success(f"🗑️ Deleted sale record for VIN {vin}.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()
