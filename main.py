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
        st.subheader("🥽 Complete GCSE Physics Required Practicals Guide")
        st.write("Master all 10 mandatory practicals, view active experiment variables, and study model 6-mark exam answers.")
        
        rp_list = [
            "RP 1: Specific Heat Capacity",
            "RP 2: Thermal Insulators",
            "RP 3: Resistance of a Wire",
            "RP 4: I-V Characteristics",
            "RP 5: Determining Density",
            "RP 6: Extension of a Spring (Hooke's Law)",
            "RP 7: Acceleration (Newton's 2nd Law)",
            "RP 8: Ripple Tank & Waves in a Solid",
            "RP 9: Light Reflection & Refraction",
            "RP 10: Radiation & Absorption (Leslie Cube)"
        ]
        
        selected_rp = st.selectbox("Select a Required Practical to Master:", rp_list)
        st.markdown("---")
        
        if "RP 1" in selected_rp:
            st.markdown("### 🌡️ RP 1: Investigating Specific Heat Capacity")
            power = st.slider("Heater Power Rating (Watts):", 10, 100, 50, step=10)
            time_s = st.slider("Heating Duration (seconds):", 60, 600, 300, step=60)
            energy_j = power * time_s
            st.info(r"👉 **Calculated Work Done (Energy Transferred):** $E = P \times t = " + f"{power}" + r" \text{ W} \times " + f"{time_s}" + r" \text{ s} = " + f"{energy_j:,}" + r" \text{ Joules}$")

            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("""
                **🔬 Core Variables:**
                * **Independent:** Energy supplied / Time
                * **Dependent:** Temperature rise ($\Delta\theta$)
                * **Control:** Mass of block (1 kg), Insulation wrap
                """)
            with c2:
                st.markdown(f"""
                **📊 Mock Data Output:**
                * Block Mass: **1.0 kg**
                * Energy Supplied: **{energy_j:,} J**
                * Expected Temp Rise: **~{(energy_j / 4200):.1f}°C**
                """)
                
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe a method the student could use to determine the specific heat capacity of a metal block. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Preparation:** Measure and record the mass of the metal block using a top-pan balance.
                2. **Setup:** Wrap the block securely in an insulating layer (e.g., newspaper or foam) to reduce heat loss to the surroundings.
                3. **Assembly:** Place a thermometer and an immersion heater into the two holes in the block. Add a few drops of water to ensure good thermal contact.
                4. **Measurements:** Connect the heater to a power pack alongside a joulemeter. Record the initial temperature of the block.
                5. **Execution:** Turn on the power pack and heat the block for 10 minutes. Read the final temperature and the total energy input from the joulemeter.
                6. **Analysis:** Use the rearranged formula $c = \\frac{\\Delta E}{m \\times \\Delta\\theta}$ to calculate the specific heat capacity.
                """)

        elif "RP 2" in selected_rp:
            st.markdown("### ☕ RP 2: Investigating Thermal Insulators")
            insulator = st.radio("Choose Insulation Material:", ["None (Control)", "Bubble Wrap", "Cotton Wool", "Thick Cardboard"])
            rates = {"None (Control)": 4.5, "Bubble Wrap": 1.2, "Cotton Wool": 1.8, "Thick Cardboard": 2.5}
            st.error(f"📉 Simulated Temperature Drop Rate: **{rates[insulator]} °C per minute**")
            
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe how a student could compare the effectiveness of different materials as thermal insulators. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Setup:** Place a small beaker inside a larger beaker and fill the gap between them with the first insulating material (e.g., card, cotton wool).
                2. **Start conditions:** Boil water using a kettle and pour a fixed volume (e.g., $200\\text{ ml}$) into the inner beaker.
                3. **Covering:** Seal the beaker with a cardboard lid containing a hole for a thermometer to stop evaporation losses.
                4. **Timing:** Record the initial temperature of the water, start a stopwatch, and measure the temperature every 3 minutes for 15 minutes.
                5. **Comparison:** Repeat the exact experiment using the same volume of water and initial starting temperature, but changing the insulation material.
                6. **Conclusion:** Plot a cooling curve graph (Time vs Temp). The material with the lowest temperature drop (shallowest curve gradient) is the best thermal insulator.
                """)

        elif "RP 3" in selected_rp:
            st.markdown("### 📏 RP 3: Investigating the Resistance of a Wire")
            length = st.slider("Wire Length (cm):", 10, 100, 50, step=10)
            res = length * 0.12
            st.success(f"⚡ Calculated Wire Resistance: **{res:.2f} Ω**")
            
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe an experiment to investigate how the length of a wire affects its electrical resistance. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Circuit build:** Setup a basic series circuit containing a power pack, switch, ammeter, and a long test wire taped to a meter ruler.
                2. **Voltmeter:** Connect a voltmeter in parallel directly across the test wire using crocodile clips.
                3. **Initial setup:** Attach the first crocodile clip at the 0 cm mark and the second clip at the 10 cm mark.
                4. **Data extraction:** Close the switch, quickly record the readings on the ammeter and voltmeter, then immediately open the switch to stop the wire heating up.
                5. **Repetition:** Move the second crocodile clip out in 10 cm increments (20cm, 30cm, etc.), recording the current and voltage at each step.
                6. **Analysis:** Calculate resistance for each length using $R = \\frac{V}{I}$. Plot a graph of Length vs Resistance. It should show a straight line through the origin, proving they are directly proportional.
                """)

        elif "RP 4" in selected_rp:
            st.markdown("### 💡 RP 4: Investigating I-V Characteristics")
            comp = st.selectbox("Select Component:", ["Ohmic Resistor", "Filament Lamp", "Diode"])
            
            if comp == "Ohmic Resistor": st.write("📈 Graph shape: **Straight diagonal line passing through (0,0)**")
            elif comp == "Filament Lamp": st.write("⏳ Graph shape: **S-shaped curve due to temperature increase**")
            else: st.write("📐 Graph shape: **Flat zero current until 0.7V, then shoots straight up**")
            
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe a method the student could use to plot the Current-Voltage (I-V) characteristic curve for a component. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Assembly:** Construct a circuit containing the test component, an ammeter in series, a voltmeter in parallel across the component, and a variable resistor.
                2. **First reading:** Set the variable resistor to its maximum value and record the initial voltage and current readings.
                3. **Varying data:** Adjust the variable resistor in small steps to change the potential difference, taking a set of 5-6 current readings.
                4. **Negative bias:** Disconnect the battery wires and flip them around to reverse the direction of the potential difference.
                5. **Reverse tracking:** Adjust the variable resistor again to take negative voltage and negative current values.
                6. **Graph plot:** Plot a graph with Current on the y-axis and Potential Difference on the x-axis to reveal the curve.
                """)

        elif "RP 5" in selected_rp:
            st.markdown("### 🧱 RP 5: Determining Density (Regular vs Irregular Solids)")
            obj_type = st.radio("Object Shape Category:", ["Regular Shape (Cube/Brick)", "Irregular Shape (Stone/Key)"])
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                if "Regular" in obj_type:
                    st.markdown("""
                    **Question:** *Describe a method to find the density of a regular plastic block. [6 marks]*
                    
                    **Model Answer Checklist:**
                    1. **Mass:** Measure the mass of the regular block using a digital top-pan balance.
                    2. **Dimensions:** Use a ruler to measure the length, width, and height of the block.
                    3. **Volume:** Multiply the three dimensions together ($\text{Volume} = l \\times w \\times h$) to calculate its volume.
                    4. **Calculation:** Use the density formula: $\\text{Density} = \\frac{\\text{Mass}}{\\text{Volume}}$ ($\\rho = \\frac{m}{V}$).
                    """)
                else:
                    st.markdown("""
                    **Question:** *Describe a method to determine the density of an irregularly shaped small object. [6 marks]*
                    
                    **Model Answer Checklist:**
                    1. **Mass:** Measure the mass of the irregular object using a digital balance scale.
 2. **Displacement Setup:** Fill a displacement (Eureka) can with water until it aligns exactly level with the bottom of the spout. Place an empty measuring cylinder beneath the spout.
                    3. **Submersion:** Lower the irregular object gently into the water using a thin piece of string so it is fully submerged.
                    4. **Volume collection:** The object will displace its exact volume in water. Measure the volume of the collected displaced water at eye level.
                    5. **Calculation:** Divide the initial recorded mass by this displaced volume value using $\\rho = \\frac{m}{V}$.
                    """)

        elif "RP 6" in selected_rp:
            st.markdown("### 🪓 RP 6: Investigating Spring Extension (Hooke's Law)")
            weights = st.slider("Added Load Force (Newtons):", 0, 10, 3)
            st.write(f"📏 Simulated Spring Extension: **{weights * 2.5} cm**")
            
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe a laboratory method to investigate the relationship between the force applied to a spring and its extension. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Rigging:** Secure a clamp stand to the bench. Attach a spring to the top clamp, and hold a meter ruler vertically next to it.
                2. **Zero alignment:** Note the initial unstretched length using a pointer on the bottom loop.
                3. **Loading:** Add a 1 Newton weight hanger to the bottom hook of the spring.
                4. **Measurement:** Record the new position. Calculate extension by subtracting the unstretched length from this value.
                5. **Increments:** Repeat the process by adding 1N weights one at a time up to 5N or 6N.
                6. **Analysis:** Plot a graph of Force vs Extension. The straight line indicates they are directly proportional ($F=ke$), until it reaches the limit of proportionality.
                """)

        elif "RP 7" in selected_rp:
            st.markdown("### 🏎️ RP 7: Investigating Acceleration and Force")
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe a method to investigate how the force acting on a glider toy affects its acceleration rate. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Setup:** Set up an air track or low-friction ramp with a toy car connected via a string to a hanging weight stack.
                2. **Sensor timing:** Place two light gates along the track connected to a digital data logger.
                3. **Action:** Release the car and let the falling weight pull it down the track.
                4. **Calculation:** The data logger records initial velocity ($u$) and final velocity ($v$), dividing the change by the time taken ($a = \\frac{v-u}{t}$).
                5. **Changing Force:** Move a weight from the car body down to the hanging hook stack to change force while keeping system mass identical.
                6. **Plotting:** Repeat across a range of forces and plot Force vs Acceleration.
                """)

        elif "RP 8" in selected_rp:
            st.markdown("### 🌊 RP 8: Measuring Wave Properties (Ripple Tank)")
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe how a ripple tank can be used to measure the frequency, wavelength, and speed of water waves. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Setup:** Fill a shallow ripple tank with water. Set a vibrating wooden bar powered by a motor to touch the water surface.
                2. **Projection:** Place a lamp above the tank to project wave patterns onto a white card sheet underneath.
                3. **Wavelength:** Place a meter ruler on the card. Take a photograph, measure the distance across 10 clear wave crests, and divide by 10 to find 1 wavelength.
                4. **Frequency:** Film the waves in slow motion next to a timer, count how many waves pass a point over 10 seconds, and divide by 10.
                5. **Calculation:** Use the wave speed equation: $\\text{Wave Speed} = \\text{Frequency} \\times \\text{Wavelength}$ ($v = f \\lambda$).
                """)

        elif "RP 9" in selected_rp:
            st.markdown("### 🔦 RP 9: Investigating Light Reflection & Refraction")
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe an experiment using a ray box to investigate the reflection and refraction of light through a glass block. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Trace outline:** Place a rectangular glass block onto a sheet of white paper and trace around its border.
                2. **Normal Line:** Remove the block and draw a normal line perpendicular ($90^\\circ$) to the long edge outline.
                3. **Angles:** Use a protractor to mark out an angle of incidence (e.g., $30^\\circ$) from the normal line.
                4. **Ray tracking:** Shine a thin ray of light from a ray box along the incident line. Mark the exit ray path with pencil dots.
                5. **Interior links:** Remove the block, connect the entry point to the exit point with a straight line to track the refracted ray.
                6. **Analysis:** Measure the angle of reflection and the angle of refraction relative to the normal line using a protractor. Repeat for a range of angles.
                """)

        elif "RP 10" in selected_rp:
            st.markdown("### 📦 RP 10: Emission and Absorption of Infrared Heat")
            cube_side = st.selectbox("Select Surface Face of Leslie Cube:", ["Matt Black", "Shiny Black", "White", "Shiny Silver"])
            emissions = {"Matt Black": 98.0, "Shiny Black": 85.0, "White": 60.0, "Shiny Silver": 12.0}
            st.warning(f"🌡️ Infrared Thermopile Reading: **{emissions[cube_side]} Internal Units**")
            
            with st.expander("📝 View Perfect 6-Mark Exam Answer Template"):
                st.markdown("""
                **Question:** *Describe a method using a Leslie Cube to investigate how different surfaces emit infrared radiation. [6 marks]*
                
                **Model Answer Checklist:**
                1. **Setup:** Place a Leslie cube onto a heatproof mat on a level workbench.
                2. **Filling:** Fill the cube carefully with boiling water from a kettle.
                3. **Stabilization:** Wait a few minutes for the box surfaces to heat up to a steady temperature.
                4. **Measurement tool:** Hold an infrared detector at a fixed, identical distance (e.g., $10\text{ cm}$) from one of the vertical faces.
                5. **Tracking:** Record the value. Rotate the cube to measure emissions from all 4 remaining surfaces.
                6. **Conclusion:** The results will show that **Matt Black is the best emitter**, while **Shiny Silver is the poorest emitter** of infrared radiation.
                """)
