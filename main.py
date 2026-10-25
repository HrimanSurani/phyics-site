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
    
    # Physics Variables
    star_mass = st.sidebar.slider("Star Mass (scaled x10^13 kg)", min_value=1.0, max_value=50.0, value=20.0, step=1.0)
    init_dist = st.sidebar.slider("Initial Distance from Star (AU-scaled)", min_value=20.0, max_value=150.0, value=100.0, step=5.0)
    init_speed = st.sidebar.slider("Initial Tangential Speed", min_value=0.0, max_value=15.0, value=8.5, step=0.5)
    
    # Play controls
    st.sidebar.markdown("---")
    sim_steps = st.sidebar.slider("Simulation Length (Frames)", min_value=200, max_value=2000, value=800, step=100)
    run_orbit = st.sidebar.button("🚀 Launch Planet Into Orbit")

    # --- ORBIT PHYSICS ENGINE ---
    # Scaling constant for stable screen math calculations
    G = 1.0 
    
    # Planet starting status vectors
    # We position the planet at (init_dist, 0) and shoot it vertically up (0, init_speed)
    x, y = init_dist, 0.0
    vx, vy = 0.0, init_speed
    
    dt = 0.1 # Time precision delta
    
    x_history = [x]
    y_history = [y]
    distances = [init_dist]
    speeds = [init_speed]

    # Pre-calculating the physics frame loop arrays
    for _ in range(sim_steps):
        # 1. Distance vector from central star (positioned at 0,0 origin coordinates)
        r = math.sqrt(x**2 + y**2)
        if r < 5.0: # Safeguard collision check if the planet crashes directly into the star
            break
            
        distances.append(r)
        
        # 2. Total Gravitational Force Acceleration (a = G * M / r^2)
        accel_total = (G * star_mass) / (r**2)
        
        # 3. Resolve vector directions toward the coordinate origin center
        ax = -accel_total * (x / r)
        ay = -accel_total * (y / r)
        
        # 4. Integrate vectors step-by-step
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        
        x_history.append(x)
        y_history.append(y)
        speeds.append(math.sqrt(vx**2 + vy**2))

    # --- LAYOUT DASHBOARD HOOKS ---
    col1, col2 = st.columns([2, 1]) # Make graph section wider

    with col1:
        st.subheader("🌌 System Orbit Tracking View")
        orbit_placeholder = st.empty()

    with col2:
        st.subheader("📉 Real-Time Telemetry Metrics")
        dist_metric = st.empty()
        speed_metric = st.empty()
        status_metric = st.empty()

    # --- LIVE RENDER DRAWING LOOP ---
    # Creates an active rendering loop
    step_skip = max(1, len(x_history) // 50)
    
    for i in range(1, len(x_history), step_skip):
        # Package path data into structural display frames
        # We append a single point at (0,0) to anchor the central star icon securely on graph layers
        current_data = {
            "X Position": x_history[:i] + [0.0],
            "Y Position": y_history[:i] + [0.0]
        }
        
        # Re-render active window map view canvas frame
        orbit_placeholder.line_chart(data=current_data, x="X Position", y="Y Position", height=500)
        
        # Calculate changing values dynamically for metrics panels
        current_r = distances[min(i, len(distances)-1)]
        current_v = speeds[min(i, len(speeds)-1)]
        
        dist_metric.metric("Current Orbital Radius", f"{current_r:.2f} AU")
        speed_metric.metric("Current Velocity Vector", f"{current_v:.2f} units/s")
        
        # Provide real-time status clues about orbit shapes
        if max(distances) - min(distances) < 2.0:
            status_metric.info("Stable Circular Alignment")
        elif current_v > init_speed * 1.3:
            status_metric.warning("High Eccentric Periapsis Passage")
        else:
            status_metric.success("Elliptical Trajectory Loop")
            
        time.sleep(0.01)

    # Output concluding anchor points cleanly
    final_data = {"X Position": x_history + [0.0], "Y Position": y_history + [0.0]}
    orbit_placeholder.line_chart(data=final_data, x="X Position", y="Y Position", height=500)


# ==========================================
# MODULE 2: PROJECTILE MOTION SIMULATOR
# ==========================================
elif module == "Projectile Motion Simulator":
    st.title("🏹 Interactive Projectile Motion Simulator")
    st.write("Adjust parameters in the sidebar and watch the motion physics simulate in real time.")

    # --- SIDEBAR CONTROL PANEL ---
    st.sidebar.header("🛠️ Simulation Parameters")

    velocity = st.sidebar.slider("Initial Velocity (m/s)", min_value=5.0, max_value=100.0, value=30.0, step=1.0)
    angle_degrees = st.sidebar.slider("Launch Angle (degrees)", min_value=0, max_value=90, value=45, step=1)
    mass = st.sidebar.slider("Object Mass (kg)", min_value=0.1, max_value=10.0, value=0.5, step=0.1)
    enable_drag = st.sidebar.toggle("Enable Air Resistance", value=True)
    replay_btn = st.sidebar.button("🔄 Re-run Animation")

    # --- PHYSICS ENGINE CLASS ---
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

    # --- PRE-CALCULATE FULL PATH ---
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

    # --- DASHBOARD LAYOUT BLOCKS ---
    col1, col2 = st.columns([2, 1]) 

    with col1:
        st.subheader("📊 Trajectory Path")
        chart_placeholder = st.empty()

    with col2:
        st.subheader("📋 Final Metrics")
        st.metric(label="Total Distance Traveled", value=f"{all_x[-1]:.2f} meters")
        st.metric(label="Total Flight Time", value=f"{time_elapsed:.2f} seconds")
        st.metric(label="Peak Height Reached", value=f"{max(all_y):.2f} meters")

    # --- LIVE LOOPING ANIMATION EFFECT ---
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
