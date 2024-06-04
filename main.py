import streamlit as st

# Initial list of appliances and their power ratings (in watts)
appliance_power = {
    "Oven": 2000,
    "Microwave": 1000,
    "Grill": 1500,
    "Stove": 1200,
    "Blender": 300,
    "Heater": 1500
}

PV_power = {
    "100W": 100,
    "200W": 200,
    "300W": 300,
    "400W": 400,
    "500W": 500
}
total_power = 0
# st.session_state.installed_appliances = [] 
# st.session_state.PV_power = 0
# st.session_state.solar_panel_quantity = 0
# st.session_state.selected_PV_power = 0
# st.session_state.selected_appliance = 0
# st.session_state.new_appliance_name = 0
# st.session_state.power_rating = 0
# Function to calculate total power and battery requirement

def calculate_total_power(installed_appliances):
    total_power = sum(power for appliance, power in installed_appliances)
    return total_power

# Title of the Streamlit app
st.title("Food Truck Appliance Power Calculator")

st.subheader("Appliance Setup")
# Dropdown to select appliances
selected_appliance = st.selectbox(
    "Select an appliance",
    list(appliance_power.keys()) + ["Other"]
)

# If 'Other' is selected, ask the user to name the appliance
if selected_appliance == "Other":
    new_appliance_name = st.text_input("Enter the name of the new appliance")

# Text box to show and modify power rating of the selected appliance
if selected_appliance:
    if selected_appliance == "Other":
        selected_appliance = new_appliance_name
        appliance_power[selected_appliance] = 0

    power_rating = st.number_input(
        "Power rating (in watts)",
        value=appliance_power[selected_appliance]
    )

# Initialize the list of installed appliances in session state if it doesn't exist
if 'installed_appliances' not in st.session_state:
    st.session_state.installed_appliances = []

installed_appliances = st.session_state.installed_appliances

# Button to add the appliance to the list of installed appliances
if st.button("Add Appliance"):
    if selected_appliance and power_rating:
        calculate_total_power(installed_appliances)
        installed_appliances.append((selected_appliance, power_rating))
        

# Display the list of installed appliances
st.write("**List of Installed Appliances**")

st.write(total_power)
for appliance, power in installed_appliances:
    st.write(f"{appliance}: {power}W")


st.subheader("Solar Panel Setup")
solar_panel_quantity = st.number_input(
    "Select number of solar panels:",
    min_value=0,
    max_value=3,
    step=1
)

selected_PV_power = st.selectbox(
    "Select the desired power rating of each solar panel:",
    list(PV_power.keys())
)
generated_power = solar_panel_quantity*PV_power[selected_PV_power]
st.subheader("Battery Requirements")
run_time = st.number_input(
    "Enter the desired run time (in hours):",
    min_value=0,
    max_value=24,
    step=1
)

# st.write(f"**Total power generated**: {generated_power}W")
# # st.write(f"**Total power required**: {total_power}W")
# # required_power = total_power
# battery_capacity = required_power * run_time / 1000  # Assuming battery capacity in kWh
# recc_battery_capacity = round(battery_capacity/0.7, 1)
# if battery_capacity < 0:
#     st.write(f"**Required Battery Capacity**: 0kWh")
#     st.write(f"**Recommended Battery Capacity**: 0kWh")
# else:
#     st.write(f"**Required Battery Capacity**: {battery_capacity}kWh")
#     st.write(f"**Recommended Battery Capacity**: {recc_battery_capacity}kWh")

# # Button to reset the list of installed appliances
# if st.button("Reset"):
#     st.session_state.installed_appliances = [] 
#     st.session_state.PV_power = 0
#     st.session_state.solar_panel_quantity = 0
#     st.session_state.selected_PV_power = 0
#     st.session_state.selected_appliance = 0
#     st.session_state.new_appliance_name = 0
#     st.session_state.power_rating = 0
