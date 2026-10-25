import math
import streamlit as st  # <-- 1. Added Streamlit here

# --- WEBSITE INTERFACE CONFIGURATION ---
st.title("🏹 Projectile Motion Simulator")
st.write("This interactive application simulates a projectile's flight path using real physics equations incorporating gravity and air resistance.")

class Projectile:
    def __init__(self, x, y, velocity, angle_degrees, mass):
        self.x = x  
        self.y = y  
        self.mass = mass  
        
        angle_rad = math.radians(angle_degrees)
        
        self.vx = velocity * math.cos(angle_rad)
        self.vy = velocity * math.sin(angle_rad)
        
        self.g = 9.81         
        self.drag_coef = 0.47 

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
ball = Projectile(x=0, y=0, velocity=30, angle_degrees=45, mass=0.5)
dt = 0.01  

# We will collect the data into a list to display nicely on the web page
telemetry_data = []

time_elapsed = 0.0
while ball.y >= 0: 
    ball.update_physics(dt)
    time_elapsed += dt
    
    # Save the data points to display in a chart and table
    if round(time_elapsed, 3) % 0.2 == 0:
        telemetry_data.append({
            "Time (s)": round(time_elapsed, 1),
            "X Position (m)": round(ball.x, 2),
            "Y Position (m)": round(ball.y, 2)
        })

# --- 2. DISPLAY DATA TO THE USER ---
st.subheader("📊 Simulation Results")

# Show a neat visual graph of the trajectory path (X vs Y position)
st.line_chart(data=telemetry_data, x="X Position (m)", y="Y Position (m)")

# Show the raw telemetry table underneath
st.subheader("📋 Raw Telemetry Data")
st.dataframe(telemetry_data, use_container_width=True)
