import gamelib
import random
import math
import warnings
from sys import maxsize
import json
import enemy_info
from unit_info import UnitInfo
"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER, BITS, CORES
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        BITS = 1
        CORES = 0
        # This is a good place to do initial setup
        self.scored_on_locations = []

        global FILTER_INFO, ENCRYPTOR_INFO, DESTRUCTOR_INFO, PING_INFO, EMP_INFO, SCRAMBLER_INFO

        FILTER_INFO = UnitInfo(config, 0)
        ENCRYPTOR_INFO = UnitInfo(config, 1)
        DESTRUCTOR_INFO = UnitInfo(config, 2)
        PING_INFO = UnitInfo(config, 3)
        EMP_INFO = UnitInfo(config, 4)
        SCRAMBLER_INFO = UnitInfo(config, 5)

        self.scored_on_locations = []

        # EMP_range = gamelib.GameUnit(EMP, self.config).attackRange()
        # gamelib.debug_write("Got scored on at: {}".format(EMP_range))
        # gamelib.debug_write(EMP, EMP_INFO.attackRange)

        self.frontier = [(x, 15-math.ceil(EMP_INFO.attackRange)) for x in range(7, 21)]
        # self.left_corner =

    def get_unit_info(self):
        type_config = self.config["unitInformation"][0]
        self.stationary = type_config["unitCategory"] == 0
        self.speed = type_config.get("speed", 0)
        self.damage_f = type_config.get("attackDamageTower", 0)
        self.damage_i = type_config.get("attackDamageWalker", 0)
        self.attackRange = type_config.get("attackRange", 0)
        self.shieldRange = type_config.get("shieldRange", 0)
        self.max_health = type_config.get("startHealth", 0)
        self.shieldPerUnit = type_config.get("shieldPerUnit", 0)
        self.cost = [type_config.get("cost1", 0), type_config.get("cost2", 0)]

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()




    """
    Our strategy
    """

    def our_strategy_V1(self, game_state):
        """
        if we use
        """
        stationary_units = [FILTER, DESTRUCTOR, ENCRYPTOR]
        cheapest_unit = FILTER
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.BITS] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[
                game_state.BITS]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our EMPs from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.

        self.attack_side = 0  # 0 left, 1 right

        # determine where to build the wall of cheapest units
        self.build_line(game_state)

    def build_defense_line(self, game_state):
        """
        how to use bins
        """

        # self.line_y = get_frountier(deconstrutor) - range(EMP_attack) + 1

        # for x in range(27, 5, -1):
        #     game_state.attempt_spawn(cheapest_unit, [x, 11])

    # def emp_attacks(self, game_state):
    #     """
    #     how to use cores
    #     """
    #     # Now spawn EMPs next to the line
    #     # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
    #     # game_state.attempt_spawn(EMP, [24, 10], 1000)

    def build_Encryptor(self, game_state):
        pass

    def add_scrambler(self, game_state):
        pass



    """
    From fayllkw
    """
    def _got_scored_on_corner(self, left=True):
        if left:
            targets = [[0, 13], [1, 12], [2, 11], [3, 10], [4, 9]]
        else:
            targets = [[27, 13], [26, 12], [25, 11], [24, 10], [23, 9]]
        for point in self.scored_on_locations:
            if point in targets:
                return True
        return False


    """
    New for competitions
    """
    def spawn_and_upgrade_FILTER(self, game_state, filters_locations):
        if isinstance(filters_locations[0], int):
            filters_locations = [filters_locations]

        for loc in filters_locations:
            if game_state.attempt_spawn(FILTER, loc) > 0:
                game_state.attempt_upgrade(loc)

    def frontier_defense(self, game_state):
        self.frontier_destructor(game_state)


    def frontier_destructor(self, game_state):
        # build deconstructor by levels
        destr_locs_multilevel = \
            [
                # [[2, 12], [25, 12], [13, 12], [19, 12], [8, 12]], # level1
                [[2, 12], [25, 12], [13, 12], [19, 12], [8, 12]], # level1
                [[23, 11], [4, 11]],
                [[9, 10], [18, 10]],

            ]
        n_levels = len(destr_locs_multilevel)

        for level in range(n_levels):

            # for each loc build a destructor
            # for loc in destr_locs_multilevel[level]:
            game_state.attempt_spawn(DESTRUCTOR, destr_locs_multilevel[level])
            if not self.check_finish_level(game_state, destr_locs_multilevel[level]):
                break

            # build filter wall
            if level == 0:
                for loc in destr_locs_multilevel[level]:
                    self.spawn_and_upgrade_FILTER(game_state, [loc[0], loc[1]+1])

            # if level > 0:
            #     for loc in destr_locs_multilevel[level-1]:
            #         self.spawn_and_upgrade_FILTER(game_state, [loc[0]+1, loc[1]])
            #     for loc in destr_locs_multilevel[level-1]:
            #         self.spawn_and_upgrade_FILTER(game_state, [loc[0]-1, loc[1]])
        

    def check_finish_level(self, game_state, locs):
        # check if a level of defenses has been built
        count = 0
        for loc in locs:
            if game_state.contains_stationary_unit(loc):
                count += 1
        if count == len(locs):
            return True

    def emp_line_strategy_adaptive(self, game_state, left=True, scan=False):
        """
        Build a line of the cheapest stationary unit so our EMP's can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [FILTER, DESTRUCTOR, ENCRYPTOR]
        cheapest_unit = FILTER
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.BITS] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.BITS]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our EMPs from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.


        if left:
            emp_line = [24,] + list(range(21, 5, -1))
        else:
            emp_line = [3,] + list(range(5, 21))

        # if left:
        #     if game_state.contains_stationary_unit([5, 12]):
        #         game_state.attempt_remove()
        left_start = [3,10]
        right_start = [24,10]

        if left:
            gate = [22, 12]

            start_loc = right_start if scan else left_start
        else:
            gate = [5, 12]
            start_loc = left_start if scan else right_start

        game_state.attempt_spawn(cheapest_unit, gate)
        game_state.attempt_remove(gate)

        for x in emp_line:
            if cheapest_unit == FILTER:
                # self.spawn_and_upgrade_FILTER(game_state, [x, 12])
                game_state.attempt_spawn(cheapest_unit, [x, 12])
            else:
                game_state.attempt_spawn(cheapest_unit, [x, 12])

        if game_state.number_affordable(EMP) >= 5:
            self.emp_attacks(game_state, start_loc)

        # Now spawn EMPs next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        # gamelib.debug_write(EMP_INFO.cost)

    def emp_attacks(self, game_state, loc, num=1000):
        return game_state.attempt_spawn(EMP, loc, num)

    def get_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy destructors that can attack the final location and multiply by destructor damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(DESTRUCTOR,
                                                                                             game_state.config).damage_i
            damages.append(damage)

        # Now just return the location that takes the least damage
        return damages

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def starter_strategy(self, game_state):
        """
        For defense we will use a spread out layout and some Scramblers early on.
        We will place destructors near locations the opponent managed to score on.
        For offense we will use long range EMPs if they place stationary units near the enemy's front.
        If there are no stationary units to attack in the front, we will send Pings to try and score quickly.
        """
        # TODO the current strategy is vulnerable to ping set cornner attack

        # First, place basic defenses
        self.build_defences(game_state)
        # Now build reactive defenses based on where the enemy scored
        self.build_reactive_defense(game_state)

        # If the turn is less than 5, stall with Scramblers and wait to see enemy's base
        if game_state.turn_number < 4:
            self.stall_with_scramblers(game_state)


        else:
            # Now let's analyze the enemy base to see where their defenses are concentrated.
            # If they have many units in the front we can build a line for our EMPs to attack them at long range.
            if self.detect_enemy_unit(game_state, unit_type=None, valid_x=None, valid_y=[14, 15]) > 10:
                self.emp_line_strategy_adaptive(game_state, left=True, scan=True)

            if self._got_scored_on_corner(left=True):
                self.emp_line_strategy_adaptive(game_state, left=True)  # check if have attacked

            if self._got_scored_on_corner(left=False):
                self.emp_line_strategy_adaptive(game_state, left=False)  # check if have attacked


            else:
                # They don't have many units in the front so lets figure out their least defended area and send Pings there.

                # Only spawn Ping's every other turn
                # Sending more at once is better since attacks can only hit a single ping at a time
                # if game_state.turn_number % 2 == 1:

                # To simplify we will just check sending them from back left and right
                ping_spawn_location_options = [[13, 0], [14, 0], [7,6], [20, 6]]
                # TODO need to check more possible sending locations

                # if self._got_scored_on_corner(left=True):

                damages = self.get_damage_spawn_location(game_state, ping_spawn_location_options)
                if min(damages) > game_state.number_affordable(PING)*15*0.5:
                    # emp
                    worst_loc = ping_spawn_location_options[damages.index(max(damages))]
                    if game_state.number_affordable(EMP) >= 5:
                        self.emp_attacks(game_state, worst_loc)
                else:
                    best_location = ping_spawn_location_options[damages.index(min(damages))]
                # best_location = self.least_damage_spawn_location(game_state, ping_spawn_location_options)
                    if game_state.number_affordable(PING) >= 15:
                        game_state.attempt_spawn(PING, best_location, 1000)



            # If we have spare cores, let's build some Encryptors to boost our Pings' health.
            encryptor_locations = [[6,10], [21,10], [12, 10], [14, 10]]
            game_state.attempt_spawn(ENCRYPTOR, encryptor_locations)
            
            if game_state.number_affordable(DESTRUCTOR) >= 6:
                self.build_luxury_defense(game_state)
            
            if game_state.number_affordable(DESTRUCTOR) >= 6:
                self.build_luxury_walls(game_state)


    def build_defences(self, game_state):
        """
        Build basic defenses using hardcoded locations.
        Remember to defend corners and avoid placing units in the front where enemy EMPs can attack them.
        """
        # Useful tool for setting up your base locations: https://www.kevinbai.design/terminal-map-maker
        # More community tools available at: https://terminal.c1games.com/rules#Download

        # Place destructors that attack enemy units
        # destructor_locations = [[0, 13], [27, 13], [8, 11], [19, 11], [13, 11], [14, 11]]
        # attempt_spawn will try to spawn units if we have resources, and will check if a blocking unit is already there
        # game_state.attempt_spawn(DESTRUCTOR, destructor_locations)

        # build frontier defense line
        self.frontier_defense(game_state)

        # Place filters in front of destructors to soak up damage for them
        # filter_locations = [[8, 12], [19, 12]]
        # game_state.attempt_spawn(FILTER, filter_locations)
        # self.spawn_and_upgrade_FILTER(game_state, filter_locations)

        # upgrade filters so they soak more damage
        # game_state.attempt_upgrade(filter_locations)

        # filters at corners
        edge_locs = [[0, 13], [27, 13], [26, 13], [1, 13], [25, 13], [2, 13]]
        # edge_locs_right = [[27, 13], [26, 13], [25, 13], [24, 12]]
        self.spawn_and_upgrade_FILTER(game_state, edge_locs)


        if self._got_scored_on_corner(left=True) or game_state.number_affordable(DESTRUCTOR) >= 6:
            self.protect_left_corner(game_state) # check if have attacked

        if self._got_scored_on_corner(left=False) or game_state.number_affordable(DESTRUCTOR) >= 6:
            self.protect_right_corner(game_state) # check if have attacked

    def build_luxury_defense(self, game_state):
        luxury_destructor_locs = [[1,12],[26,12],[3,13],[24,13],[6,13],[21,13],[14,12],[16,13],[10,13]]
        count = 0
        for loc in luxury_destructor_locs:
            count += game_state.attempt_spawn(DESTRUCTOR, loc, 1)
            if game_state.number_affordable(DESTRUCTOR) < 3:
                return
    
    def build_luxury_walls(self, game_state):
        
        luxury_wall_locs = [[0,13],[1,13],[2,13],[4,13],[7,13],[8,13],[9,13],[11,13],[12,13],[13,13],[14,13],[15,13],[17,13],[18,13],[19,13],[20,13],[23,13],[25,13],[26,13],[27,13]]
        random.shuffle(luxury_wall_locs)
        for loc in luxury_wall_locs:
            self.spawn_and_upgrade_FILTER(game_state, loc)
            if game_state.number_affordable(DESTRUCTOR) < 3:
                return
            

    def protect_left_corner(self,game_state):

        game_state.attempt_spawn(DESTRUCTOR, [1, 12], 1)
        game_state.attempt_spawn(DESTRUCTOR, [26, 12], 1)

        yellow_destructors_points = [[1,12],[2,12],]
        yellow_filters_points = [[3,12],[1,13],[2,13],[0,13]]
        for loc in yellow_destructors_points:
#             self.if_do(0.7)
            game_state.attempt_spawn(DESTRUCTOR, loc, 1)
        for loc in yellow_filters_points:
#             self.if_do(0.7)
            # game_state.attempt_spawn(FILTER, loc, 1)
            self.spawn_and_upgrade_FILTER(game_state, loc)


    def protect_right_corner(self,game_state):
        orange_destructors_points = [[25,12],[26,12]]
        orange_filters_points = [[24,12],[26,13],[25,13],[27,13]]
        for loc in orange_destructors_points:
#             self.if_do(0.7)
            game_state.attempt_spawn(DESTRUCTOR, loc, 1)
        for loc in orange_filters_points:
#             self.if_do(0.7)
            # game_state.attempt_spawn(FILTER, loc, 1)
            self.spawn_and_upgrade_FILTER(game_state, loc)
            
    def protect_center(self, game_state):
        center_destructors_points = [[13,12],[14,12],[9,9],[18,9]]
        center_filter_points = [[13,13],[14,13],[12,12],[15,12]]
        for loc in center_destructors_points:
            game_state.attempt_spawn(DESTRUCTOR, loc, 1)
        for loc in center_filter_points:
            self.spawn_and_upgrade_FILTER(game_state, loc)
        

    def if_do(self,cut_off=0.5):
        r = random.random()
        return r<cut_off

    def build_reactive_defense(self, game_state):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames 
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build destructor one space above so that it doesn't block our own edge spawn locations
            build_location = [location[0], location[1]+1]
            game_state.attempt_spawn(DESTRUCTOR, build_location)

    def stall_with_scramblers(self, game_state):
        """
        Send out Scramblers at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        
        # Remove locations that are blocked by our own firewalls 
        # since we can't deploy units there.
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        # While we have remaining bits to spend lets send out scramblers randomly.
        while game_state.get_resource(BITS) >= game_state.type_cost(SCRAMBLER)[BITS] and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            
            game_state.attempt_spawn(SCRAMBLER, deploy_location)
            """
            We don't have to remove the location since multiple information 
            units can occupy the same space.
            """

    def emp_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our EMP's can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [FILTER, DESTRUCTOR, ENCRYPTOR]
        cheapest_unit = FILTER
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.BITS] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.BITS]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our EMPs from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        game_state.attempt_spawn(DESTRUCTOR, [1,12], 1)
        game_state.attempt_spawn(DESTRUCTOR, [26,12], 1)
        for x in range(27, 5, -1):
            if cheapest_unit == FILTER:
                self.spawn_and_upgrade_FILTER(game_state, [x, 12])
            else:
                game_state.attempt_spawn(cheapest_unit, [x, 12])

        # Now spawn EMPs next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        gamelib.debug_write(EMP_INFO.cost)
        if game_state.number_affordable(EMP) >= 5:
            game_state.attempt_spawn(EMP, [24, 10], 1000)

    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to 
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy destructors that can attack the final location and multiply by destructor damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(DESTRUCTOR, game_state.config).damage_i
            damages.append(damage)
        
        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at: https://docs.c1games.com/json-docs.html
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
