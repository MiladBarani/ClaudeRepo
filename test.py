import pygame
import random
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
NUM_PARTICLES = 500
GRAVITY = 0.15
AIR_RESISTANCE = 0.995
BOUNCE_DAMPING = 0.85
FLOOR_HEIGHT = 650

# Theme Colors (warm, elegant aesthetic)
BG_COLOR_TOP = (15, 20, 35)
BG_COLOR_BOTTOM = (35, 40, 60)
FLOOR_COLOR = (45, 50, 75)
FLOOR_ACCENT = (60, 70, 100)

# Light source
LIGHT_POS = (WIDTH // 2, 100)
LIGHT_BRIGHTNESS = 1.0
LIGHT_COLOR = (255, 240, 180)  # Warm white light

# Colors with gradients
GRADIENT_COLORS = {
    'red': [(255, 50, 50), (255, 150, 100), (255, 200, 150)],
    'blue': [(50, 150, 255), (100, 180, 255), (150, 200, 255)],
    'green': [(50, 255, 100), (100, 255, 150), (150, 255, 200)],
    'purple': [(180, 50, 255), (200, 100, 255), (220, 150, 255)],
    'orange': [(255, 150, 50), (255, 180, 100), (255, 210, 150)],
}

COLOR_NAMES = list(GRADIENT_COLORS.keys())

class Particle:
    def __init__(self, x, y, vx=None, vy=None, color_name=None, is_fountain=False):
        self.x = float(x)
        self.y = float(y)
        
        # Physics with more realistic distribution
        if is_fountain:
            # Fountain effect: particles shoot upward at angles
            angle = random.uniform(-math.pi / 2.5, -math.pi / 3.5)  # Upward angles
            speed = random.uniform(5, 12)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        elif vx is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 8)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        else:
            self.vx = vx
            self.vy = vy
        
        # Particle properties
        self.color_name = color_name or random.choice(COLOR_NAMES)
        self.color_gradient = GRADIENT_COLORS[self.color_name]
        self.mass = random.uniform(0.5, 2.0)
        self.size = max(2, int(self.mass * 3))
        self.max_size = self.size
        
        # Life and decay
        self.life = 300 + random.randint(-50, 50)
        self.max_life = self.life
        
        # Trail
        self.trail = []
        self.trail_max_length = 8
    
    def apply_forces(self):
        """Apply real-world physics forces"""
        # Gravity (F = ma)
        self.vy += GRAVITY * self.mass
        
        # Air resistance (drag force)
        self.vx *= AIR_RESISTANCE
        self.vy *= AIR_RESISTANCE
        
        # Terminal velocity check
        max_velocity = 20
        velocity = math.sqrt(self.vx**2 + self.vy**2)
        if velocity > max_velocity:
            scale = max_velocity / velocity
            self.vx *= scale
            self.vy *= scale
    
    def update(self):
        """Update particle position and physics"""
        # Store previous position for trail
        if len(self.trail) >= self.trail_max_length:
            self.trail.pop(0)
        self.trail.append((self.x, self.y))
        
        # Apply forces
        self.apply_forces()
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Wall collisions with energy loss
        if self.x <= self.size:
            self.x = self.size
            self.vx = abs(self.vx) * BOUNCE_DAMPING
        elif self.x >= WIDTH - self.size:
            self.x = WIDTH - self.size
            self.vx = -abs(self.vx) * BOUNCE_DAMPING
        
        # Floor collision
        if self.y >= FLOOR_HEIGHT - self.size:
            self.y = FLOOR_HEIGHT - self.size
            self.vy = -abs(self.vy) * BOUNCE_DAMPING * 0.7
            # Add slight friction on floor
            self.vx *= 0.95
        
        # Top collision
        if self.y <= self.size:
            self.y = self.size
            self.vy = abs(self.vy) * BOUNCE_DAMPING
        
        # Age and fade
        self.life -= 1
        life_ratio = self.life / self.max_life
        self.size = max(1, int(self.max_size * life_ratio))
    
    def calculate_shadow(self):
        """Calculate shadow position on floor based on light source"""
        lx, ly = LIGHT_POS
        
        # Ray from light through particle to floor
        if self.y < FLOOR_HEIGHT:
            # Simple projection: where does ray hit the floor
            dx = self.x - lx
            dy = self.y - ly
            
            # Avoid division by zero
            if abs(dy) > 0.1:
                t = (FLOOR_HEIGHT - ly) / dy
                shadow_x = lx + dx * t
                return shadow_x
        
        return self.x
    
    def draw(self, screen):
        """Draw particle with realistic lighting and shadows"""
        # Calculate color fade
        life_ratio = max(0, self.life / self.max_life)
        
        # Get color from gradient based on life
        gradient_index = int((1 - life_ratio) * (len(self.color_gradient) - 1))
        base_color = self.color_gradient[gradient_index]
        
        # Calculate real lighting at particle position
        light_intensity = calculate_light_at_point(self.x, self.y)
        
        # Apply light to particle color (brighten based on light intensity)
        lit_color = tuple(
            min(255, int(base_color[i] * (0.5 + light_intensity)))
            for i in range(3)
        )
        faded_color = tuple(int(c * life_ratio) for c in lit_color)
        
        # Draw realistic shadow based on light projection
        if self.y < FLOOR_HEIGHT:
            shadow_x = self.calculate_shadow()
            
            # Shadow intensity based on light
            light_at_floor = calculate_light_at_point(shadow_x, FLOOR_HEIGHT)
            height_ratio = (FLOOR_HEIGHT - self.y) / FLOOR_HEIGHT
            shadow_intensity = height_ratio * max(0, 1 - light_intensity) * life_ratio
            
            # Multi-layer soft shadow
            for shadow_layer in range(int(self.size * 2), 0, -1):
                layer_intensity = shadow_intensity * (1 - shadow_layer / (self.size * 2))
                shadow_color = tuple(int(c * layer_intensity * 0.3) for c in base_color)
                if layer_intensity > 0.02:
                    pygame.draw.circle(screen, shadow_color, (int(shadow_x), int(FLOOR_HEIGHT - 2)), shadow_layer)
        
        # Draw trail with lighting
        if len(self.trail) > 1:
            for i, (tx, ty) in enumerate(self.trail):
                trail_light = calculate_light_at_point(tx, ty)
                trail_alpha = (i / len(self.trail)) * life_ratio
                trail_size = max(1, int(self.size * trail_alpha))
                trail_base = tuple(int(c * (0.3 + trail_light * 0.4)) for c in base_color)
                trail_color = tuple(int(c * trail_alpha * 0.5) for c in trail_base)
                if trail_size > 0:
                    pygame.draw.circle(screen, trail_color, (int(tx), int(ty)), trail_size)
        
        # Draw glow effect based on lighting
        if self.size > 1:
            glow_intensity = 0.2 + light_intensity * 0.3
            glow_color = tuple(int(c * glow_intensity * life_ratio) for c in base_color)
            pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), 
                             int(self.size * 2), 2)
        
        # Draw main particle
        if self.size > 0:
            pygame.draw.circle(screen, faded_color, (int(self.x), int(self.y)), self.size)
    
    def is_alive(self):
        return self.life > 0

def draw_background(screen):
    """Draw gradient background"""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = (
            int(BG_COLOR_TOP[0] + (BG_COLOR_BOTTOM[0] - BG_COLOR_TOP[0]) * ratio),
            int(BG_COLOR_TOP[1] + (BG_COLOR_BOTTOM[1] - BG_COLOR_TOP[1]) * ratio),
            int(BG_COLOR_TOP[2] + (BG_COLOR_BOTTOM[2] - BG_COLOR_TOP[2]) * ratio)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def calculate_light_at_point(x, y):
    """Calculate light intensity at a specific point using inverse square law"""
    lx, ly = LIGHT_POS
    dx = x - lx
    dy = y - ly
    distance = max(1, math.sqrt(dx**2 + dy**2))
    
    # Inverse square law: intensity = 1 / distance^2
    intensity = 1.0 / (1 + (distance / 100) ** 2)
    return intensity

def draw_volumetric_rays(screen):
    """Draw volumetric light rays (crepuscular rays) for realistic lighting"""
    lx, ly = LIGHT_POS
    
    # Create multiple layers of rays with different patterns
    num_primary_rays = 32
    
    for layer in range(3):
        layer_variation = layer * 0.3
        
        for i in range(num_primary_rays):
            angle = (i / num_primary_rays) * 2 * math.pi + layer_variation
            
            # Ray origin slightly offset from light center
            ray_start_x = lx + math.cos(angle) * (5 + layer * 2)
            ray_start_y = ly + math.sin(angle) * (5 + layer * 2)
            
            # Ray with perpendicular spread for volumetric effect
            spread_angle = angle + math.pi / 2 + random.uniform(-0.3, 0.3)
            ray_length = 800
            
            ray_end_x = lx + math.cos(angle) * ray_length
            ray_end_y = ly + math.sin(angle) * ray_length
            
            # Calculate gradient falloff
            gradient_steps = 50
            for step in range(gradient_steps):
                progress = step / gradient_steps
                current_x = ray_start_x + (ray_end_x - ray_start_x) * progress
                current_y = ray_start_y + (ray_end_y - ray_start_y) * progress
                
                # Skip if outside screen
                if current_y > FLOOR_HEIGHT:
                    break
                
                # Brightness decreases along the ray
                brightness = (1 - progress) * (1 - layer * 0.3) * 0.08
                
                ray_color = (
                    int(LIGHT_COLOR[0] * brightness),
                    int(LIGHT_COLOR[1] * brightness * 0.9),
                    int(LIGHT_COLOR[2] * brightness * 0.6)
                )
                
                # Draw small segment
                next_x = ray_start_x + (ray_end_x - ray_start_x) * (step + 1) / gradient_steps
                next_y = ray_start_y + (ray_end_y - ray_start_y) * (step + 1) / gradient_steps
                
                if ray_color[0] > 5 or ray_color[1] > 5:
                    pygame.draw.line(screen, ray_color, (current_x, current_y), (next_x, next_y), 2)

def draw_light_source(screen):
    """Draw realistic light source with proper illumination"""
    lx, ly = LIGHT_POS
    
    # Draw light bloom/halo with proper gradients
    bloom_layers = 80
    for radius in range(bloom_layers, 0, -1):
        # Quadratic falloff for more realistic bloom
        intensity = (1 - (radius / bloom_layers)) ** 2
        
        bloom_color = (
            int(LIGHT_COLOR[0] * intensity * 0.5),
            int(LIGHT_COLOR[1] * intensity * 0.4),
            int(LIGHT_COLOR[2] * intensity * 0.2)
        )
        
        if intensity > 0.01:
            pygame.draw.circle(screen, bloom_color, (lx, ly), radius, 1)
    
    # Draw light source core
    pygame.draw.circle(screen, LIGHT_COLOR, (lx, ly), 15)
    pygame.draw.circle(screen, (255, 255, 255), (lx, ly), 10)
    pygame.draw.circle(screen, (255, 250, 230), (lx, ly), 5)

def draw_floor_with_light(screen):
    """Draw floor with proper lighting response and fountain base"""
    # Main floor with lighting gradient
    for x in range(0, WIDTH, 10):
        light_intensity = calculate_light_at_point(x, FLOOR_HEIGHT)
        brightness = 0.4 + light_intensity * 0.6
        
        floor_color = (
            int(FLOOR_COLOR[0] * brightness),
            int(FLOOR_COLOR[1] * brightness),
            int(FLOOR_COLOR[2] * brightness)
        )
        pygame.draw.line(screen, floor_color, (x, FLOOR_HEIGHT), (x + 10, FLOOR_HEIGHT), 
                        int(HEIGHT - FLOOR_HEIGHT))
    
    # Floor accent line with lighting
    for x in range(0, WIDTH, 5):
        light_intensity = calculate_light_at_point(x, FLOOR_HEIGHT)
        brightness = 0.5 + light_intensity * 0.8
        accent_color = (
            int(FLOOR_ACCENT[0] * brightness),
            int(FLOOR_ACCENT[1] * brightness),
            int(FLOOR_ACCENT[2] * brightness)
        )
        pygame.draw.line(screen, accent_color, (x, FLOOR_HEIGHT), (x + 5, FLOOR_HEIGHT), 4)
    
    # Draw fountain base
    fountain_x = WIDTH // 2
    fountain_radius = 40
    
    # Fountain basin (stone-like)
    light_intensity = calculate_light_at_point(fountain_x, FLOOR_HEIGHT)
    basin_brightness = 0.4 + light_intensity * 0.6
    basin_color = (
        int(100 * basin_brightness),
        int(110 * basin_brightness),
        int(130 * basin_brightness)
    )
    
    pygame.draw.circle(screen, basin_color, (fountain_x, int(FLOOR_HEIGHT - 5)), fountain_radius, 3)
    pygame.draw.circle(screen, basin_color, (fountain_x, int(FLOOR_HEIGHT)), fountain_radius - 10, 2)
    
    # Fountain nozzle
    nozzle_color = (
        int(150 * basin_brightness),
        int(150 * basin_brightness),
        int(160 * basin_brightness)
    )
    pygame.draw.circle(screen, nozzle_color, (fountain_x, int(FLOOR_HEIGHT - 8)), 8)
    pygame.draw.circle(screen, (180, 180, 200), (fountain_x, int(FLOOR_HEIGHT - 8)), 5)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Advanced Particle System - Physics Engine with Lighting")
    clock = pygame.time.Clock()
    
    particles = []
    running = True
    paused = False
    show_info = True
    
    while running:
        clock.tick(FPS)
        dt = clock.get_time() / 1000.0
        
        # Update light position to follow mouse (optional)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Uncomment to make light follow mouse:
        # LIGHT_POS = (mouse_x, mouse_y)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Create particles on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                color = random.choice(COLOR_NAMES)
                for _ in range(30):
                    particles.append(Particle(mouse_x, mouse_y, color_name=color))
            
            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_i:
                    show_info = not show_info
                if event.key == pygame.K_c:
                    particles.clear()
        
        # Continuous fountain particle generation from floor
        if not paused:
            fountain_x, fountain_y = WIDTH // 2, FLOOR_HEIGHT - 10
            if random.random() < 0.6 and len(particles) < NUM_PARTICLES:
                color = random.choice(COLOR_NAMES)
                particles.append(Particle(fountain_x, fountain_y, color_name=color, is_fountain=True))
        
        # Update particles
        if not paused:
            for particle in particles:
                particle.update()
            
            # Particle-to-particle interaction (optional gravity wells)
            if len(particles) > 50 and random.random() < 0.1:
                # Simple attractive force between nearby particles
                for i, p1 in enumerate(particles):
                    if i % 10 == 0 and len(particles) > i + 1:
                        p2 = particles[random.randint(i + 1, min(len(particles) - 1, i + 20))]
                        dx = p2.x - p1.x
                        dy = p2.y - p1.y
                        dist = math.sqrt(dx**2 + dy**2)
                        if dist > 1 and dist < 150:
                            force = 0.0002 * p1.mass * p2.mass / (dist + 1)
                            p1.vx += (dx / dist) * force
                            p1.vy += (dy / dist) * force
        
        # Remove dead particles
        particles = [p for p in particles if p.is_alive()]
        
        # Drawing
        draw_background(screen)
        draw_floor_with_light(screen)
        draw_volumetric_rays(screen)
        
        # Draw particles
        for particle in particles:
            particle.draw(screen)
        
        # Draw light source last (on top)
        draw_light_source(screen)
        
        # Draw UI
        font_small = pygame.font.Font(None, 18)
        font_large = pygame.font.Font(None, 28)
        
        if show_info:
            info_texts = [
                f"Particles: {len(particles)}/{NUM_PARTICLES}",
                f"FPS: {int(clock.get_fps())}",
                "Click to create burst | SPACE to pause | I to hide info | C to clear"
            ]
            
            for i, text_str in enumerate(info_texts):
                text = font_small.render(text_str, True, (200, 220, 255))
                screen.blit(text, (15, 15 + i * 25))
        
        if paused:
            pause_text = font_large.render("PAUSED (SPACE to resume)", True, (255, 100, 100))
            screen.blit(pause_text, (WIDTH // 2 - 200, HEIGHT // 2 - 25))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
