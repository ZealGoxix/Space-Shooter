# space_shooter.py
import pgzrun
from random import randint

# Game window setup
WIDTH = 800
HEIGHT = 600
TITLE = "Python Space Shooter"

# Game objects
player = Actor('player', (WIDTH // 2, HEIGHT - 50))
player.speed = 5

asteroids = []
bullets = []

# Score and game state
score = 0
game_active = True  # NEW: Track if game is running

# Core game functions
def draw():
    """Draws everything on screen"""
    screen.clear()
    screen.blit('space_background', (0, 0))
    player.draw()
    
    for asteroid in asteroids:
        asteroid.draw()
    
    for bullet in bullets:
        bullet.draw()
    
    # Display score
    screen.draw.text(f"Score: {score}", (15, 15), fontsize=30, color='white')
    
    # NEW: Show game over message
    if not game_active:
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), 
                        fontsize=60, color='red')
        screen.draw.text(f"Final Score: {score}", center=(WIDTH//2, HEIGHT//2 + 50), 
                        fontsize=40, color='white')
        screen.draw.text("Press R to restart", center=(WIDTH//2, HEIGHT//2 + 100), 
                        fontsize=30, color='yellow')

def update():
    """Updates game state"""
    global score, game_active
    
    # NEW: Only update if game is active
    if not game_active:
        return
    
    # Player movement
    if keyboard.left and player.left > 0:
        player.x -= player.speed
    if keyboard.right and player.right < WIDTH:
        player.x += player.speed
    
    # Update asteroids
    for asteroid in asteroids[:]:  # Create copy to safely remove items
        asteroid.y += 2
        
        # Remove if off screen
        if asteroid.top > HEIGHT:
            asteroids.remove(asteroid)
            continue  # Skip collision check
        
        # Collision with player
        if asteroid.colliderect(player):
            print("Game Over! Final Score:", score)
            game_active = False  # NEW: Stop the game
            return  # Exit update immediately
    
    # Update bullets
    for bullet in bullets[:]:  # Create copy to safely remove items
        bullet.y -= 5
        
        if bullet.bottom < 0:
            bullets.remove(bullet)
            continue
        
        # Check bullet-asteroid collision
        for asteroid in asteroids[:]:
            if bullet.colliderect(asteroid):
                if bullet in bullets:  # Safety check
                    bullets.remove(bullet)
                if asteroid in asteroids:  # Safety check
                    asteroids.remove(asteroid)
                score += 10
                break

def on_key_down(key):
    """Handles key presses"""
    global game_active, score  # NEW: Added globals
    
    if key == keys.SPACE and game_active:
        # Create a new bullet at player position
        bullet = Actor('bullet', (player.x, player.top))
        bullets.append(bullet)
    
    # NEW: Restart game with R key
    elif key == keys.R and not game_active:
        reset_game()
        game_active = True

def create_asteroid():
    """Creates a new asteroid at random position"""
    # NEW: Only create if game is active
    if game_active:
        asteroid = Actor('asteroid', (randint(40, WIDTH-40), -40))
        asteroids.append(asteroid)

def reset_game():
    """Resets the game"""
    global score
    score = 0
    asteroids.clear()
    bullets.clear()
    player.pos = (WIDTH // 2, HEIGHT - 50)

# Create asteroids every 1.5 seconds (but only if game is active)
clock.schedule_interval(create_asteroid, 1.5)

# Run the game
pgzrun.go()