import pygame
import random

class GameMap:
    def __init__(self, width=800, height=600, tile_size=40):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        
        # タイルの種類
        self.GRASS = 0
        self.WATER = 1
        self.MOUNTAIN = 2
        self.PATH = 3
        self.HOUSE = 4
        self.TREE = 5
        
        # タイルの色
        self.tile_colors = {
            self.GRASS: (100, 200, 100),
            self.WATER: (100, 100, 240),
            self.MOUNTAIN: (150, 120, 90),
            self.PATH: (210, 180, 140),
            self.HOUSE: (200, 100, 100),
            self.TREE: (50, 120, 50)
        }
        
        # マップデータの初期化
        self.tiles = self.generate_map()
        
        # エリア情報
        self.areas = self.define_areas()
    
    def generate_map(self):
        """シンプルなマップを生成"""
        cols = self.width // self.tile_size
        rows = self.height // self.tile_size
        
        # 基本的に草原で埋める
        tiles = [[self.GRASS for _ in range(cols)] for _ in range(rows)]
        
        # 水辺を追加
        for i in range(3, 8):
            for j in range(cols):
                if random.random() < 0.8:
                    tiles[i][j] = self.WATER
        
        # 山を追加
        for i in range(rows-5, rows):
            for j in range(cols):
                if random.random() < 0.7:
                    tiles[i][j] = self.MOUNTAIN
        
        # 道を追加
        for i in range(rows):
            tiles[i][cols//2] = self.PATH
        
        for j in range(cols):
            tiles[rows//2][j] = self.PATH
        
        # 家を追加
        tiles[2][2] = self.HOUSE
        tiles[2][cols-3] = self.HOUSE
        tiles[rows-3][2] = self.HOUSE
        tiles[rows-3][cols-3] = self.HOUSE
        
        # 木を追加
        for _ in range(20):
            i = random.randint(0, rows-1)
            j = random.randint(0, cols-1)
            if tiles[i][j] == self.GRASS:
                tiles[i][j] = self.TREE
        
        return tiles
    
    def define_areas(self):
        """マップ上のエリアを定義"""
        cols = self.width // self.tile_size
        rows = self.height // self.tile_size
        
        # エリアマップ（各タイルがどのエリアに属するか）
        areas = {}
        
        # 草原エリア
        grass_area = []
        for i in range(rows):
            for j in range(cols):
                if self.tiles[i][j] == self.GRASS:
                    grass_area.append((j * self.tile_size, i * self.tile_size))
        areas["grass"] = grass_area
        
        # 水辺エリア
        water_area = []
        for i in range(rows):
            for j in range(cols):
                if self.tiles[i][j] == self.WATER:
                    water_area.append((j * self.tile_size, i * self.tile_size))
        areas["water"] = water_area
        
        # 山岳エリア
        mountain_area = []
        for i in range(rows):
            for j in range(cols):
                if self.tiles[i][j] == self.MOUNTAIN:
                    mountain_area.append((j * self.tile_size, i * self.tile_size))
        areas["mountain"] = mountain_area
        
        return areas
    
    def draw(self, screen):
        """マップを描画"""
        cols = self.width // self.tile_size
        rows = self.height // self.tile_size
        
        for i in range(rows):
            for j in range(cols):
                tile_type = self.tiles[i][j]
                color = self.tile_colors.get(tile_type, (0, 0, 0))
                
                rect = pygame.Rect(j * self.tile_size, i * self.tile_size, 
                                  self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)
                
                # タイルの境界線
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)
    
    def get_tile_at_position(self, x, y):
        """指定された座標のタイルタイプを取得"""
        col = x // self.tile_size
        row = y // self.tile_size
        
        cols = self.width // self.tile_size
        rows = self.height // self.tile_size
        
        if 0 <= row < rows and 0 <= col < cols:
            return self.tiles[row][col]
        return None
    
    def is_walkable(self, x, y):
        """指定された座標が歩行可能かどうか"""
        tile_type = self.get_tile_at_position(x, y)
        
        # 水と山と家と木は歩けない
        return tile_type not in [self.WATER, self.MOUNTAIN, self.HOUSE, self.TREE]
    
    def get_area_at_position(self, x, y):
        """指定された座標のエリアを取得"""
        tile_type = self.get_tile_at_position(x, y)
        
        if tile_type == self.GRASS or tile_type == self.PATH:
            return "grass"
        elif tile_type == self.WATER:
            return "water"
        elif tile_type == self.MOUNTAIN:
            return "mountain"
        else:
            return "grass"  # デフォルト
