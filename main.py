import streamlit as st
import pandas as pd

# Initial list of appliances and their power ratings (in watts)
appliance_power = {
    "Oven": 2000,
    "Microwave": 1000,
    "Grill": 1500,
    "Stove": 1200,
    "Blender": 300,
    "Heater": 1500
}

# Power ratings of solar panels in watts
PV_power = {
    "100W": 100,
    "200W": 200,
    "300W": 300,
    "400W": 400,
    "500W": 500
}

# Average costs of solar panels in USD
PV_cost = {
    "100W": 115,
    "200W": 225,
    "300W": 325,
    "400W": 450,
    "500W": 600
}

# Conversion rate from USD to EUR (example rate)
USD_TO_EUR = 0.92

def calculate_total_power(installed_appliances):
    """
    Calculate the total power requirement of the installed appliances.
    """
    total_power = sum(power for appliance, power in installed_appliances)
    return total_power

# Title of the Streamlit app
st.title("Food Truck Appliance Power Calculator")

# Appliance setup section
st.subheader("Appliance Setup")

# Create two columns for appliance selection and power rating
col1, col2 = st.columns(2)

with col1:
    # Dropdown to select appliances
    selected_appliance = st.selectbox(
        "Select an appliance",
        list(appliance_power.keys()) + ["Other"]
    )

    # If 'Other' is selected, ask the user to name the appliance
    if selected_appliance == "Other":
        new_appliance_name = st.text_input("Enter the name of the new appliance")

with col2:
    # Text box to show and modify power rating of the selected appliance
    if selected_appliance:

        # Set up conditional value assignment
        if selected_appliance == "Other":
            default_power_rating = 0
        else:
            default_power_rating = appliance_power[selected_appliance]

        # Use conditional value assignment inside st.number_input()
        power_rating = st.number_input(
            label="Power rating (in watts)" if selected_appliance != "Other" else "Enter power rating:",
            value=default_power_rating
        )

# Initialize the list of installed appliances in session state if it doesn't exist
if 'installed_appliances' not in st.session_state:
    st.session_state.installed_appliances = []

installed_appliances = st.session_state.installed_appliances

# Button to add the appliance to the list of installed appliances
if st.button("Add Appliance"):
    if selected_appliance == "Other" and new_appliance_name and power_rating:
        # Update appliance_power dictionary with the new appliance and its power rating
        appliance_power[new_appliance_name] = power_rating
        installed_appliances.append((new_appliance_name, power_rating))
        st.session_state.installed_appliances = installed_appliances
        st.session_state.appliance_power = appliance_power
    elif selected_appliance and power_rating:
        installed_appliances.append((selected_appliance, power_rating))
        st.session_state.installed_appliances = installed_appliances

# Display the list of installed appliances in a list format
st.write("**List of Installed Appliances**")
for appliance, power_rating in installed_appliances:
    st.write(f"{appliance}: {power_rating}W")

total_power = calculate_total_power(installed_appliances)
st.write(f"**Total Power Requirement**: {total_power}W")

st.markdown('<hr>', unsafe_allow_html=True)
# Create two columns for solar panel setup and battery requirements
col3, col4 = st.columns(2)

with col3:
    st.subheader("Solar Panel Setup")

    # Select number of solar panels
    solar_panel_quantity = st.number_input(
        "Select number of solar panels:",
        min_value=0,
        max_value=3,
        step=1
    )

    # Select the desired power rating of each solar panel
    selected_PV_power = st.selectbox(
        "Select the desired power rating of each solar panel:",
        list(PV_power.keys())
    )

    generated_power = solar_panel_quantity * PV_power[selected_PV_power]
    total_cost_usd = solar_panel_quantity * PV_cost[selected_PV_power]
    total_cost_eur = total_cost_usd * USD_TO_EUR

    st.write(f"**Total Power Generated**: {generated_power}W")
    st.write(f"**Estimated Cost of Solar Panels**: ${total_cost_usd:.2f} / €{total_cost_eur:.2f}")

with col4:
    st.subheader("Battery Requirements")

    # Enter the desired run time
    run_time = st.number_input(
        "Enter the desired run time (in hours per day):",
        min_value=0,
        max_value=24,
        step=1,
        value=12
    )

    # Calculate the total required power for the desired run time
    total_required_power_per_day = total_power * run_time

    # Calculate the net power requirement after accounting for generated solar power
    net_power_requirement_per_day = total_required_power_per_day - generated_power
    if net_power_requirement_per_day < 0:
        net_power_requirement_per_day = 0  # If generated power exceeds required power, set net requirement to 0

    # Calculate battery capacity required in kWh
    battery_capacity = net_power_requirement_per_day / 1000  # Converting power to kWh
    recommended_battery_capacity = round(battery_capacity / 0.7, 1)  # Considering 70% efficiency

    # Cost per kWh of Li-ion battery in USD
    battery_cost_per_kwh_usd = 150
    recommended_battery_cost_usd = recommended_battery_capacity * battery_cost_per_kwh_usd
    recommended_battery_cost_eur = recommended_battery_cost_usd * USD_TO_EUR

    # # Enter the cost of electricity
    # electricity_cost_usd = st.number_input(
    #     "Enter the cost of electricity per kWh (in USD):",
    #     value=0.2,
    #     step=0.01
    # )
    # electricity_cost_eur = electricity_cost_usd * USD_TO_EUR

    # Calculate the cost of charging the battery
    # battery_charging_cost_usd = net_power_requirement_per_day * electricity_cost_usd
    # battery_charging_cost_eur = battery_charging_cost_usd * USD_TO_EUR

    if battery_capacity <= 0:
        # st.write(f"**Required Battery Capacity**: 0 kWh")
        st.write(f"**Recommended Battery Capacity**: 0 kWh")
        st.write(f"**Estimated Battery Cost**: $0 / €0")
        # st.write(f"**Battery Charging Cost**: $0 / €0")
    else:
        # st.write(f"**Required Battery Capacity**: {battery_capacity:.1f} kWh")
        st.write(f"**Required Battery Capacity**: {recommended_battery_capacity:.1f} kWh")
        st.write(f"**Estimated Battery Cost**: ${recommended_battery_cost_usd:.2f} / €{recommended_battery_cost_eur:.2f}")
        # st.write(f"**Battery Charging Cost**: ${battery_charging_cost_usd:.2f} / €{battery_charging_cost_eur:.2f}")

st.markdown('<hr>', unsafe_allow_html=True)

# # Fuel cost estimation section
# st.subheader("Fuel Cost Estimation")

# # Enter the cost of fuel per kWh
# fuel_cost_per_kwh_usd = st.number_input(
#     "Enter the cost of fuel per kWh (in USD):",
#     value=0.13,
#     step=0.01
# )
# fuel_cost_per_kwh_eur = fuel_cost_per_kwh_usd * USD_TO_EUR

# # Calculate the daily fuel cost
# daily_power_consumption_kwh = net_power_requirement_per_day / 1000  # Converting power to kWh
# daily_fuel_cost_usd = daily_power_consumption_kwh * fuel_cost_per_kwh_usd
# daily_fuel_cost_eur = daily_fuel_cost_usd * USD_TO_EUR

# # Calculate the annual fuel cost
# annual_fuel_cost_usd = daily_fuel_cost_usd * 365
# annual_fuel_cost_eur = annual_fuel_cost_usd * USD_TO_EUR

# st.write(f"**Daily Fuel Cost**: ${daily_fuel_cost_usd:.2f} / €{daily_fuel_cost_eur:.2f}")
# st.write(f"**Annual Fuel Cost**: ${annual_fuel_cost_usd:.2f} / €{annual_fuel_cost_eur:.2f}")

# st.markdown('<hr>', unsafe_allow_html=True)

# # Calculate break-even time
# total_initial_cost_usd = total_cost_usd + recommended_battery_cost_usd
# if annual_fuel_cost_usd > 0:
#     break_even_time_years = total_initial_cost_usd / annual_fuel_cost_usd
# else:
#     break_even_time_years = float('inf')  # If there's no annual fuel cost, break-even time is infinite

# st.write(f"**Total Initial Cost (Solar Panels + Battery)**: ${total_initial_cost_usd:.2f} / €{total_initial_cost_usd * USD_TO_EUR:.2f}")
# st.write(f"**Break-even Time**: {break_even_time_years:.2f} years")
