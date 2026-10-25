import math
import time
import streamlit as st

# --- WEBSITE MASTER CONFIGURATION ---
st.set_page_config(page_title="Physics Sandbox Laboratory", layout="wide")

# Navigation Sidebar to pick between different modules
st.sidebar.title("🔬 Physics Lab Menu")
module = st.sidebar.selectbox("Choose a Physics Topic:", ["Planetary Orbit Sandbox", "Projectile Motion Simulator"])

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
