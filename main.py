import math
import time
import streamlit as st

# --- WEBSITE CONFIGURATION ---
st.set_page_config(page_title="Projectile Simulation", layout="wide")

st.title("🏹 Interactive Projectile Motion Simulator")
st.write("Adjust parameters in the sidebar and watch the motion physics simulate in real time.")

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("🛠️ Simulation Parameters")

velocity = st.sidebar.slider("Initial Velocity (m/s)", min_value=5.0, max_value=100.0, value=30.0, step=1.0)
angle_degrees = st.sidebar.slider("Launch Angle (degrees)", min_value=0, max_value=90, value=45, step=1)
mass = st.sidebar.slider("Object Mass (kg)", min_value=0.1, max_value=10.0, value=0.5, step=0.1)
enable_drag = st.sidebar.toggle("Enable Air Resistance", value=True)

# Add an animation toggle so users can re-run the animation manually
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
dt = 0.01  # Step speed optimized for calculation smoothness

all_x = [0.0]
all_y = [0.0]
time_elapsed = 0.0

while ball.y >= 0 and len(all_x) < 5000: 
    ball.update_physics(dt)
    time_elapsed += dt
    all_x.append(ball.x)
    all_y.append(ball.y)

# --- DASHBOARD LAYOUT BLOCKS ---
col1, col2 = st.columns([2, 1]) # Column 1 is twice as wide for the chart

with col1:
    st.subheader("📊 Trajectory Path")
    # 1. Create an empty container handle to drop our updating chart into
    chart_placeholder = st.empty()

with col2:
    st.subheader("📋 Final Metrics")
    st.metric(label="Total Distance Traveled", value=f"{all_x[-1]:.2f} meters")
    st.metric(label="Total Flight Time", value=f"{time_elapsed:.2f} seconds")
    st.metric(label="Peak Height Reached", value=f"{max(all_y):.2f} meters")

# --- 2. LIVE LOOPING ANIMATION EFFECT ---
# We feed the graph increments of our pre-calculated array smoothly
animation_speed_factor = max(1, len(all_x) // 40) # Dynamically skips steps for fast parameters

for i in range(1, len(all_x), animation_speed_factor):
    # Slice the coordinates up to the current point
    current_chart_data = {
        "Horizontal Distance (m)": all_x[:i],
        "Vertical Height (m)": all_y[:i]
    }
    # Swap out the data inside the chart frame container
    chart_placeholder.line_chart(data=current_chart_data, x="Horizontal Distance (m)", y="Vertical Height (m)")
    time.sleep(0.01) # 10ms frame pacing delay

# Ensure the final point is neatly drawn when the loop closes
final_chart_data = {
    "Horizontal Distance (m)": all_x,
    "Vertical Height (m)": all_y
}
chart_placeholder.line_chart(data=final_chart_data, x="Horizontal Distance (m)", y="Vertical Height (m)")
