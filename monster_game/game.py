import pygame
import sys
import random
from monster import Monster, generate_wild_monster
from player import Player
from battle import Battle
from map import GameMap

# Initialize the game
pygame.init()
pygame.font.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Collection Game")

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Game states
TITLE = "title"
WORLD_MAP = "world_map"
BATTLE = "battle"
MONSTER_MENU = "monster_menu"
POKEDEX = "pokedex"
ITEM_MENU = "item_menu"
EVOLUTION = "evolution"

# Game class
class Game:
    def __init__(self):
        self.state = TITLE
        self.player = Player("Trainer")
        self.map = GameMap(WIDTH, HEIGHT)
        self.battle = None
        self.menu_selection = 0
        
        # Add initial monster
        starter = Monster(1, 5)  # Embery Lv.5
        self.player.add_monster(starter)
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        if self.state == TITLE:
            # Title screen update
            pass
        
        elif self.state == WORLD_MAP:
            # Update player
            self.player.update(keys, WIDTH, HEIGHT)
            
            # Random encounter
            if self.player.can_encounter() and random.random() < 0.3:  # 30% chance for encounter
                area = self.map.get_area_at_position(self.player.x, self.player.y)
                wild_monster = generate_wild_monster(area)
                self.start_battle(wild_monster)
        
        elif self.state == BATTLE:
            # Battle update
            if self.battle.state == "end":
                if self.battle.result == "win":
                    # Victory processing
                    self.state = WORLD_MAP
                elif self.battle.result == "lose":
                    # Defeat processing (return to center, etc.)
                    self.state = WORLD_MAP
                    # Heal all monsters
                    for monster in self.player.monsters:
                        monster.heal()
                elif self.battle.result == "run" or self.battle.result == "catch":
                    # Run or catch
                    self.state = WORLD_MAP
        
        elif self.state == MONSTER_MENU:
            # Monster menu update
            pass
        
        elif self.state == POKEDEX:
            # Pokedex update
            pass
        
        elif self.state == ITEM_MENU:
            # Item menu update
            pass
        
        elif self.state == EVOLUTION:
            # Evolution update
            pass
    
    def handle_event(self, event):
        """Event handling"""
        if event.type == pygame.KEYDOWN:
            if self.state == TITLE:
                if event.key == pygame.K_RETURN:
                    self.state = WORLD_MAP
            
            elif self.state == WORLD_MAP:
                if event.key == pygame.K_m:
                    self.state = MONSTER_MENU
                elif event.key == pygame.K_p:
                    self.state = POKEDEX
                elif event.key == pygame.K_i:
                    self.state = ITEM_MENU
                elif event.key == pygame.K_s:
                    self.player.save_game()
                elif event.key == pygame.K_l:
                    loaded_player = Player.load_game()
                    if loaded_player:
                        self.player = loaded_player
            
            elif self.state == BATTLE:
                if self.battle.state == "player_turn":
                    if event.key == pygame.K_UP:
                        self.battle.update("menu_select", (self.battle.menu_selection - 2) % 4)
                    elif event.key == pygame.K_DOWN:
                        self.battle.update("menu_select", (self.battle.menu_selection + 2) % 4)
                    elif event.key == pygame.K_LEFT:
                        self.battle.update("menu_select", (self.battle.menu_selection - 1) % 4)
                    elif event.key == pygame.K_RIGHT:
                        self.battle.update("menu_select", (self.battle.menu_selection + 1) % 4)
                    elif event.key == pygame.K_RETURN:
                        self.battle.update("menu_confirm")
                
                elif self.battle.state == "move_select":
                    if event.key == pygame.K_UP:
                        self.battle.update("menu_select", (self.battle.move_selection - 2) % len(self.player.get_active_monster().moves))
                    elif event.key == pygame.K_DOWN:
                        self.battle.update("menu_select", (self.battle.move_selection + 2) % len(self.player.get_active_monster().moves))
                    elif event.key == pygame.K_LEFT:
                        self.battle.update("menu_select", (self.battle.move_selection - 1) % len(self.player.get_active_monster().moves))
                    elif event.key == pygame.K_RIGHT:
                        self.battle.update("menu_select", (self.battle.move_selection + 1) % len(self.player.get_active_monster().moves))
                    elif event.key == pygame.K_RETURN:
                        self.battle.update("menu_confirm")
                    elif event.key == pygame.K_ESCAPE:
                        self.battle.update("menu_cancel")
                
                elif self.battle.state == "start":
                    if event.key == pygame.K_RETURN:
                        self.battle.update()
                
                elif self.battle.state == "enemy_turn":
                    if event.key == pygame.K_RETURN:
                        self.battle.update()
            
            elif self.state == MONSTER_MENU:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    self.state = WORLD_MAP
            
            elif self.state == POKEDEX:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    self.state = WORLD_MAP
            
            elif self.state == ITEM_MENU:
                if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                    self.state = WORLD_MAP
    
    def start_battle(self, wild_monster):
        """Start battle"""
        self.state = BATTLE
        self.battle = Battle(self.player, wild_monster)
    
    def draw(self):
        """Screen drawing"""
        screen.fill(WHITE)
        
        if self.state == TITLE:
            self.draw_title()
        elif self.state == WORLD_MAP:
            self.draw_world_map()
        elif self.state == BATTLE:
            self.battle.draw(screen, font, small_font)
        elif self.state == MONSTER_MENU:
            self.draw_monster_menu()
        elif self.state == POKEDEX:
            self.draw_pokedex()
        elif self.state == ITEM_MENU:
            self.draw_item_menu()
        elif self.state == EVOLUTION:
            self.draw_evolution()
    
    def draw_title(self):
        """Draw title screen"""
        title = font.render("Monster Collection Game", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 150, HEIGHT // 3))
        
        start = font.render("Press ENTER to Start", True, BLACK)
        screen.blit(start, (WIDTH // 2 - 100, HEIGHT // 2))
    
    def draw_world_map(self):
        """Draw world map"""
        # Draw map
        self.map.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Instructions
        instructions = small_font.render("Arrow Keys: Move  M: Monsters  P: Pokedex  I: Items  S: Save  L: Load", True, BLACK)
        screen.blit(instructions, (10, HEIGHT - 30))
    
    def draw_monster_menu(self):
        """Draw monster menu"""
        screen.fill((230, 230, 255))
        title = font.render("Monster List", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 100, 20))
        
        for i, monster in enumerate(self.player.monsters):
            y_pos = 80 + i * 100
            
            # Monster frame
            pygame.draw.rect(screen, WHITE, (50, y_pos, WIDTH - 100, 80))
            pygame.draw.rect(screen, BLACK, (50, y_pos, WIDTH - 100, 80), 2)
            
            # Monster display (simple rectangle)
            pygame.draw.rect(screen, BLUE, (70, y_pos + 10, 60, 60))
            
            # Monster info
            name = font.render(monster.name, True, BLACK)
            screen.blit(name, (150, y_pos + 10))
            
            type_text = small_font.render(f"Type: {'/'.join(monster.type)}", True, BLACK)
            screen.blit(type_text, (150, y_pos + 40))
            
            hp_text = small_font.render(f"HP: {monster.current_hp}/{monster.max_hp}", True, BLACK)
            screen.blit(hp_text, (300, y_pos + 10))
            
            level_text = small_font.render(f"Level: {monster.level}", True, BLACK)
            screen.blit(level_text, (300, y_pos + 40))
            
            # Move info
            moves_text = small_font.render(f"Moves: {', '.join([m['name'] for m in monster.moves])}", True, BLACK)
            screen.blit(moves_text, (450, y_pos + 10))
        
        # Back button
        back_text = font.render("Back (B)", True, BLACK)
        screen.blit(back_text, (WIDTH - 150, HEIGHT - 50))
    
    def draw_pokedex(self):
        """Draw pokedex"""
        screen.fill((255, 230, 230))
        title = font.render("Monster Encyclopedia", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 100, 20))
        
        # Display discovered monsters
        from monster_data import MONSTER_SPECIES
        
        y_pos = 80
        for species_id in sorted(self.player.discovered_monsters):
            if species_id in MONSTER_SPECIES:
                species_data = MONSTER_SPECIES[species_id]
                name = species_data[0]
                type_str = species_data[1]
                
                entry = font.render(f"No.{species_id}: {name} ({type_str} type)", True, BLACK)
                screen.blit(entry, (100, y_pos))
                y_pos += 40
        
        # Back button
        back_text = font.render("Back (B)", True, BLACK)
        screen.blit(back_text, (WIDTH - 150, HEIGHT - 50))
    
    def draw_item_menu(self):
        """Draw item menu"""
        screen.fill((230, 255, 230))
        title = font.render("Items", True, BLACK)
        screen.blit(title, (WIDTH // 2 - 50, 20))
        
        # Item list
        item_names = {
            "monster_ball": "Monster Ball",
            "potion": "Potion",
            "full_restore": "Full Restore"
        }
        
        y_pos = 80
        for item_id, count in self.player.items.items():
            if count > 0:
                name = item_names.get(item_id, item_id)
                item_text = font.render(f"{name} x {count}", True, BLACK)
                screen.blit(item_text, (100, y_pos))
                y_pos += 40
        
        # Back button
        back_text = font.render("Back (B)", True, BLACK)
        screen.blit(back_text, (WIDTH - 150, HEIGHT - 50))
    
    def draw_evolution(self):
        """Draw evolution screen"""
        screen.fill(BLACK)
        
        # Pre-evolution monster
        pygame.draw.rect(screen, BLUE, (200, 250, 100, 100))
        
        # Arrow
        pygame.draw.polygon(screen, WHITE, [(350, 300), (400, 250), (400, 350)])
        
        # Post-evolution monster
        pygame.draw.rect(screen, RED, (450, 250, 100, 100))
        
        # Text
        evolving_text = font.render("Evolving...", True, WHITE)
        screen.blit(evolving_text, (WIDTH // 2 - 50, 400))

# Main game loop
def main():
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Draw
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
