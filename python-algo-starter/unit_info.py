#!/usr/bin/env python
"""
Created by zhenlinxu on 01/31/2020
"""
# from gamelib.game_state i

class UnitInfo:

    def __init__(self, config, index):
        self.config = config
        type_config = self.config["unitInformation"][index]
        self.stationary = type_config["unitCategory"] == 0
        self.speed = type_config.get("speed", 0)
        self.damage_f = type_config.get("attackDamageTower", 0)
        self.damage_i = type_config.get("attackDamageWalker", 0)
        self.attackRange = type_config.get("attackRange", 0)
        self.shieldRange = type_config.get("shieldRange", 0)
        self.max_health = type_config.get("startHealth", 0)
        self.shieldPerUnit = type_config.get("shieldPerUnit", 0)
        self.cost = [type_config.get("cost1", 0), type_config.get("cost2", 0)]


