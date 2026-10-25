import math
import time
import streamlit as st

# --- WEBSITE MASTER CONFIGURATION ---
st.set_page_config(page_title="Physics Sandbox Laboratory", layout="wide")

# Navigation Sidebar to pick between different modules
st.sidebar.title("🔬 Physics Lab Menu")
module = st.sidebar.selectbox("Choose a Physics Topic:", ["Planetary Orbit Sandbox", "Projectile Motion Simulator", "GCSE Bitesize Hub 🇬🇧"])


# ==========================================
# MODULE 1: PLANETARY ORBIT GRAVITY SANDBOX
# ==========================================
if module == "Planetary Orbit Sandbox":
    st.title("🪐 Planetary Orbit Gravity Sandbox")
    st.write("Simulate orbital trajectories around a massive central star using Newtonian classical gravity mechanics.")

    # --- SIMULATION PARAMETERS PANEL ---
    st.sidebar.header("🛠️ Universe Controls")
    
    star_mass = st.sidebar.slider("Star Mass (scaled x10^13 kg)", min_value=1.0, max_value=50.0, value=20.0, step=1.0)
    init_dist = st.sidebar.slider("Initial Distance from Star (AU-scaled)", min_value=20.0, max_value=150.0, value=100.0, step=5.0)
    init_speed = st.sidebar.slider("Initial Tangential Speed", min_value=0.0, max_value=15.0, value=8.5, step=0.5)
    
    st.sidebar.markdown("---")
    sim_steps = st.sidebar.slider("Simulation Length (Frames)", min_value=200, max_value=2000, value=800, step=100)
    run_orbit = st.sidebar.button("🚀 Launch Planet Into Orbit")

    G = 1.0 
    x, y = init_dist, 0.0
    vx, vy = 0.0, init_speed
    dt = 0.1 
    
    x_history = [x]
    y_history = [y]
    distances = [init_dist]
    speeds = [init_speed]

    for _ in range(sim_steps):
        r = math.sqrt(x**2 + y**2)
        if r < 5.0: 
            break
            
        distances.append(r)
        accel_total = (G * star_mass) / (r**2)
        ax = -accel_total * (x / r)
        ay = -accel_total * (y / r)
        
        vx += ax * dt
        vy += ay * dt

        x += vx * dt
        y += vy * dt
        
        x_history.append(x)
        y_history.append(y)
        speeds.append(math.sqrt(vx**2 + vy**2))

    col1, col2 = st.columns([2, 1]) 

    with col1:
        st.subheader("🌌 System Orbit Tracking View")
        orbit_placeholder = st.empty()
        
        # --- SIMPLE EXPLANATION UNDER THE GRAVITY GRAPH ---
        st.markdown("""
        ---
        ### 💡 How to Read This Planetary Graph
        * **The Center Context:** The very middle of the graph cross-grid where the lines meet `(0,0)` is where your massive **Star** sits. 
        * **The Moving Line:** This path tracks your planet's actual flight history across space.
        
        ### 🧐 What to look for as you move the sliders:
        1. **Perfect Circles (Balancing Act):** If you give a planet the *exact right speed*, it forms a perfect circle. Gravity pulls it in at the exact same rate that its forward speed tries to carry it away!
        2. **Egg-Shaped Ovals (Ellipses):** If you start a planet too far away or too fast, it will drop into a lopsided oval orbit. Notice how it **slingshots rapidly** whenever it skims past the central star, and then **moves like turtle molasses** when it drifts out far away. That's real orbital mechanics in action!
        3. **Crash or Escape:** If your speed slider is too low, the planet spiraling downward will hit the center star. If the speed is way too high, it breaks free from the star's gravity entirely and flies off the edge of the graph layout forever!
        """)

    with col2:
        st.subheader("📉 Real-Time Telemetry Metrics")
        dist_metric = st.empty()
        speed_metric = st.empty()
        status_metric = st.empty()

    step_skip = max(1, len(x_history) // 50)
    for i in range(1, len(x_history), step_skip):
        current_data = {
            "X Position": x_history[:i] + [0.0],
            "Y Position": y_history[:i] + [0.0]
        }
        orbit_placeholder.line_chart(data=current_data, x="X Position", y="Y Position", height=500)
        
        current_r = distances[min(i, len(distances)-1)]
        current_v = speeds[min(i, len(speeds)-1)]
        
        dist_metric.metric("Current Distance from Star", f"{current_r:.2f} AU")
        speed_metric.metric("Current Speed", f"{current_v:.2f} units/s")
        
        if max(distances) - min(distances) < 2.0:
            status_metric.info("Stable Circular Alignment")
        elif current_v > init_speed * 1.3:
            status_metric.warning("High Speed Slingshot!")
        else:
            status_metric.success("Stable Oval Loop")
            
        time.sleep(0.01)

    final_data = {"X Position": x_history + [0.0], "Y Position": y_history + [0.0]}
    orbit_placeholder.line_chart(data=final_data, x="X Position", y="Y Position", height=500)


# ==========================================
# MODULE 2: PROJECTILE MOTION SIMULATOR
# ==========================================
elif module == "Projectile Motion Simulator":
    st.title("🏹 Interactive Projectile Motion Simulator")
    st.write("Adjust parameters in the sidebar and watch the motion physics simulate in real time.")

    st.sidebar.header("🛠️ Simulation Parameters")

    velocity = st.sidebar.slider("Initial Velocity (m/s)", min_value=5.0, max_value=100.0, value=30.0, step=1.0)
    angle_degrees = st.sidebar.slider("Launch Angle (degrees)", min_value=0, max_value=90, value=45, step=1)
    mass = st.sidebar.slider("Object Mass (kg)", min_value=0.1, max_value=10.0, value=0.5, step=0.1)
    enable_drag = st.sidebar.toggle("Enable Air Resistance", value=True)
    replay_btn = st.sidebar.button("🔄 Re-run Animation")

    class Projectile:
        def __init__(self, x, y, velocity, angle_degrees, mass, enable_drag):
            self.x = x  
            self.y = y  
            self.mass = mass  
            
            angle_rad = math.radians(angle_degrees)
            self.vx = velocity * math.cos(angle_rad)
            self.vy = velocity * math.sin(angle_rad)
            
            self.g = 9.81         
            self.drag_coef = 0.47 if enable_drag else 0.0

        def update_physics(self, dt):
            speed = math.sqrt(self.vx**2 + self.vy**2)
            f_drag = 0.5 * self.drag_coef * (speed**2)
            
            if speed > 0:
                f_drag_x = -f_drag * (self.vx / speed)
                f_drag_y = -f_drag * (self.vy / speed)
            else:
                f_drag_x, f_drag_y = 0, 0
                
            ax = f_drag_x / self.mass
            ay = -self.g + (f_drag_y / self.mass) 
            
            self.vx += ax * dt
            self.vy += ay * dt
            
            self.x += self.vx * dt
            self.y += self.vy * dt

    ball = Projectile(x=0, y=0, velocity=velocity, angle_degrees=angle_degrees, mass=mass, enable_drag=enable_drag)
    dt = 0.01  

    all_x = [0.0]
    all_y = [0.0]
    time_elapsed = 0.0

    while ball.y >= 0 and len(all_x) < 5000: 
        ball.update_physics(dt)
        time_elapsed += dt
        all_x.append(ball.x)
        all_y.append(ball.y)

    col1, col2 = st.columns([2, 1]) 

    with col1:
        st.subheader("📊 Trajectory Path")
        chart_placeholder = st.empty()
        
        # --- SIMPLE EXPLANATION UNDER THE PROJECTILE GRAPH ---
        st.markdown("""
        ---
        ### 💡 How to Read This Projectile Graph
        * **The Bottom Line (X-Axis):** Tells you exactly how far forward across the ground the ball flew in meters.
        * **The Side Line (Y-Axis):** Tells you how high into the air the ball reached at that point.
        
        ### 🧐 What to look for as you move the sliders:
        1. **The Magic 45-Degree Angle:** Set air resistance to *Off* and look at what happens at a 45-degree angle. That angle gets you the absolute furthest total distance! Launching higher makes it go tall but drop early; launching flatter makes it crash down instantly.
        2. **Air Resistance Effect:** Turn air resistance *On* and launch a light object (like `0.1 kg`). Notice how the arc curve loses its perfect symmetrical rainbow shape! It climbs up normally but gets squished and drops almost straight down at the end because air friction is actively slowing it down.
        """)

    with col2:
        st.subheader("📋 Final Metrics")
        st.metric(label="Total Distance Traveled", value=f"{all_x[-1]:.2f} meters")
        st.metric(label="Total Flight Time", value=f"{time_elapsed:.2f} seconds")
        st.metric(label="Peak Height Reached", value=f"{max(all_y):.2f} meters")

    animation_speed_factor = max(1, len(all_x) // 40) 

    for i in range(1, len(all_x), animation_speed_factor):
        current_chart_data = {
            "Horizontal Distance (m)": all_x[:i],
            "Vertical Height (m)": all_y[:i]
        }
        chart_placeholder.line_chart(data=current_chart_data, x="Horizontal Distance (m)", y="Vertical Height (m)")
        time.sleep(0.01) 

    final_chart_data = {"Horizontal Distance (m)": all_x, "Vertical Height (m)": all_y}
    chart_placeholder.line_chart(data=final_chart_data, x="Horizontal Distance (m)", y="Vertical Height (m)")
# ==========================================
# MODULE 3: GCSE BITESIZE HUB
# ==========================================
elif module == "GCSE Bitesize Hub 🇬🇧":
    st.title("⚡ GCSE Interactive Physics Hub")
    st.write("Master core concepts, tricky exam formulas, and quick-fire memory tricks without the boring textbook walls.")

    # Tab partitions to divide information cleanly
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📐 Magic Formula Triangles", 
        "🧠 Exam Memory Hacks", 
        "🎯 Quick Knowledge Check",
        "📝 Practice Your Equations", 
        "📖 Simple Terms Glossary",
        "🥽 Required Practicals Lab"
    ])



    with tab1:
        st.subheader("How to Use Formula Triangles")
        st.write("Cover the letter you want to find with your hand! If the remaining letters are side-by-side, **multiply** them. If one is over the other, **divide**.")
        
        # Dropdown selection for formulas
        formula_choice = st.selectbox("Pick a Required GCSE Equation to Test:", [
            "Weight = Mass × Gravity (W = m g)",
            "Speed = Distance ÷ Time (s = d/t)",
            "Density = Mass ÷ Volume (ρ = m/V)"
        ])
        
        st.markdown("---")
        if "Weight" in formula_choice:
            st.code("      [ W ]      \n     -------     \n    [m] * [g]    ", language="text")
            m_input = st.number_input("Enter Mass (kg):", value=10.0)
            g_input = st.number_input("Enter Gravity (Earth is approx 9.81 m/s²):", value=9.81)
            st.success(f"**Calculated Weight (W):** {m_input * g_input:.2f} Newtons (N)")
            
        elif "Speed" in formula_choice:
            st.code("      [ d ]      \n     -------     \n    [s] * [t]    ", language="text")
            d_input = st.number_input("Enter Distance (meters):", value=100.0)
            t_input = st.number_input("Enter Time (seconds):", value=12.5)
            st.success(f"**Calculated Speed (s):** {d_input / t_input:.2f} m/s")
            
        elif "Density" in formula_choice:
            st.code("      [ m ]      \n     -------     \n    [ρ] * [V]    ", language="text")
            mass_in = st.number_input("Enter Mass (kg):", value=50.0)
            vol_in = st.number_input("Enter Volume (m³):", value=5.0)
            st.success(f"**Calculated Density (ρ):** {mass_in / vol_in:.2f} kg/m³")

    with tab2:
        st.subheader("💡 Simple Revision Cheat-Sheets")
        
        with st.expander("🌈 The Electromagnetic Spectrum (Shortest to Longest Wave)"):
            st.markdown("""
            **Memory Phrase:** *Roman Men Invented Very Unusual X-Ray Guns*
            * **R**adio | **M**icrowave | **I**nfrared | **V**isible | **U**ltraviolet | **X**-ray | **G**amma
            """)
            
        with st.expander("⚡ Renewable vs Non-Renewable Energy Storage"):
            col_ren, col_non = st.columns(2)
            with col_ren:
                st.info("**Renewable (Won't run out)**\n* Solar\n* Wind\n* Hydroelectric\n* Tidal")
            with col_non:
                st.error("**Non-Renewable (Finite supply)**\n* Coal\n* Oil\n* Gas\n* Nuclear Uranium")

    with tab3:
        st.subheader("🧠 Quick Fire GCSE Quiz")
        st.write("Test your memory below before you walk into the exam room. Answer the questions to check your knowledge!")

        # --- QUESTION 1 ---
        st.markdown("### **Question 1: Electrical Circuits**")
        q1_choice = st.radio(
            "When measuring the electric current flowing through a specific component in a circuit, how should the ammeter be connected?",
            ["In parallel across the component", "Wrapped around the outside of the wire externally", "In series with the component", "Directly across the battery terminals only"],
            index=None, # Starts with no option selected
            key="q1"
        )
        
        if q1_choice:
            if q1_choice == "In series with the component":
                st.success("✅ **Correct!** An ammeter must always be placed in series so that all the electric current flows directly through the meter.")
            else:
                st.error("❌ **Not quite!**")
                st.info("💡 **Hint:** Think about how current is the rate of flow of charge. The charge has to physically pass *through* the meter to be counted. (Voltmeters go in parallel, ammeters go in series!)")

        st.markdown("---")

        # --- QUESTION 2 ---
        st.markdown("### **Question 2: Kinetic Energy**")
        q2_choice = st.radio(
            "If you double the speed (velocity) of a moving bicycle, what happens to its kinetic energy?",
            ["It doubles to twice its original value", "It stays exactly the same", "It increases by a factor of eight", "It quadruples to four times its original value"],
            index=None,
            key="q2"
        )
        
        if q2_choice:
            if q2_choice == "It quadruples to four times its original value":
                st.success("✅ **Correct!** Because velocity is squared in the kinetic energy formula ($E_k = \\frac{1}{2}mv^2$), doubling the speed has a massive impact. Doubling the speed ($2^2$) makes the energy **4 times** larger!")
            else:
                st.error("❌ **Not quite!**")
                st.info("💡 **Hint:** Look closely at the kinetic energy formula: $E_k = \\frac{1}{2}mv^2$. Notice that the velocity ($v$) is **squared**. What is 2 squared ($2^2$)?")

        st.markdown("---")

        # --- QUESTION 3 ---
        st.markdown("### **Question 3: SI Units**")
        q3_choice = st.radio(
            "Which of the following is the correct SI unit for electrical resistance?",
            ["Ampere", "Ohm", "Volt", "Watt"],
            index=None,
            key="q3"
        )
        
        if q3_choice:
            if q3_choice == "Ohm":
                st.success("✅ **Correct!** The ohm ($\Omega$) is the unit of electrical resistance, named after Georg Ohm.")
            else:
                st.error("❌ **Not quite!**")
                st.info("💡 **Hint:** Remember Ohm's Law ($V = IR$). Amperes measure current, Volts measure potential difference, and Watts measure power.")

    # --- NEW ADDITION: TAB 4 (EQUATION PRACTICE WORKBENCH) ---
    with tab4:
        st.subheader("📝 Physics Equation Practice Workbench")
        st.write("Exams don't just ask you to memorize formulas—they make you rearrange them! Pick a scenario below to practice.")
        
        # Real-world exam style word problems
        scenario = st.selectbox("Select a Practice Scenario:", [
            "Scenario A: The Acceleration of a Sports Car",
            "Scenario B: The Weight of an Astronaut on Mars"
        ])
        
        st.markdown("---")
        
        if "Sports Car" in scenario:
            st.markdown("💬 **The Problem:** A Tesla accelerates from rest to a final velocity of **30 m/s** over a period of **6 seconds**. Calculate the car's average acceleration.")
            st.info("💡 **Formula Reminder:** $\\text{Acceleration} = \\frac{\\text{Change in Velocity}}{\\text{Time taken}}$ ($a = \\frac{\\Delta v}{t}$)")
            
            # Interactive student working inputs
            user_calc_a = st.number_input("Type your calculated answer here (m/s²):", value=0.0, step=0.5, key="car_calc")
            
            if user_calc_a > 0:
                if math.isclose(user_calc_a, 5.0):
                    st.success("🎉 **Spot on!** 30 ÷ 6 = **5 m/s²**. Excellent working.")
                else:
                    st.error("❌ Not quite. Divide the total speed change (30) by the time taken (6). Try modifying your answer input above!")
                    
        elif "Astronaut" in scenario:
            st.markdown("💬 **The Problem:** An astronaut has a mass of **80 kg**. On the surface of Mars, the local gravitational field strength ($g$) is only **3.7 m/s²**. What is the astronaut's total weight on Mars?")
            st.info("💡 **Formula Reminder:** $\\text{Weight} = \\text{Mass} \\times \\text{Gravity}$ ($W = m g$)")
            
            user_calc_w = st.number_input("Type your calculated answer here (Newtons):", value=0.0, step=10.0, key="mars_calc")
            
            if user_calc_w > 0:
                if math.isclose(user_calc_w, 296.0):
                    st.success("🎉 **Brilliant!** 80 kg × 3.7 m/s² = **296 Newtons**. Notice how much lighter they are than on Earth!")
                else:
                    st.error("❌ Not quite. Multiply the mass (80) by the Mars gravity (3.7). Check your math and adjust the slider input value!")


    # --- NEW ADDITION: TAB 5 (THE GLOSSARY & TRICKY WORDS FINDER) ---
    with tab5:
        st.subheader("📖 Simple Terms & Tricky Words Dictionary")
        st.write("Physics is filled with words that sound complicated but mean simple things. Type or click a term below to decode it into plain English.")
        
        # Interactive searchable glossary dictionary
        glossary = {
            "Scalar Quantity": "A measurement that only has a size (magnitude), but NO specific direction. Examples: Speed, distance, mass, or time.",
            "Vector Quantity": "A measurement that has BOTH a size AND a clear physical direction. Examples: Velocity (speed in a direction), weight (pulling down), or force.",
            "Inertia": "How stubborn an object is! It is the tendency of an object to resist any change to its current movement state.",
            "Potential Difference": "The technical name for Voltage. It is the measure of how much electrical energy push is given to electrons traveling around a circuit path.",
            "Work Done": "Simply a fancy physics term for 'Energy Transferred'. Whenever a force moves an object across a physical distance, work is done."
        }
        
        # Let users select a word instantly from a dropdown list to view definition
        selected_word = st.selectbox("Search or Select a Tricky Word:", list(glossary.keys()))
        
        # Display the explanation in an easy-to-read callout box card
        st.markdown(f"""
        ### 🔍 Definition for **{selected_word}**
        > {glossary[selected_word]}
        """)
        
        # Fast Unit Converter widget right underneath
        st.markdown("---")
        st.subheader("⚖️ Quick Unit Converter")
        st.write("Exam questions love to trick students by giving values in kilometers or grams instead of standard units. Convert them instantly here:")
        
        convert_type = st.radio("What unit do you want to fix?", ["Kilometers (km) ➔ Meters (m)", "Grams (g) ➔ Kilograms (kg)"], horizontal=True)
        
        if "Kilometers" in convert_type:
            km_val = st.number_input("Enter value in km:", value=1.5, step=0.1)
            st.info(f"👉 **Standard Form:** {km_val} km is equal to **{km_val * 1000:,.0f} meters** (Ready to use in formulas!)")
        else:
            g_val = st.number_input("Enter value in grams (g):", value=500.0, step=50.0)
            st.info(f"👉 **Standard Form:** {g_val} g is equal to **{g_val / 1000:.3f} kg** (Ready to use in formulas!)")
    # --- NEW ADDITION: TAB 6 (REQUIRED PRACTICALS LAB) ---
    with tab6:
        st.subheader("🥽 GCSE Physics Required Practicals Workbench")
        st.write("Simulate mandatory lab experiments, collect mock trial data, and study exam-style trends instantly.")
        
        practical_choice = st.selectbox("Select a Required Practical:", [
            "RP 3: Resistance of a Wire (Length vs Resistance)",
            "RP 4: I–V Characteristics (Current vs Potential Difference)"
        ])
        
        st.markdown("---")
        
        if "RP 3" in practical_choice:
            st.markdown("### 📏 Investigating How Wire Length Changes Resistance")
            st.write("Move the virtual crocodile clip along the meter ruler wire to change its length and record voltage ($V$) and current ($I$).")
            
            # Interactive Slider simulating the crocodile clip placement
            wire_length = st.slider("Select Wire Length (cm):", min_value=10, max_value=100, value=50, step=10)
            
            # Underlying physics simulation values (Constant resistance per cm = 0.15 Ohms/cm)
            sim_resistance = (wire_length * 0.15)
            sim_voltage = 4.5 # Fixed power supply voltage
            sim_current = sim_voltage / sim_resistance if sim_resistance > 0 else 0
            
            # Display current live readings as if reading lab multimeters
            c1, c2, c3 = st.columns(3)
            c1.metric("📏 Set Length", f"{wire_length} cm")
            c2.metric("🔌 Voltmeter Reading", f"{sim_voltage:.2f} V")
            c3.metric("📉 Ammeter Reading", f"{sim_current:.2f} A")
            
            # Generate the full exam data set table so they can see the overall trend
            st.markdown("#### 📋 Full Results Data Table")
            rp3_data = []
            for length in range(10, 110, 10):
                r_calc = length * 0.15
                v_calc = 4.5
                i_calc = v_calc / r_calc
                rp3_data.append({
                    "Wire Length (cm)": length,
                    "Potential Difference (V)": round(v_calc, 2),
                    "Current (A)": round(i_calc, 2),
                    "Calculated Resistance (Ω)": round(r_calc, 2)
                })
            st.dataframe(rp3_data, use_container_width=True)
            
            # Graph Plotting the Exam Trend
            st.markdown("#### 📈 Trajectory Trend: Length vs Resistance")
            st.line_chart(data=rp3_data, x="Wire Length (cm)", y="Calculated Resistance (Ω)")
            
            st.info("💡 **Exam Takeaway:** The graph is a straight line passing through the origin $(0,0)$. This proves that **the resistance of a wire is directly proportional to its length**. Doubling the length doubles the number of metal ions electrons must collide with!")

        elif "RP 4" in practical_choice:
            st.markdown("### 💡 Investigating I–V Characteristics")
            st.write("Vary the variable resistor to adjust the potential difference across a component. Change components to view their classic curves.")
            
            component = st.radio("Choose a Circuit Component to Test:", ["Fixed Resistor (Ohmic)", "Filament Lamp", "Diode"], horizontal=True)
            
            # Simulate generating forward and reverse potential difference points (-5V to +5V)
            rp4_data = []
            voltage_steps = [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
            
            for v in voltage_steps:
                if component == "Fixed Resistor (Ohmic)":
                    # Constant linear resistance (Ohm's Law: I = V / R)
                    i = v / 2.0
                elif component == "Filament Lamp":
                    # Resistance increases with heat/voltage magnitude, curving the line
                    if v >= 0:
                        i = math.sqrt(v) * 0.8 if v > 0 else 0.0
                    else:
                        i = -math.sqrt(abs(v)) * 0.8
                elif component == "Diode":
                    # Conducts current in one forward direction only after ~0.7V threshold bias
                    if v > 0.7:
                        i = (v - 0.7) ** 2
                    else:
                        i = 0.0
                        
                rp4_data.append({
                    "Potential Difference (V)": v,
                    "Current (A)": round(i, 2)
                })
                
            # Render Table and Chart side-by-side
            col_left, col_right = st.columns([1, 2])
            with col_left:
                st.markdown("##### 📋 Telemetry Data")
                st.dataframe(rp4_data, use_container_width=True)
            with col_right:
                st.markdown("##### 📈 I–V Characteristic Curve Graph")
                st.line_chart(data=rp4_data, x="Potential Difference (V)", y="Current (A)")
                
            # Tailored exam explanations per selection
            if component == "Fixed Resistor (Ohmic)":
                st.success("📝 **Ohmic Behavior:** Current is directly proportional to potential difference. The constant gradient means resistance is completely steady.")
            elif component == "Filament Lamp":
                st.warning("📝 **Filament Lamp Curve:** As current increases, the metal filament heats up. The vibration of metal ions increases resistance, creating the distinct **S-shape curve**.")
            elif component == "Diode":
                st.error("📝 **Diode Curve:** Diodes only let current flow in **one direction** (forward bias). In reverse, resistance is infinitely high so current stays at zero.")
