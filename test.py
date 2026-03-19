"""
Advanced Particle Physics Engine with Realistic Lighting
=========================================================
A sophisticated 2D particle system with physics-based simulation,
realistic lighting, shadows, and volumetric light effects.

Architecture:
- Configuration Layer: Centralized settings
- Utility Layer: Physics, Lighting, and Rendering engines
- Domain Layer: Particle and ParticleSystem classes
- Presentation Layer: Scene rendering and UI
- Application Layer: Main simulation loop
"""

import pygame
import random
import math


# ============================================================================
# CONFIGURATION LAYER
# ============================================================================

class Config:
    """Central configuration for all simulation parameters"""
    
    # Display
    WIDTH = 1200
    HEIGHT = 800
    FPS = 60
    
    # Physics
    NUM_PARTICLES = 500
    GRAVITY = 0.15
    AIR_RESISTANCE = 0.995
    BOUNCE_DAMPING = 0.85
    MAX_VELOCITY = 20
    
    # Environment
    FLOOR_HEIGHT = 650
    FLOOR_FRICTION = 0.95
    
    # Colors - Theme (warm, elegant aesthetic)
    BG_COLOR_TOP = (15, 20, 35)
    BG_COLOR_BOTTOM = (35, 40, 60)
    FLOOR_COLOR = (45, 50, 75)
    FLOOR_ACCENT = (60, 70, 100)
    
    # Lighting
    LIGHT_POS = (WIDTH // 2, 80)  # Center horizontally, positioned higher for better visibility
    LIGHT_BRIGHTNESS = 1.0
    LIGHT_COLOR = (255, 240, 180)  # Warm white light
    
    # Light Animation
    LIGHT_ANIMATE = False  # Enable/disable light movement (disabled - fixed position)
    LIGHT_MOVE_SPEED = 2.0  # Speed of light movement (pixels per frame)
    LIGHT_MOVE_DISTANCE = 400  # How far light moves left/right from center
    
    # Fountain Animation (moves opposite to light)
    FOUNTAIN_ANIMATE = True  # Enable/disable fountain movement
    FOUNTAIN_BASE_X = WIDTH // 2  # Center position of fountain
    FOUNTAIN_Y = FLOOR_HEIGHT - 10  # Y position of fountain
    
    # Speed Control Settings
    INITIAL_LIGHT_SPEED = 2.0  # Initial speed (pixels per frame)
    MIN_SPEED = 0.1  # Minimum speed
    MAX_SPEED = 5.0  # Maximum speed
    SPEED_ADJUSTMENT_STEP = 0.1  # Amount to change per key press
    
    # Particle Colors with gradients
    GRADIENT_COLORS = {
        'red': [(255, 50, 50), (255, 150, 100), (255, 200, 150)],
        'blue': [(50, 150, 255), (100, 180, 255), (150, 200, 255)],
        'green': [(50, 255, 100), (100, 255, 150), (150, 255, 200)],
        'purple': [(180, 50, 255), (200, 100, 255), (220, 150, 255)],
        'orange': [(255, 150, 50), (255, 180, 100), (255, 210, 150)],
    }
    
    COLOR_NAMES = list(GRADIENT_COLORS.keys())


# Initialize Pygame
pygame.init()


# ============================================================================
# UTILITY LAYER - Physics & Lighting Engines
# ============================================================================

class LightingEngine:
    """Manages all lighting calculations and effects"""
    
    @staticmethod
    def calculate_intensity_at(x, y, light_pos=None):
        """Calculate light intensity at a point using inverse square law"""
        if light_pos is None:
            light_pos = Config.LIGHT_POS
        
        lx, ly = light_pos
        dx = x - lx
        dy = y - ly
        distance = max(1, math.sqrt(dx**2 + dy**2))
        
        # Inverse square law: intensity = 1 / distance^2
        intensity = 1.0 / (1 + (distance / 100) ** 2)
        return intensity
    
    @staticmethod
    def calculate_shadow_projection(particle_x, particle_y, light_pos=None):
        """Calculate shadow position on floor based on light source"""
        if light_pos is None:
            light_pos = Config.LIGHT_POS
        
        lx, ly = light_pos
        dx = particle_x - lx
        dy = particle_y - ly
        
        if particle_y < Config.FLOOR_HEIGHT and abs(dy) > 0.1:
            t = (Config.FLOOR_HEIGHT - ly) / dy
            shadow_x = lx + dx * t
            return shadow_x
        return particle_x
    
    @staticmethod
    def apply_light_to_color(base_color, light_intensity, alpha=1.0):
        """Apply lighting effect to a color"""
        lit_color = tuple(
            min(255, int(base_color[i] * (0.5 + light_intensity)))
            for i in range(3)
        )
        return tuple(int(c * alpha) for c in lit_color)


class PhysicsEngine:
    """Manages all physics calculations"""
    
    @staticmethod
    def apply_gravity_and_drag(vx, vy, mass):
        """Apply gravity and air resistance"""
        vy += Config.GRAVITY * mass
        vx *= Config.AIR_RESISTANCE
        vy *= Config.AIR_RESISTANCE
        return vx, vy
    
    @staticmethod
    def apply_terminal_velocity(vx, vy):
        """Limit velocity to terminal velocity"""
        velocity = math.sqrt(vx**2 + vy**2)
        if velocity > Config.MAX_VELOCITY:
            scale = Config.MAX_VELOCITY / velocity
            vx *= scale
            vy *= scale
        return vx, vy
    
    @staticmethod
    def handle_wall_collision(x, y, vx, vy, size):
        """Handle collisions with left/right walls"""
        if x <= size:
            x = size
            vx = abs(vx) * Config.BOUNCE_DAMPING
        elif x >= Config.WIDTH - size:
            x = Config.WIDTH - size
            vx = -abs(vx) * Config.BOUNCE_DAMPING
        return x, vx
    
    @staticmethod
    def handle_floor_collision(x, y, vx, vy, size):
        """Handle collision with floor"""
        if y >= Config.FLOOR_HEIGHT - size:
            y = Config.FLOOR_HEIGHT - size
            vy = -abs(vy) * Config.BOUNCE_DAMPING * 0.7
            vx *= Config.FLOOR_FRICTION
        return y, vx, vy
    
    @staticmethod
    def handle_ceiling_collision(x, y, vx, vy, size):
        """Handle collision with ceiling"""
        if y <= size:
            y = size
            vy = abs(vy) * Config.BOUNCE_DAMPING
        return y, vy


# ============================================================================
# DOMAIN LAYER - Particle System
# ============================================================================

class Particle:
    """Represents a single particle with physics and rendering"""
    
    def __init__(self, x, y, vx=None, vy=None, color_name=None, is_fountain=False):
        # Position
        self.x = float(x)
        self.y = float(y)
        
        # Velocity initialization
        self._initialize_velocity(vx, vy, is_fountain)
        
        # Properties
        self.color_name = color_name or random.choice(Config.COLOR_NAMES)
        self.color_gradient = Config.GRADIENT_COLORS[self.color_name]
        self.mass = random.uniform(0.5, 2.0)
        self.size = max(2, int(self.mass * 3))
        self.max_size = self.size
        
        # Life and decay
        self.life = 300 + random.randint(-50, 50)
        self.max_life = self.life
        
        # Trail for visual feedback
        self.trail = []
        self.trail_max_length = 8
    
    def _initialize_velocity(self, vx, vy, is_fountain):
        """Initialize particle velocity based on conditions"""
        if is_fountain:
            # Fountain effect: particles shoot upward at angles
            angle = random.uniform(-math.pi / 2.5, -math.pi / 3.5)
            speed = random.uniform(5, 12)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        elif vx is None:
            # Random initial velocity
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 8)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        else:
            self.vx = vx
            self.vy = vy
    
    def update(self):
        """Update particle position and apply physics"""
        # Store trail
        if len(self.trail) >= self.trail_max_length:
            self.trail.pop(0)
        self.trail.append((self.x, self.y))
        
        # Apply physics
        self.vx, self.vy = PhysicsEngine.apply_gravity_and_drag(
            self.vx, self.vy, self.mass
        )
        self.vx, self.vy = PhysicsEngine.apply_terminal_velocity(self.vx, self.vy)
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Handle collisions
        self.x, self.vx = PhysicsEngine.handle_wall_collision(
            self.x, self.y, self.vx, self.vy, self.size
        )
        self.y, self.vx, self.vy = PhysicsEngine.handle_floor_collision(
            self.x, self.y, self.vx, self.vy, self.size
        )
        self.y, self.vy = PhysicsEngine.handle_ceiling_collision(
            self.x, self.y, self.vx, self.vy, self.size
        )
        
        # Age and fade
        self.life -= 1
        life_ratio = self.life / self.max_life
        self.size = max(1, int(self.max_size * life_ratio))
    
    def draw(self, screen, light_pos=None):
        """Draw particle with realistic lighting and shadows"""
        if self.life <= 0:
            return
        
        if light_pos is None:
            light_pos = Config.LIGHT_POS
        
        life_ratio = max(0, self.life / self.max_life)
        
        # Get gradient color
        gradient_index = int((1 - life_ratio) * (len(self.color_gradient) - 1))
        base_color = self.color_gradient[gradient_index]
        
        # Calculate lighting
        light_intensity = LightingEngine.calculate_intensity_at(self.x, self.y, light_pos)
        faded_color = LightingEngine.apply_light_to_color(base_color, light_intensity, life_ratio)
        
        # Draw shadow
        if self.y < Config.FLOOR_HEIGHT:
            self._draw_shadow(screen, base_color, light_intensity, life_ratio, light_pos)
        
        # Draw trail
        if len(self.trail) > 1:
            self._draw_trail(screen, base_color, life_ratio, light_pos)
        
        # Draw glow
        if self.size > 1:
            self._draw_glow(screen, base_color, light_intensity, life_ratio)
        
        # Draw main particle
        if self.size > 0:
            pygame.draw.circle(screen, faded_color, (int(self.x), int(self.y)), self.size)
    
    def _draw_shadow(self, screen, base_color, light_intensity, life_ratio, light_pos):
        """Draw particle shadow on floor"""
        shadow_x = LightingEngine.calculate_shadow_projection(self.x, self.y, light_pos)
        
        height_ratio = (Config.FLOOR_HEIGHT - self.y) / Config.FLOOR_HEIGHT
        shadow_intensity = height_ratio * max(0, 1 - light_intensity) * life_ratio
        
        for shadow_layer in range(int(self.size * 2), 0, -1):
            layer_intensity = shadow_intensity * (1 - shadow_layer / (self.size * 2))
            shadow_color = tuple(int(c * layer_intensity * 0.3) for c in base_color)
            if layer_intensity > 0.02:
                pygame.draw.circle(screen, shadow_color, 
                                  (int(shadow_x), int(Config.FLOOR_HEIGHT - 2)), 
                                  shadow_layer)
    
    def _draw_trail(self, screen, base_color, life_ratio, light_pos):
        """Draw particle trail with gradient fade"""
        for i, (tx, ty) in enumerate(self.trail):
            trail_light = LightingEngine.calculate_intensity_at(tx, ty, light_pos)
            trail_alpha = (i / len(self.trail)) * life_ratio
            trail_size = max(1, int(self.size * trail_alpha))
            trail_base = tuple(int(c * (0.3 + trail_light * 0.4)) for c in base_color)
            trail_color = tuple(int(c * trail_alpha * 0.5) for c in trail_base)
            if trail_size > 0:
                pygame.draw.circle(screen, trail_color, (int(tx), int(ty)), trail_size)
    
    def _draw_glow(self, screen, base_color, light_intensity, life_ratio):
        """Draw particle glow effect based on lighting"""
        glow_intensity = 0.2 + light_intensity * 0.3
        glow_color = tuple(int(c * glow_intensity * life_ratio) for c in base_color)
        pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), 
                          int(self.size * 2), 2)
    
    def is_alive(self):
        """Check if particle is still alive"""
        return self.life > 0


class ParticleSystem:
    """Manages all particles in the simulation"""
    
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x, y, vx=None, vy=None, color_name=None, is_fountain=False):
        """Add a new particle to the system"""
        if len(self.particles) < Config.NUM_PARTICLES:
            self.particles.append(Particle(x, y, vx, vy, color_name, is_fountain))
    
    def add_burst(self, x, y, count=30, color=None):
        """Add multiple particles at once (burst effect)"""
        for _ in range(count):
            self.add_particle(x, y, color_name=color)
    
    def add_fountain_emission(self, rate=0.6, fountain_pos=None):
        """Generate particles continuously from fountain"""
        if fountain_pos is None:
            fountain_pos = (Config.FOUNTAIN_BASE_X, Config.FOUNTAIN_Y)
        
        if random.random() < rate and len(self.particles) < Config.NUM_PARTICLES:
            fountain_x, fountain_y = fountain_pos
            color = random.choice(Config.COLOR_NAMES)
            self.add_particle(fountain_x, fountain_y, color_name=color, is_fountain=True)
    
    def update(self):
        """Update all particles"""
        for particle in self.particles:
            particle.update()
    
    def apply_particle_interactions(self):
        """Apply particle-to-particle gravitational interactions"""
        if len(self.particles) > 50 and random.random() < 0.1:
            for i, p1 in enumerate(self.particles):
                if i % 10 == 0 and len(self.particles) > i + 1:
                    p2 = self.particles[random.randint(
                        i + 1, min(len(self.particles) - 1, i + 20)
                    )]
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    dist = math.sqrt(dx**2 + dy**2)
                    if 1 < dist < 150:
                        force = 0.0002 * p1.mass * p2.mass / (dist + 1)
                        p1.vx += (dx / dist) * force
                        p1.vy += (dy / dist) * force
    
    def draw(self, screen, light_pos=None):
        """Draw all particles"""
        if light_pos is None:
            light_pos = Config.LIGHT_POS
        for particle in self.particles:
            particle.draw(screen, light_pos)
    
    def cleanup_dead(self):
        """Remove dead particles"""
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()
    
    def get_count(self):
        """Get current particle count"""
        return len(self.particles)


# ============================================================================
# PRESENTATION LAYER - Scene Rendering
# ============================================================================

class RenderEngine:
    """Handles all rendering operations"""
    
    @staticmethod
    def draw_background(screen):
        """Draw sky background with clouds"""
        # Sky gradient: light blue at top, lighter blue at horizon
        sky_top = (135, 206, 235)      # Sky blue
        sky_horizon = (200, 230, 255)  # Lighter blue
        sky_bottom = (100, 180, 220)   # Darker blue lower
        
        # Draw gradient sky
        for y in range(Config.HEIGHT):
            if y < Config.HEIGHT * 0.7:
                # Upper sky gradient
                ratio = y / (Config.HEIGHT * 0.7)
                color = (
                    int(sky_top[0] + (sky_horizon[0] - sky_top[0]) * ratio),
                    int(sky_top[1] + (sky_horizon[1] - sky_top[1]) * ratio),
                    int(sky_top[2] + (sky_horizon[2] - sky_top[2]) * ratio)
                )
            else:
                # Lower sky to horizon
                ratio = (y - Config.HEIGHT * 0.7) / (Config.HEIGHT * 0.3)
                color = (
                    int(sky_horizon[0] + (sky_bottom[0] - sky_horizon[0]) * ratio),
                    int(sky_horizon[1] + (sky_bottom[1] - sky_horizon[1]) * ratio),
                    int(sky_horizon[2] + (sky_bottom[2] - sky_horizon[2]) * ratio)
                )
            pygame.draw.line(screen, color, (0, y), (Config.WIDTH, y))
        
        # Draw procedural clouds
        RenderEngine._draw_clouds(screen)
    
    @staticmethod
    def _draw_clouds(screen):
        """Draw procedurally generated clouds"""
        cloud_data = [
            # (x_center, y_center, size_scale, opacity)
            (250, 100, 1.2, 0.7),
            (500, 150, 1.5, 0.6),
            (800, 80, 1.3, 0.65),
            (1000, 180, 1.1, 0.75),
            (150, 200, 1.0, 0.5),
            (1100, 280, 1.4, 0.6),
        ]
        
        cloud_color = (255, 255, 255)
        
        for cx, cy, scale, opacity in cloud_data:
            # Draw cloud as multiple overlapping circles
            cloud_radius = int(40 * scale)
            
            # Create a surface for the cloud with transparency
            cloud_surf = pygame.Surface((cloud_radius * 3, cloud_radius * 2), pygame.SRCALPHA)
            
            # Draw cloud puffs
            puff_positions = [
                (cloud_radius * 0.5, cloud_radius * 0.6),
                (cloud_radius * 1.0, cloud_radius * 0.4),
                (cloud_radius * 1.5, cloud_radius * 0.6),
                (cloud_radius * 0.8, cloud_radius * 1.1),
                (cloud_radius * 1.3, cloud_radius * 1.0),
            ]
            
            for px, py in puff_positions:
                alpha = int(255 * opacity)
                color_with_alpha = cloud_color + (alpha,)
                pygame.draw.circle(cloud_surf, color_with_alpha, 
                                 (int(px), int(py)), cloud_radius // 2)
            
            # Blit the cloud surface to the main screen
            screen.blit(cloud_surf, 
                       (int(cx - cloud_radius * 1.5), int(cy - cloud_radius)))
    
    @staticmethod
    def draw_volumetric_rays(screen, light_pos=None):
        """Draw volumetric light rays (crepuscular rays)"""
        if light_pos is None:
            light_pos = Config.LIGHT_POS
        lx, ly = light_pos
        num_primary_rays = 32
        
        for layer in range(3):
            layer_variation = layer * 0.3
            
            for i in range(num_primary_rays):
                angle = (i / num_primary_rays) * 2 * math.pi + layer_variation
                
                # Ray origin
                ray_start_x = lx + math.cos(angle) * (5 + layer * 2)
                ray_start_y = ly + math.sin(angle) * (5 + layer * 2)
                
                ray_length = 800
                ray_end_x = lx + math.cos(angle) * ray_length
                ray_end_y = ly + math.sin(angle) * ray_length
                
                # Draw gradient ray
                gradient_steps = 50
                for step in range(gradient_steps):
                    progress = step / gradient_steps
                    current_x = ray_start_x + (ray_end_x - ray_start_x) * progress
                    current_y = ray_start_y + (ray_end_y - ray_start_y) * progress
                    
                    if current_y > Config.FLOOR_HEIGHT:
                        break
                    
                    brightness = (1 - progress) * (1 - layer * 0.3) * 0.08
                    ray_color = (
                        int(Config.LIGHT_COLOR[0] * brightness),
                        int(Config.LIGHT_COLOR[1] * brightness * 0.9),
                        int(Config.LIGHT_COLOR[2] * brightness * 0.6)
                    )
                    
                    next_x = ray_start_x + (ray_end_x - ray_start_x) * (step + 1) / gradient_steps
                    next_y = ray_start_y + (ray_end_y - ray_start_y) * (step + 1) / gradient_steps
                    
                    if ray_color[0] > 5 or ray_color[1] > 5:
                        pygame.draw.line(screen, ray_color, (current_x, current_y), 
                                       (next_x, next_y), 2)
    
    @staticmethod
    def draw_light_source(screen, light_pos=None):
        """Draw realistic light source with bloom"""
        if light_pos is None:
            light_pos = Config.LIGHT_POS
        lx, ly = light_pos
        
        # Draw bloom layers
        bloom_layers = 80
        for radius in range(bloom_layers, 0, -1):
            intensity = (1 - (radius / bloom_layers)) ** 2
            
            bloom_color = (
                int(Config.LIGHT_COLOR[0] * intensity * 0.5),
                int(Config.LIGHT_COLOR[1] * intensity * 0.4),
                int(Config.LIGHT_COLOR[2] * intensity * 0.2)
            )
            
            if intensity > 0.01:
                pygame.draw.circle(screen, bloom_color, (lx, ly), radius, 1)
        
        # Draw light core
        pygame.draw.circle(screen, Config.LIGHT_COLOR, (lx, ly), 15)
        pygame.draw.circle(screen, (255, 255, 255), (lx, ly), 10)
        pygame.draw.circle(screen, (255, 250, 230), (lx, ly), 5)
    
    @staticmethod
    def draw_floor_with_light(screen, light_pos=None, fountain_pos=None):
        """Draw floor with proper lighting response"""
        if light_pos is None:
            light_pos = Config.LIGHT_POS
        if fountain_pos is None:
            fountain_pos = (Config.FOUNTAIN_BASE_X, Config.FOUNTAIN_Y)
        # Main floor - brighter base colors
        for x in range(0, Config.WIDTH, 10):
            light_intensity = LightingEngine.calculate_intensity_at(x, Config.FLOOR_HEIGHT, light_pos)
            brightness = 0.65 + light_intensity * 0.7  # Increased base brightness
            
            # Brighter floor colors
            brighter_floor = (100, 110, 140)  # Lighter gray-blue
            floor_color = (
                int(brighter_floor[0] * brightness),
                int(brighter_floor[1] * brightness),
                int(brighter_floor[2] * brightness)
            )
            pygame.draw.line(screen, floor_color, (x, Config.FLOOR_HEIGHT), 
                           (x + 10, Config.FLOOR_HEIGHT), 
                           int(Config.HEIGHT - Config.FLOOR_HEIGHT))
        
        # Floor accent line - much brighter
        for x in range(0, Config.WIDTH, 5):
            light_intensity = LightingEngine.calculate_intensity_at(x, Config.FLOOR_HEIGHT, light_pos)
            brightness = 0.7 + light_intensity * 0.9  # Increased brightness
            # Brighter accent colors
            brighter_accent = (150, 160, 190)
            accent_color = (
                int(brighter_accent[0] * brightness),
                int(brighter_accent[1] * brightness),
                int(brighter_accent[2] * brightness)
            )
            pygame.draw.line(screen, accent_color, (x, Config.FLOOR_HEIGHT), 
                           (x + 5, Config.FLOOR_HEIGHT), 4)
        
        # Draw fountain base - much brighter
        fountain_x, fountain_y = fountain_pos
        fountain_radius = 40
        
        light_intensity = LightingEngine.calculate_intensity_at(fountain_x, Config.FLOOR_HEIGHT, light_pos)
        basin_brightness = 0.7 + light_intensity * 0.8  # Brighter
        basin_color = (
            int(160 * basin_brightness),
            int(170 * basin_brightness),
            int(190 * basin_brightness)
        )
        
        pygame.draw.circle(screen, basin_color, (int(fountain_x), int(Config.FLOOR_HEIGHT - 5)), 
                          fountain_radius, 3)
        pygame.draw.circle(screen, basin_color, (int(fountain_x), int(Config.FLOOR_HEIGHT)), 
                          fountain_radius - 10, 2)
        
        # Fountain nozzle
        nozzle_color = (
            int(150 * basin_brightness),
            int(150 * basin_brightness),
            int(160 * basin_brightness)
        )
        pygame.draw.circle(screen, nozzle_color, (int(fountain_x), int(Config.FLOOR_HEIGHT - 8)), 8)
        pygame.draw.circle(screen, (180, 180, 200), (int(fountain_x), int(Config.FLOOR_HEIGHT - 8)), 5)
    
    @staticmethod
    @staticmethod
    def draw_ui(screen, particle_count, fps, paused, show_info, light_speed=None):
        """Draw user interface elements"""
        if show_info:
            font_small = pygame.font.Font(None, 18)
            info_texts = [
                f"Particles: {particle_count}/{Config.NUM_PARTICLES}",
                f"FPS: {int(fps)}",
                f"Speed: {light_speed:.1f}x | UP/DOWN to adjust | SPACE to pause | I to hide info | C to clear"
            ]
            
            for i, text_str in enumerate(info_texts):
                text = font_small.render(text_str, True, (200, 220, 255))
                screen.blit(text, (15, 15 + i * 25))
        
        if paused:
            font_large = pygame.font.Font(None, 28)
            pause_text = font_large.render("PAUSED (SPACE to resume)", True, (255, 100, 100))
            screen.blit(pause_text, (Config.WIDTH // 2 - 200, Config.HEIGHT // 2 - 25))


# ============================================================================
# APPLICATION LAYER - Main Simulation
# ============================================================================

class Simulation:
    """Main simulation controller"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption(
            "Advanced Particle System - Physics Engine with Lighting"
        )
        self.clock = pygame.time.Clock()
        
        self.particle_system = ParticleSystem()
        self.running = True
        self.paused = False
        self.show_info = True
        
        # Light animation
        self.frame_count = 0
        self.light_pos = list(Config.LIGHT_POS)
        
        # Fountain animation (opposite direction)
        self.fountain_pos = [Config.FOUNTAIN_BASE_X, Config.FOUNTAIN_Y]
        
        # Speed control
        self.light_speed = Config.INITIAL_LIGHT_SPEED
        self.fountain_speed = Config.INITIAL_LIGHT_SPEED  # Fountain moves at same speed as light
    
    def handle_events(self):
        """Handle user input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create particles on mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                color = random.choice(Config.COLOR_NAMES)
                self.particle_system.add_burst(mouse_x, mouse_y, count=30, color=color)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                elif event.key == pygame.K_c:
                    self.particle_system.clear()
                
                # Speed control with arrow keys
                elif event.key == pygame.K_UP:
                    # Increase speed
                    new_speed = min(self.light_speed + Config.SPEED_ADJUSTMENT_STEP, Config.MAX_SPEED)
                    self.light_speed = new_speed
                    self.fountain_speed = new_speed
                elif event.key == pygame.K_DOWN:
                    # Decrease speed
                    new_speed = max(self.light_speed - Config.SPEED_ADJUSTMENT_STEP, Config.MIN_SPEED)
                    self.light_speed = new_speed
                    self.fountain_speed = new_speed
                
                # Alternative speed control with + and - keys
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    new_speed = min(self.light_speed + Config.SPEED_ADJUSTMENT_STEP, Config.MAX_SPEED)
                    self.light_speed = new_speed
                    self.fountain_speed = new_speed
                elif event.key == pygame.K_MINUS:
                    new_speed = max(self.light_speed - Config.SPEED_ADJUSTMENT_STEP, Config.MIN_SPEED)
                    self.light_speed = new_speed
                    self.fountain_speed = new_speed
    
    def update(self):
        """Update simulation state"""
        # Increment frame counter (used for animations)
        self.frame_count += 1
        
        # Animate light position (X only, Y stays fixed)
        if Config.LIGHT_ANIMATE:
            # Use sine wave for smooth back-and-forth motion
            center_x = Config.WIDTH // 2
            offset_x = math.sin(self.frame_count * self.light_speed * 0.05) * (Config.LIGHT_MOVE_DISTANCE / 2)
            self.light_pos[0] = center_x + offset_x
            self.light_pos[1] = Config.LIGHT_POS[1]  # Keep Y position fixed
        else:
            # Keep light at fixed position
            self.light_pos = list(Config.LIGHT_POS)
        
        # Animate fountain position (opposite direction to light)
        if Config.FOUNTAIN_ANIMATE:
            center_x = Config.FOUNTAIN_BASE_X
            # Fountain moves opposite to light: if light goes right (positive offset), fountain goes left (negative offset)
            offset_x = -math.sin(self.frame_count * self.fountain_speed * 0.05) * (Config.LIGHT_MOVE_DISTANCE / 2)
            self.fountain_pos[0] = center_x + offset_x
        
        if not self.paused:
            # Generate fountain particles at updated position
            self.particle_system.add_fountain_emission(rate=0.6, fountain_pos=tuple(self.fountain_pos))
            
            # Update particles
            self.particle_system.update()
            
            # Apply interactions
            self.particle_system.apply_particle_interactions()
        
        # Clean up dead particles
        self.particle_system.cleanup_dead()
    
    def render(self):
        """Render the scene"""
        # Draw background and environment
        RenderEngine.draw_background(self.screen)
        RenderEngine.draw_floor_with_light(self.screen, tuple(self.light_pos), tuple(self.fountain_pos))
        # Volumetric rays removed for cleaner look
        
        # Draw particles
        self.particle_system.draw(self.screen, tuple(self.light_pos))
        
        # Draw lighting
        RenderEngine.draw_light_source(self.screen, tuple(self.light_pos))
        
        # Draw UI
        RenderEngine.draw_ui(self.screen, self.particle_system.get_count(), 
                            self.clock.get_fps(), self.paused, self.show_info, self.light_speed)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main simulation loop"""
        while self.running:
            self.clock.tick(Config.FPS)
            
            self.handle_events()
            self.update()
            self.render()
        
        pygame.quit()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
