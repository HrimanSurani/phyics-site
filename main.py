import math

class Projectile:
    def __init__(self, x, y, velocity, angle_degrees, mass):
        self.x = x  # Horizontal position (metres)
        self.y = y  # Vertical position (metres)
        self.mass = mass  # Mass (kg)
        
        # Convert angle to radians for trigonometry
        angle_rad = math.radians(angle_degrees)
        
        # Split initial velocity into horizontal (x) and vertical (y) vectors
        self.vx = velocity * math.cos(angle_rad)
        self.vy = velocity * math.sin(angle_rad)
        
        # Physics constants
        self.g = 9.81         # Acceleration due to gravity (m/s^2)
        self.drag_coef = 0.47 # Drag coefficient (approx. for a sphere)

    def update_physics(self, dt):
        """Calculates the object's next position over a tiny timeframe (dt)"""
        # 1. Calculate current speed (magnitude of velocity vector)
        speed = math.sqrt(self.vx**2 + self.vy**2)
        
        # 2. Calculate Drag Force (F = 0.5 * drag_coef * speed^2)
        # For simplicity, we assume fluid density and cross-section equal 1
        f_drag = 0.5 * self.drag_coef * (speed**2)
        
        # 3. Break Drag Force down into x and y directions (opposing motion)
        if speed > 0:
            f_drag_x = -f_drag * (self.vx / speed)
            f_drag_y = -f_drag * (self.vy / speed)
        else:
            f_drag_x, f_drag_y = 0, 0
            
        # 4. Calculate Net Accelerations (a = F / m)
        ax = f_drag_x / self.mass
        ay = -self.g + (f_drag_y / self.mass) # Gravity pulls down, drag opposes upward/downward movement
        
        # 5. Update Velocities (v = u + at)
        self.vx += ax * dt
        self.vy += ay * dt
        
        # 6. Update Positions (s = vt)
        self.x += self.vx * dt
        self.y += self.vy * dt

# --- RUNNING A SIMULATION ---
ball = Projectile(x=0, y=0, velocity=30, angle_degrees=45, mass=0.5)
dt = 0.01  # Progress time in 10-millisecond chunks

print("Time (s) | X Pos (m) | Y Pos (m)")
print("-" * 32)

time_elapsed = 0.0
while ball.y >= 0: # Run until the ball hits the ground
    ball.update_physics(dt)
    time_elapsed += dt
    # Print telemetry data every 0.2 seconds to avoid spamming the console
    if round(time_elapsed, 3) % 0.2 == 0:
        print(f"{time_elapsed:8.1f} | {ball.x:9.2f} | {ball.y:9.2f}")
