import streamlit as st
import pandas as pd
from db import get_connection

class CarTable:
    def render(self):
        st.markdown("<div class='neon-title'>🚘 Car Table</div>", unsafe_allow_html=True)
        self.insert_form()
        self.view_records()
        self.update_record()
        self.delete_record()

    def insert_form(self):
        st.subheader("Add a New Car")

        # Car brand → model mapping
        car_models = {
            "Toyota": ["Corolla", "Camry", "Yaris"],
            "Hyundai": ["Elantra", "Tucson", "Sonata"],
            "Kia": ["Picanto", "Sportage", "Cerato"],
            "BMW": ["X1", "X3", "X5"],
            "Mercedes": ["C180", "E300", "GLA"]
        }

        make = st.selectbox("Brand", list(car_models.keys()))
        model = st.selectbox("Model", car_models[make])
        year = st.selectbox("Choose a year", list(range(1990, 2026)), index=20)
        vin = st.text_input("VIN")
        mileage = st.number_input("Mileage", 0)
        color = st.text_input("Color")
        price = st.number_input("Price", 0.0)
        cost = st.number_input("Cost", 0.0)
        status = st.selectbox("Status", ["Available", "Sold", "Reserved"])

        # Load Branch names
        branches = pd.read_sql("SELECT BranchID, City FROM Branch", get_connection())
        branch_map = dict(zip(branches["City"], branches["BranchID"]))
        branch_name = st.selectbox("Branch", list(branch_map.keys()))
        branch_id = branch_map[branch_name]

        # Load Supplier names
        suppliers = pd.read_sql("SELECT SupplierID, Name FROM Supplier", get_connection())
        supplier_map = dict(zip(suppliers["Name"], suppliers["SupplierID"]))
        supplier_name = st.selectbox("Supplier", list(supplier_map.keys()))
        supplier_id = supplier_map[supplier_name]

        if st.button("Insert Car"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("""INSERT INTO Car VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (vin, make, model, year, mileage, color, price, cost, status, branch_id, supplier_id))
                conn.commit()
                st.success("Car added successfully.")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                conn.close()

    def view_records(self):
        st.subheader("View All Cars")
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Car", conn)
        st.dataframe(df)
        conn.close()
    def update_record(self):
        st.subheader("Update Car Record")

        # Load Car data
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM Car", conn)
        df = df.reset_index().rename(columns={"index": "ID"})

        # Load Branch data
        branches = pd.read_sql("SELECT BranchID, City FROM Branch", get_connection())
        branch_map = dict(zip(branches["City"], branches["BranchID"]))

        # Load Supplier data
        suppliers = pd.read_sql("SELECT SupplierID, Name FROM Supplier", get_connection())
        supplier_map = dict(zip(suppliers["Name"], suppliers["SupplierID"]))

        # Search bar by Car ID
        search_id = st.text_input("Search by Car ID (row index)")
        if search_id.isdigit():
            row_id = int(search_id)
            filtered_df = df[df["ID"] == row_id]
        else:
            filtered_df = df

        st.markdown("Click a row below to select a car to update:")

        selected_rows = st.data_editor(
            filtered_df,
            use_container_width=True,
            disabled=True,
            num_rows="dynamic",
            key="car_update_editor"
        )

        if isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty:
            selected_car = selected_rows.iloc[0]

            st.markdown("Edit Car Details")

            car_models = {
                "Toyota": ["Corolla", "Camry", "Yaris"],
                "Hyundai": ["Elantra", "Tucson", "Sonata"],
                "Kia": ["Picanto", "Sportage", "Cerato"],
                "BMW": ["X1", "X3", "X5"],
                "Mercedes": ["C180", "E300", "GLA"]
            }

            st.text_input("VIN (Primary Key)", selected_car["VIN"], disabled=True)
            make = st.selectbox("Brand", list(car_models.keys()), index=list(car_models.keys()).index(selected_car["Make"]))
            model = st.selectbox("Model", car_models[make], index=car_models[make].index(selected_car["Model"]) if selected_car["Model"] in car_models[make] else 0)
            year = st.selectbox("Choose a year", list(range(1990, 2026)), index=list(range(1990, 2026)).index(int(selected_car["Year"])))
            mileage = st.number_input("Mileage", value=int(selected_car["Mileage"]))
            color = st.text_input("Color", selected_car["Color"])
            price = st.number_input("Price", value=float(selected_car["Price"]))
            cost = st.number_input("Cost", value=float(selected_car["Cost"]))
            status = st.selectbox("Status", ["Available", "Sold", "Reserved"], index=["Available", "Sold", "Reserved"].index(selected_car["Status"]))

            branch_name = st.selectbox("Branch", list(branch_map.keys()), index=list(branch_map.values()).index(int(selected_car["BranchID"])))
            branch_id = branch_map[branch_name]

            supplier_name = st.selectbox("Supplier", list(supplier_map.keys()), index=list(supplier_map.values()).index(int(selected_car["SupplierID"])))
            supplier_id = supplier_map[supplier_name]

            if st.button("Update Record"):
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        UPDATE Car SET Make=%s, Model=%s, Year=%s, Mileage=%s, Color=%s,
                        Price=%s, Cost=%s, Status=%s, BranchID=%s, SupplierID=%s
                        WHERE VIN=%s
                    """, (make, model, year, mileage, color, price, cost, status, branch_id, supplier_id, selected_car["VIN"]))
                    conn.commit()
                    st.success(f"Updated car with VIN {selected_car['VIN']}")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
        else:
            st.info("No car selected.")
            conn.close()


    def delete_record(self):
        st.subheader("Delete Car")
        vin = st.text_input("VIN to Delete")
        if st.button("Delete Car"):
            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Car WHERE VIN = %s", (vin,))
                conn.commit()
                st.success(f"🗑️ Deleted car with VIN {vin}.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                conn.close()
