import streamlit as st
import pandas as pd
from db import get_connection

class CustomerTable:
    def render(self):
        st.markdown("<div class='neon-title'>👤 Customer Table</div>", unsafe_allow_html=True)
        self.insert_form()
        self.view_records()
        self.update_record()
        self.delete_record()

    def insert_form(self):
        st.subheader("Add a New Customer")
        cid = st.number_input("Customer ID", step=1)
        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        date = st.date_input("Purchase Date")

        if st.button("Insert Customer"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Customer VALUES (%s, %s, %s, %s)", (cid, name, phone, date))
                conn.commit()
                st.success("✅ Customer added successfully.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()

    def view_records(self):
        st.subheader("View All Customers")
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Customer", conn)
        st.dataframe(df)
        conn.close()

    def update_record(self):
        st.subheader("Update Customer Record")

        # Load customer data
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Customer", conn)

        # Search bar by CustomerID
        search_id = st.text_input("Search by Customer ID")

        if search_id.isdigit():
            cust_id = int(search_id)
            filtered_df = df[df["CustomerID"] == cust_id]
        else:
            filtered_df = df

        # Display customer table
        st.markdown("Click a row below to select a customer to update:")
        selected_rows = st.data_editor(
            filtered_df,
            use_container_width=True,
            disabled=True,
            num_rows="dynamic",
            key="customer_update_editor"
        )

        if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
            selected_customer = selected_rows.iloc[0]

            st.markdown("Edit Customer Details")
            cust_id = int(selected_customer["CustomerID"])
            name = st.text_input("Customer Name", selected_customer["Name"])
            phone = st.text_input("Phone Number", selected_customer["Phone"])
            purchase_date = st.date_input("Purchase Date", pd.to_datetime(selected_customer["PurchaseDate"]))

            if st.button("Update Customer Record"):
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE Customer
                        SET Name=%s, Phone=%s, PurchaseDate=%s
                        WHERE CustomerID = %s
                    """, (name, phone, purchase_date, cust_id))
                    conn.commit()
                    st.success(f"Updated customer with ID {cust_id}")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
        else:
            st.info("No customer selected.")
            conn.close()


    def delete_record(self):
        st.subheader("Delete Customer")
        cid = st.number_input("Customer ID to Delete", step=1)
        if st.button("Delete Customer"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Customer WHERE CustomerID = %s", (cid,))
                conn.commit()
                st.success(f"🗑️ Deleted customer with ID {cid}.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()
