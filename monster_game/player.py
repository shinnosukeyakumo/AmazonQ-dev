import pygame
import json
import os
from monster import Monster

class Player:
    def __init__(self, name="Trainer"):
        self.name = name
        self.x = 400  # Initial position X
        self.y = 300  # Initial position Y
        self.size = 40  # Player size
        self.speed = 5  # Movement speed
        self.direction = "down"  # Direction (up, down, left, right)
        self.moving = False  # Whether moving
        self.step_count = 0  # Step counter
        
        self.monsters = []  # Owned monsters
        self.active_monster = 0  # Lead monster
        
        self.items = {
            "monster_ball": 5,  # Monster Ball
            "potion": 3,        # Potion
            "full_restore": 1   # Full Restore
        }
        
        self.money = 1000  # Money
        self.badges = []  # Badges
        
        self.discovered_monsters = set()  # Monsters registered in encyclopedia
    
    def update(self, keys, map_width, map_height):
        """プレイヤーの更新処理"""
        old_x, old_y = self.x, self.y
        self.moving = False
        
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"
            self.moving = True
        elif keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = "up"
            self.moving = True
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = "down"
            self.moving = True
        
        # 画面外に出ないように
        self.x = max(0, min(map_width - self.size, self.x))
        self.y = max(0, min(map_height - self.size, self.y))
        
        # 移動していたら歩数カウント増加
        if self.moving and (old_x != self.x or old_y != self.y):
            self.step_count += 1
    
    def draw(self, screen):
        """プレイヤーの描画"""
        # 簡易的な描画（後で画像に置き換え）
        color = (0, 0, 255)  # 青色
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))
        
        # 向きを示す三角形
        if self.direction == "up":
            points = [(self.x + self.size//2, self.y), 
                     (self.x, self.y + self.size//2), 
                     (self.x + self.size, self.y + self.size//2)]
        elif self.direction == "down":
            points = [(self.x + self.size//2, self.y + self.size), 
                     (self.x, self.y + self.size//2), 
                     (self.x + self.size, self.y + self.size//2)]
        elif self.direction == "left":
            points = [(self.x, self.y + self.size//2), 
                     (self.x + self.size//2, self.y), 
                     (self.x + self.size//2, self.y + self.size)]
        elif self.direction == "right":
            points = [(self.x + self.size, self.y + self.size//2), 
                     (self.x + self.size//2, self.y), 
                     (self.x + self.size//2, self.y + self.size)]
        
        pygame.draw.polygon(screen, (255, 255, 0), points)
    
    def add_monster(self, monster):
        """モンスターを追加"""
        if len(self.monsters) < 6:  # 最大6体まで
            # 野生モンスターの場合はフラグを変更
            monster.is_wild = False
            self.monsters.append(monster)
            
            # 図鑑に登録
            self.discovered_monsters.add(monster.species_id)
            return True
        return False
    
    def get_active_monster(self):
        """現在の先頭モンスターを取得"""
        if self.monsters and len(self.monsters) > self.active_monster:
            return self.monsters[self.active_monster]
        return None
    
    def switch_monster(self, index):
        """モンスターの順番を入れ替え"""
        if 0 <= index < len(self.monsters):
            self.active_monster = index
            return True
        return False
    
    def use_item(self, item_name, target_monster=None):
        """Use an item"""
        if item_name not in self.items or self.items[item_name] <= 0:
            return False, f"You don't have any {item_name}!"
        
        result = ""
        success = False
        
        if item_name == "potion" and target_monster:
            # Potion (recover 20 HP)
            old_hp = target_monster.current_hp
            target_monster.heal(20)
            heal_amount = target_monster.current_hp - old_hp
            result = f"{target_monster.name} recovered {heal_amount} HP!"
            success = True
        
        elif item_name == "full_restore" and target_monster:
            # Full Restore (recover all HP and status)
            old_hp = target_monster.current_hp
            target_monster.heal()
            heal_amount = target_monster.current_hp - old_hp
            result = f"{target_monster.name} recovered {heal_amount} HP! Status conditions were cured!"
            success = True
        
        # If successful, reduce item count
        if success:
            self.items[item_name] -= 1
        
        return success, result
    
    def can_encounter(self):
        """エンカウント判定（10歩ごとに判定）"""
        return self.moving and self.step_count % 10 == 0
    
    def save_game(self, filename="save_data.json"):
        """ゲームデータをセーブ"""
        save_data = {
            "player_name": self.name,
            "position": {"x": self.x, "y": self.y},
            "money": self.money,
            "items": self.items,
            "badges": self.badges,
            "discovered_monsters": list(self.discovered_monsters),
            "monsters": [monster.to_dict() for monster in self.monsters],
            "active_monster": self.active_monster
        }
        
        try:
            with open(os.path.join(os.path.dirname(__file__), filename), 'w') as f:
                json.dump(save_data, f)
            return True
        except Exception as e:
            print(f"セーブエラー: {e}")
            return False
    
    @classmethod
    def load_game(cls, filename="save_data.json"):
        """ゲームデータをロード"""
        try:
            with open(os.path.join(os.path.dirname(__file__), filename), 'r') as f:
                save_data = json.load(f)
            
            player = cls(save_data["player_name"])
            player.x = save_data["position"]["x"]
            player.y = save_data["position"]["y"]
            player.money = save_data["money"]
            player.items = save_data["items"]
            player.badges = save_data["badges"]
            player.discovered_monsters = set(save_data["discovered_monsters"])
            
            # モンスターの復元
            for monster_data in save_data["monsters"]:
                monster = Monster.from_dict(monster_data)
                player.monsters.append(monster)
            
            player.active_monster = save_data["active_monster"]
            
            return player
        except Exception as e:
            print(f"ロードエラー: {e}")
            return None
