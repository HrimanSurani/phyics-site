import math
import streamlit as st

# --- WEBSITE CONFIGURATION ---
st.set_page_config(page_title="Projectile Simulation", layout="wide")

st.title("🏹 Interactive Projectile Motion Simulator")
st.write("Adjust the parameters in the sidebar to see how velocity, angle, mass, and gravity alter the trajectory path.")

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.header("🛠️ Simulation Parameters")

# Sliders that let the user control variables interactively
velocity = st.sidebar.slider("Initial Velocity (m/s)", min_value=5.0, max_value=100.0, value=30.0, step=1.0)
angle_degrees = st.sidebar.slider("Launch Angle (degrees)", min_value=0, max_value=90, value=45, step=1)
mass = st.sidebar.slider("Object Mass (kg)", min_value=0.1, max_value=10.0, value=0.5, step=0.1)
enable_drag = st.sidebar.toggle("Enable Air Resistance", value=True)

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

# --- RUNNING THE SIMULATION ---
ball = Projectile(x=0, y=0, velocity=velocity, angle_degrees=angle_degrees, mass=mass, enable_drag=enable_drag)
dt = 0.005  # Made step smaller for an ultra-smooth trajectory curve

# Create containers to store x and y data points for the graph
x_coords = [0.0]
y_coords = [0.0]

time_elapsed = 0.0
# Guard against infinitely running loops if angle is 0 or edge cases occur
max_steps = 10000 
step_count = 0

while ball.y >= 0 and step_count < max_steps: 
    ball.update_physics(dt)
    time_elapsed += dt
    step_count += 1
    
    # Save every position calculation to ensure a perfect graph path
    x_coords.append(ball.x)
    y_coords.append(ball.y)

# Format data into a dictionary structure Streamlit natively maps out
chart_data = {
    "Horizontal Distance (m)": x_coords,
    "Vertical Height (m)": y_coords
}

# --- RENDER DASHBOARD LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Trajectory Path")
    # Draw a line chart plotting vertical height across horizontal distance
    st.line_chart(data=chart_data, x="Horizontal Distance (m)", y="Vertical Height (m)")

with col2:
    st.subheader("📋 Key Metrics")
    # Highlight final data summary milestones
    st.metric(label="Total Distance Traveled", value=f"{x_coords[-1]:.2f} meters")
    st.metric(label="Total Flight Time", value=f"{time_elapsed:.2f} seconds")
    st.metric(label="Peak Height Reached", value=f"{max(y_coords):.2f} meters")
