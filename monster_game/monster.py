import random
from monster_data import MONSTER_SPECIES, MOVES, TYPE_CHART, LEARNABLE_MOVES

class Monster:
    def __init__(self, species_id, level=5, is_wild=False):
        # 種族データの取得
        species_data = MONSTER_SPECIES.get(species_id)
        if not species_data:
            raise ValueError(f"Invalid species ID: {species_id}")
        
        self.species_id = species_id
        self.name = species_data[0]
        self.type = species_data[1].split('/')  # タイプは複数の場合がある
        self.base_hp = species_data[2]
        self.base_attack = species_data[3]
        self.base_defense = species_data[4]
        self.base_speed = species_data[5]
        self.evolution_level = species_data[6]
        self.evolution_to = species_data[7]
        
        # レベルとステータス
        self.level = level
        self.exp = 0
        self.exp_to_next_level = 20 * level
        
        # 実際のステータスを計算
        self.calculate_stats()
        
        # 現在のHP
        self.current_hp = self.max_hp
        
        # 技リスト
        self.moves = []
        self.learn_moves_for_level()
        
        # 状態異常
        self.status_condition = None
        self.status_counter = 0
        
        # 野生かどうか
        self.is_wild = is_wild
    
    def calculate_stats(self):
        """レベルに基づいてステータスを計算"""
        self.max_hp = int((self.base_hp * 2 * self.level) / 100) + self.level + 10
        self.attack = int((self.base_attack * 2 * self.level) / 100) + 5
        self.defense = int((self.base_defense * 2 * self.level) / 100) + 5
        self.speed = int((self.base_speed * 2 * self.level) / 100) + 5
    
    def learn_moves_for_level(self):
        """現在のレベルで覚えるべき技を習得"""
        learnable = LEARNABLE_MOVES.get(self.species_id, {})
        
        # レベルごとに覚える技をチェック
        for level, move_ids in learnable.items():
            if level <= self.level:
                for move_id in move_ids:
                    # 既に覚えている技は追加しない
                    if not any(m['id'] == move_id for m in self.moves):
                        move_data = MOVES.get(move_id)
                        if move_data:
                            self.moves.append({
                                'id': move_id,
                                'name': move_data[0],
                                'type': move_data[1],
                                'power': move_data[2],
                                'accuracy': move_data[3],
                                'pp': move_data[4],
                                'current_pp': move_data[4]
                            })
        
        # 最大4つまで
        self.moves = self.moves[-4:] if len(self.moves) > 4 else self.moves
    
    def use_move(self, move_index, target):
        """Use a move"""
        if move_index >= len(self.moves):
            return f"{self.name} is confused!"
        
        move = self.moves[move_index]
        
        # Check PP
        if move['current_pp'] <= 0:
            return f"No PP left for {move['name']}!"
        
        # Check status conditions
        if self.status_condition:
            if self.status_condition == "sleep":
                if random.random() < 0.3:  # 30% chance to wake up
                    self.status_condition = None
                    return f"{self.name} woke up!"
                else:
                    return f"{self.name} is sleeping!"
            elif self.status_condition == "paralysis":
                if random.random() < 0.25:  # 25% chance to be fully paralyzed
                    return f"{self.name} is paralyzed and can't move!"
        
        # Check accuracy
        if random.randint(1, 100) > move['accuracy']:
            return f"{self.name}'s {move['name']} missed!"
        
        # Reduce PP
        move['current_pp'] -= 1
        
        # Calculate damage
        damage = self.calculate_damage(move, target)
        
        # Reduce target's HP
        target.current_hp -= damage
        target.current_hp = max(0, target.current_hp)
        
        # Effectiveness text
        effectiveness = self.calculate_type_effectiveness(move['type'], target.type)
        effect_text = ""
        if effectiveness > 1.5:
            effect_text = "It's super effective!"
        elif effectiveness < 0.5 and effectiveness > 0:
            effect_text = "It's not very effective..."
        elif effectiveness == 0:
            effect_text = "It has no effect..."
        
        # Status effect (example)
        status_effect = ""
        if move['name'] == "Thunder Shock" and random.random() < 0.3:
            target.status_condition = "paralysis"
            status_effect = f"{target.name} is paralyzed!"
        
        result = f"{self.name} used {move['name']}! "
        if damage > 0:
            result += f"{target.name} took {damage} damage! "
        if effect_text:
            result += effect_text + " "
        if status_effect:
            result += status_effect
        
        return result.strip()
    
    def calculate_damage(self, move, target):
        """ダメージ計算"""
        if move['power'] == 0:
            return 0
        
        # 基本ダメージ
        damage = ((2 * self.level / 5 + 2) * move['power'] * self.attack / target.defense) / 50 + 2
        
        # タイプ一致ボーナス
        stab = 1.5 if move['type'] in self.type else 1.0
        
        # タイプ相性
        effectiveness = self.calculate_type_effectiveness(move['type'], target.type)
        
        # 乱数（0.85～1.0）
        random_factor = random.uniform(0.85, 1.0)
        
        # 最終ダメージ
        final_damage = int(damage * stab * effectiveness * random_factor)
        return max(1, final_damage) if effectiveness > 0 else 0
    
    def calculate_type_effectiveness(self, attack_type, defense_types):
        """タイプ相性の計算"""
        effectiveness = 1.0
        for defense_type in defense_types:
            if attack_type in TYPE_CHART and defense_type in TYPE_CHART[attack_type]:
                effectiveness *= TYPE_CHART[attack_type][defense_type]
        return effectiveness
    
    def gain_exp(self, amount):
        """経験値獲得"""
        if self.is_wild:
            return False, 0
        
        self.exp += amount
        level_up = False
        levels_gained = 0
        
        while self.exp >= self.exp_to_next_level:
            self.level_up()
            level_up = True
            levels_gained += 1
        
        return level_up, levels_gained
    
    def level_up(self):
        """レベルアップ処理"""
        self.level += 1
        old_max_hp = self.max_hp
        
        # ステータス再計算
        self.calculate_stats()
        
        # HPの差分を現在HPに加算
        self.current_hp += (self.max_hp - old_max_hp)
        
        # 経験値テーブル更新
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.2)
        
        # 新しい技を習得
        self.learn_moves_for_level()
    
    def can_evolve(self):
        """進化可能かチェック"""
        return (self.evolution_level is not None and 
                self.evolution_to is not None and 
                self.level >= self.evolution_level)
    
    def evolve(self):
        """進化処理"""
        if not self.can_evolve():
            return False, None
        
        # 現在のHP割合を計算
        hp_ratio = self.current_hp / self.max_hp
        
        # 新しい種族のモンスターを作成
        evolved = Monster(self.evolution_to, self.level)
        
        # 経験値を引き継ぐ
        evolved.exp = self.exp
        evolved.exp_to_next_level = self.exp_to_next_level
        
        # HP割合を維持
        evolved.current_hp = int(evolved.max_hp * hp_ratio)
        
        # 野生状態を引き継ぐ
        evolved.is_wild = self.is_wild
        
        return True, evolved
    
    def heal(self, amount=None):
        """回復処理"""
        if amount is None:
            self.current_hp = self.max_hp
        else:
            self.current_hp = min(self.max_hp, self.current_hp + amount)
        
        # 状態異常も回復
        self.status_condition = None
        self.status_counter = 0
        
        # PPも回復
        for move in self.moves:
            move['current_pp'] = move['pp']
    
    def get_catch_rate(self, ball_bonus=1.0):
        """捕獲率の計算"""
        # 基本捕獲率（種族ごとに異なる値を設定できる）
        base_rate = 45  # 一般的な野生モンスター
        
        # HPによる補正
        hp_factor = 1 - (self.current_hp / self.max_hp) * 0.9
        
        # 状態異常による補正
        status_bonus = 1.0
        if self.status_condition == "sleep":
            status_bonus = 2.5
        elif self.status_condition in ["paralysis", "poison", "burn"]:
            status_bonus = 1.5
        
        # 最終捕獲率
        catch_rate = (base_rate * hp_factor * status_bonus * ball_bonus) / 255
        
        return min(catch_rate, 1.0)  # 最大100%
    
    def to_dict(self):
        """モンスターデータを辞書形式で返す（セーブ用）"""
        return {
            'species_id': self.species_id,
            'level': self.level,
            'exp': self.exp,
            'current_hp': self.current_hp,
            'moves': self.moves,
            'status_condition': self.status_condition,
            'is_wild': self.is_wild
        }
    
    @classmethod
    def from_dict(cls, data):
        """辞書からモンスターを復元（ロード用）"""
        monster = cls(data['species_id'], data['level'], data['is_wild'])
        monster.exp = data['exp']
        monster.current_hp = data['current_hp']
        monster.moves = data['moves']
        monster.status_condition = data['status_condition']
        return monster


def generate_wild_monster(area="grass", min_level=3, max_level=10):
    """野生モンスターの生成"""
    # エリアごとの出現モンスター
    area_monsters = {
        "grass": [1, 7, 13],  # 草原エリアに出現するモンスターID
        "water": [4],         # 水辺エリアに出現するモンスターID
        "cave": [10, 15],     # 洞窟エリアに出現するモンスターID
        "mountain": [1, 10],  # 山岳エリアに出現するモンスターID
    }
    
    # エリアに対応するモンスターがない場合はデフォルト
    monster_pool = area_monsters.get(area, [1, 4, 7, 10, 13, 15])
    
    # ランダムに選択
    species_id = random.choice(monster_pool)
    level = random.randint(min_level, max_level)
    
    # モンスター生成
    monster = Monster(species_id, level, is_wild=True)
    
    return monster
