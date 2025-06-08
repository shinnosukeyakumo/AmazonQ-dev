# Monster Base Data

# Monster Species Data
MONSTER_SPECIES = {
    # ID: [name, type, base_hp, base_attack, base_defense, base_speed, evolution_level, evolution_to_id]
    1: ["Embery", "Fire", 20, 12, 8, 10, 16, 2],
    2: ["Flameon", "Fire", 40, 22, 15, 18, 36, 3],
    3: ["BlazeDragon", "Fire/Dragon", 70, 38, 30, 25, None, None],
    
    4: ["Aquatle", "Water", 22, 10, 10, 8, 16, 5],
    5: ["Seashell", "Water", 42, 18, 20, 15, 36, 6],
    6: ["OceanTurtle", "Water", 75, 32, 40, 22, None, None],
    
    7: ["Leafkit", "Grass", 19, 11, 9, 12, 16, 8],
    8: ["LeafCat", "Grass", 38, 20, 18, 22, 36, 9],
    9: ["ForestLion", "Grass", 68, 35, 32, 35, None, None],
    
    10: ["Rockite", "Rock", 25, 10, 15, 5, 20, 11],
    11: ["Boulderex", "Rock", 45, 18, 30, 10, 40, 12],
    12: ["MountainGolem", "Rock/Ground", 80, 35, 50, 15, None, None],
    
    13: ["Sparkle", "Electric", 18, 12, 8, 15, 20, 14],
    14: ["Thunderbolt", "Electric", 45, 30, 20, 35, None, None],
    
    15: ["Ghostly", "Ghost", 17, 13, 7, 13, 25, 16],
    16: ["Phantom", "Ghost", 40, 28, 18, 28, None, None],
}

# Move Data
MOVES = {
    # ID: [name, type, power, accuracy, PP]
    1: ["Tackle", "Normal", 40, 100, 35],
    2: ["Scratch", "Normal", 40, 100, 35],
    3: ["Bite", "Normal", 60, 100, 25],
    
    # Fire type
    10: ["Ember", "Fire", 40, 100, 25],
    11: ["Flamethrower", "Fire", 90, 100, 15],
    12: ["Fire Blast", "Fire", 110, 85, 5],
    
    # Water type
    20: ["Water Gun", "Water", 40, 100, 25],
    21: ["Surf", "Water", 90, 100, 15],
    22: ["Hydro Pump", "Water", 110, 80, 5],
    
    # Grass type
    30: ["Vine Whip", "Grass", 45, 100, 25],
    31: ["Razor Leaf", "Grass", 55, 95, 25],
    32: ["Solar Beam", "Grass", 120, 100, 10],
    
    # Rock type
    40: ["Rock Throw", "Rock", 50, 90, 15],
    41: ["Rock Slide", "Rock", 75, 90, 10],
    
    # Electric type
    50: ["Thunder Shock", "Electric", 40, 100, 30],
    51: ["Thunderbolt", "Electric", 90, 100, 15],
    
    # Ghost type
    60: ["Night Shade", "Ghost", 0, 100, 15],  # Deals damage equal to user's level
    61: ["Shadow Ball", "Ghost", 80, 100, 15],
}

# Type Chart
TYPE_CHART = {
    "Normal": {
        "Ghost": 0,
        "Rock": 0.5,
    },
    "Fire": {
        "Fire": 0.5,
        "Water": 0.5,
        "Grass": 2,
        "Rock": 0.5,
    },
    "Water": {
        "Fire": 2,
        "Water": 0.5,
        "Grass": 0.5,
        "Rock": 2,
    },
    "Grass": {
        "Fire": 0.5,
        "Water": 2,
        "Grass": 0.5,
        "Rock": 2,
    },
    "Electric": {
        "Water": 2,
        "Grass": 0.5,
        "Electric": 0.5,
        "Rock": 0.5,
    },
    "Rock": {
        "Fire": 2,
        "Grass": 0.5,
        "Rock": 0.5,
    },
    "Ghost": {
        "Normal": 0,
        "Ghost": 2,
    },
    "Dragon": {
        "Dragon": 2,
    },
    "Ground": {
        "Electric": 0,
        "Rock": 2,
    }
}

# Learnable Moves
LEARNABLE_MOVES = {
    # Monster ID: {level: [move_id, move_id, ...]}
    1: {
        1: [1, 10],  # Level 1: Tackle, Ember
        5: [2],      # Level 5: Scratch
        10: [3],     # Level 10: Bite
        15: [11],    # Level 15: Flamethrower
    },
    2: {
        1: [1, 10, 2, 3],
        20: [11],
        30: [12],
    },
    3: {
        1: [1, 10, 2, 3, 11],
        40: [12],
    },
    
    4: {
        1: [1, 20],
        5: [2],
        10: [3],
        15: [21],
    },
    
    7: {
        1: [1, 30],
        5: [2],
        10: [31],
        15: [32],
    },
    
    10: {
        1: [1, 40],
        5: [41],
    },
    
    13: {
        1: [1, 50],
        10: [51],
    },
    
    15: {
        1: [1, 60],
        10: [61],
    },
}
