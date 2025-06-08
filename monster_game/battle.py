import random
import pygame
from monster import Monster

class Battle:
    def __init__(self, player, wild_monster=None, trainer=None):
        self.player = player
        self.wild_monster = wild_monster
        self.trainer = trainer  # For trainer battles (not implemented yet)
        
        self.player_monster = player.get_active_monster()
        self.enemy_monster = wild_monster if wild_monster else trainer.get_active_monster()
        
        self.state = "start"  # start, player_turn, enemy_turn, catch, run, end
        self.message = f"A wild {self.enemy_monster.name} appeared!"
        self.animation_frame = 0
        
        # Move selection index
        self.move_selection = 0
        self.menu_selection = 0  # 0: Fight, 1: Monster, 2: Item, 3: Run
        
        # Battle result
        self.result = None  # win, lose, catch, run
        
        # Experience gain
        self.exp_gain = 0
    
    def update(self, action=None, selection=None):
        """Update battle state"""
        if self.state == "start":
            self.state = "player_turn"
            self.message = "What will you do?"
            return
        
        elif self.state == "player_turn":
            if action == "menu_select":
                self.menu_selection = selection % 4
                return
            
            elif action == "menu_confirm":
                if self.menu_selection == 0:  # Fight
                    self.state = "move_select"
                    self.message = "Choose a move"
                    return
                
                elif self.menu_selection == 1:  # Monster
                    self.state = "monster_select"
                    self.message = "Choose a monster"
                    return
                
                elif self.menu_selection == 2:  # Item
                    self.state = "item_select"
                    self.message = "Choose an item"
                    return
                
                elif self.menu_selection == 3:  # Run
                    # Run processing
                    escape_chance = 0.7  # 70% chance to escape
                    if random.random() < escape_chance:
                        self.state = "end"
                        self.result = "run"
                        self.message = "Got away safely!"
                    else:
                        self.state = "enemy_turn"
                        self.message = "Can't escape!"
                    return
        
        elif self.state == "move_select":
            if action == "menu_select":
                self.move_selection = selection % len(self.player_monster.moves)
                return
            
            elif action == "menu_confirm":
                # Use move
                if self.move_selection < len(self.player_monster.moves):
                    result = self.player_monster.use_move(self.move_selection, self.enemy_monster)
                    self.message = result
                    self.state = "enemy_turn"
                    
                    # Check if enemy HP is 0
                    if self.enemy_monster.current_hp <= 0:
                        self.handle_enemy_faint()
                    return
                
            elif action == "menu_cancel":
                self.state = "player_turn"
                self.message = "What will you do?"
                return
        
        elif self.state == "monster_select":
            if action == "menu_select":
                # Monster selection processing
                pass
            
            elif action == "menu_confirm":
                # Monster switch processing
                pass
            
            elif action == "menu_cancel":
                self.state = "player_turn"
                self.message = "What will you do?"
                return
        
        elif self.state == "item_select":
            if action == "menu_select":
                # Item selection processing
                pass
            
            elif action == "menu_confirm":
                # Item use processing (e.g., Monster Ball)
                if selection == 0:  # Monster Ball
                    self.state = "catch"
                    self.try_catch_monster()
                    return
            
            elif action == "menu_cancel":
                self.state = "player_turn"
                self.message = "What will you do?"
                return
        
        elif self.state == "enemy_turn":
            # Enemy action
            if self.enemy_monster.current_hp > 0:
                # Select random move
                enemy_move = random.randint(0, len(self.enemy_monster.moves) - 1)
                result = self.enemy_monster.use_move(enemy_move, self.player_monster)
                self.message = result
                
                # Check if player HP is 0
                if self.player_monster.current_hp <= 0:
                    self.handle_player_faint()
                else:
                    self.state = "player_turn"
                    self.message = "What will you do?"
            else:
                self.state = "player_turn"
                self.message = "What will you do?"
            return
        
        elif self.state == "catch":
            # Catch processing is done in try_catch_monster
            pass
        
        elif self.state == "end":
            # Battle end
            pass
    
    def handle_enemy_faint(self):
        """Handle enemy monster fainting"""
        self.message = f"{self.enemy_monster.name} fainted!"
        
        # Calculate experience
        self.exp_gain = self.calculate_exp_gain()
        
        # Gain experience
        level_up, levels = self.player_monster.gain_exp(self.exp_gain)
        
        if level_up:
            self.message += f" {self.player_monster.name} gained {levels} level(s)!"
            
            # Check evolution
            can_evolve, _ = self.player_monster.can_evolve()
            if can_evolve:
                self.state = "evolution"
                return
        
        self.state = "end"
        self.result = "win"
    
    def handle_player_faint(self):
        """Handle player monster fainting"""
        self.message = f"{self.player_monster.name} fainted!"
        
        # Check if other monsters are available
        healthy_monsters = [m for m in self.player.monsters if m.current_hp > 0]
        
        if healthy_monsters:
            self.state = "monster_select"
            self.message += " Choose your next monster."
        else:
            self.state = "end"
            self.result = "lose"
            self.message += " All your monsters have fainted!"
    
    def try_catch_monster(self):
        """Try to catch monster"""
        # Only wild monsters can be caught
        if not self.wild_monster:
            self.message = "Can't catch this monster!"
            self.state = "player_turn"
            return
        
        # Calculate catch rate (bonus varies by ball type)
        ball_bonus = 1.0  # Normal monster ball
        catch_rate = self.enemy_monster.get_catch_rate(ball_bonus)
        
        # Catch determination
        if random.random() < catch_rate:
            self.message = f"Caught {self.enemy_monster.name}!"
            self.player.add_monster(self.enemy_monster)
            self.state = "end"
            self.result = "catch"
        else:
            self.message = f"{self.enemy_monster.name} broke free!"
            self.state = "enemy_turn"
    
    def calculate_exp_gain(self):
        """Calculate experience gain"""
        # Base experience (proportional to enemy level)
        base_exp = self.enemy_monster.level * 3
        
        # Bonus (e.g., 1.5x for trainer battles)
        bonus = 1.0
        
        return int(base_exp * bonus)
    
    def draw(self, screen, font, small_font):
        """Draw battle screen"""
        # Battle screen background
        pygame.draw.rect(screen, (200, 230, 255), (0, 0, 800, 600))
        
        # Enemy monster
        pygame.draw.rect(screen, (255, 0, 0), (600, 100, 100, 100))
        monster_name = font.render(self.enemy_monster.name, True, (0, 0, 0))
        screen.blit(monster_name, (600, 70))
        
        # HP display
        hp_text = small_font.render(f"HP: {self.enemy_monster.current_hp}/{self.enemy_monster.max_hp}", True, (0, 0, 0))
        screen.blit(hp_text, (600, 210))
        
        # Player monster
        pygame.draw.rect(screen, (0, 0, 255), (100, 300, 100, 100))
        player_monster_name = font.render(self.player_monster.name, True, (0, 0, 0))
        screen.blit(player_monster_name, (100, 270))
        
        # HP display
        player_hp_text = small_font.render(f"HP: {self.player_monster.current_hp}/{self.player_monster.max_hp}", True, (0, 0, 0))
        screen.blit(player_hp_text, (100, 410))
        
        # Battle text
        text_box = pygame.Rect(50, 450, 700, 100)
        pygame.draw.rect(screen, (255, 255, 255), text_box)
        pygame.draw.rect(screen, (0, 0, 0), text_box, 2)
        
        battle_text = font.render(self.message, True, (0, 0, 0))
        screen.blit(battle_text, (60, 460))
        
        # Commands
        if self.state == "player_turn":
            commands = ["Fight", "Monster", "Item", "Run"]
            for i, cmd in enumerate(commands):
                cmd_x = 60 + (i % 2) * 200
                cmd_y = 500 + (i // 2) * 40
                
                # Highlight selected command
                color = (255, 0, 0) if i == self.menu_selection else (0, 0, 0)
                cmd_text = font.render(cmd, True, color)
                screen.blit(cmd_text, (cmd_x, cmd_y))
        
        # Move selection
        elif self.state == "move_select":
            for i, move in enumerate(self.player_monster.moves):
                move_x = 60 + (i % 2) * 200
                move_y = 500 + (i // 2) * 40
                
                # Highlight selected move
                color = (255, 0, 0) if i == self.move_selection else (0, 0, 0)
                move_text = font.render(move['name'], True, color)
                screen.blit(move_text, (move_x, move_y))
                
                # PP display
                pp_text = small_font.render(f"PP: {move['current_pp']}/{move['pp']}", True, (0, 0, 0))
                screen.blit(pp_text, (move_x + 150, move_y + 5))
        
        # Item selection
        elif self.state == "item_select":
            items = ["Monster Ball", "Potion", "Full Restore"]
            for i, item in enumerate(items):
                item_x = 60 + (i % 2) * 200
                item_y = 500 + (i // 2) * 40
                
                # Highlight selected item
                color = (255, 0, 0) if i == self.menu_selection else (0, 0, 0)
                item_text = font.render(item, True, color)
                screen.blit(item_text, (item_x, item_y))
        
        # Monster selection
        elif self.state == "monster_select":
            for i, monster in enumerate(self.player.monsters):
                if i < 4:  # Maximum 4 displayed
                    monster_x = 60 + (i % 2) * 350
                    monster_y = 500 + (i // 2) * 40
                    
                    # Highlight selected monster
                    color = (255, 0, 0) if i == self.menu_selection else (0, 0, 0)
                    monster_text = font.render(f"{monster.name} (HP: {monster.current_hp}/{monster.max_hp})", True, color)
                    screen.blit(monster_text, (monster_x, monster_y))
