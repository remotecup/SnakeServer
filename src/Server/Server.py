from src.Base.Server import *
import src.Conf.Server_Snake_Conf as Conf
import random


def action_to_vector(string_action):
    if string_action is 'u':
        action = Vector2D(-1, 0)
    elif string_action is 'd':
        action = Vector2D(1, 0)
    elif string_action is 'l':
        action = Vector2D(0, -1)
    elif string_action is 'r':
        action = Vector2D(0, 1)
    else:
        action = None
    return action


class Wall:
    def __init__(self, i, j, h=1, w=1):
        self.i = i
        self.j = j
        self.h = h
        self.w = w
        self.body = [Vector2D(ii, jj) for ii in range(i, i + h) for jj in range(j, j + w)]

    def is_conflict(self, wall_list):
        if type(wall_list) == Wall:
            if wall_list.i >= self.i + self.h:
                return False
            if wall_list.j >= self.j + self.w:
                return False
            if wall_list.i + wall_list.h <= self.i:
                return False
            if wall_list.j + wall_list.w <= self.j:
                return False
            return True
        if type(wall_list) == list:
            for w in self.body:
                if w in wall_list:
                    return True
            return False
        if type(wall_list) == Vector2D:
            if wall_list.i >= self.i and wall_list.i < self.i + self.h:
                if wall_list.j >= self.j and wall_list.j < self.j + self.w:
                    return True
            return False

    def is_in_game(self):
        if self.i <= 0:
            return False
        if self.i + self.h >= Conf.max_i - 1:
            return False
        if self.j <= 0:
            return False
        if self.j + self.w >= Conf.max_j - 1:
            return False
        return True

    def __repr__(self):
        return '{} {} {} {}, {}'.format(self.i, self.j,
                                        self.h, self.w,
                                        self.body)


class SnakeAgent(Agent):
    def __init__(self):
        super().__init__()
        self.last_action = Vector2D(0, 0)
        self.head = Vector2D(0, 0)
        self.next_head = Vector2D(0, 0)
        self.last_action_cycle = 0
        self.body = []
        self.goal_pos = None

    def update_next(self):
        logging.debug('id {} pos {} action {} to {}'.format(self.id, self.head, self.last_action, self.next_head))
        self.next_head.i = self.head.i + self.last_action.i
        self.next_head.j = self.head.j + self.last_action.j
        logging.debug('id {} pos {} action {} to {}'.format(self.id, self.head, self.last_action, self.next_head))

    def reset(self, snake_server):
        for pos in self.body:
            snake_server.world['board'][pos.i][pos.j] = 0
        self.body.clear()
        self.body = copy.deepcopy(snake_server.start_snake_body[self.id])
        self.head = copy.deepcopy(self.body[0])
        # if self.id == 1:
        #     self.head = Vector2D(1, 3)
        #     self.body.append(copy.deepcopy(self.head))
        #     self.body.append(Vector2D(1, 2))
        #     self.body.append(Vector2D(1, 1))
        # elif self.id == 2:
        #     self.head = Vector2D(1, Conf.max_j - 4)
        #     self.body.append(copy.deepcopy(self.head))
        #     self.body.append(Vector2D(1, Conf.max_j - 3))
        #     self.body.append(Vector2D(1, Conf.max_j - 2))
        # elif self.id == 3:
        #     self.head = Vector2D(Conf.max_i - 2, 3)
        #     self.body.append(copy.deepcopy(self.head))
        #     self.body.append(Vector2D(Conf.max_i - 2, 2))
        #     self.body.append(Vector2D(Conf.max_i - 2, 1))
        # elif self.id == 4:
        #     self.head = Vector2D(Conf.max_i - 2, Conf.max_j - 4)
        #     self.body.append(copy.deepcopy(self.head))
        #     self.body.append(Vector2D(Conf.max_i - 2, Conf.max_j - 3))
        #     self.body.append(Vector2D(Conf.max_i - 2, Conf.max_j - 2))
        for p in self.body:
            snake_server.world['board'][p.i][p.j] = self.id

    def update_world(self, world):
        pass


class SnakeServer(Server):
    def __init__(self):
        print('Server __init')
        super().__init__()
        self.null_agent = SnakeAgent()
        self.dict_conf = {'max_i': Conf.max_i, 'max_j': Conf.max_j,
                          'team_number': Conf.agent_numbers, 'goal_id': Conf.agent_numbers + 1}
        self.world = {'board': None, 'heads': {}}
        self.start_snake_body = {}
        self.start_snake_body[1] = [Vector2D(1, 3),Vector2D(1, 2),Vector2D(1, 1)]
        self.start_snake_body[2] = [Vector2D(1, Conf.max_j - 4), Vector2D(1, Conf.max_j - 3), Vector2D(1, Conf.max_j - 2)]
        self.start_snake_body[3] = [Vector2D(Conf.max_i - 2, 3), Vector2D(Conf.max_i - 2, 2), Vector2D(Conf.max_i - 2, 1)]
        self.start_snake_body[4] = [Vector2D(Conf.max_i - 2, Conf.max_j - 4), Vector2D(Conf.max_i - 2, Conf.max_j - 3), Vector2D(Conf.max_i - 2, Conf.max_j - 2)]
        self.goal_id = 5
        self.goal_ate = False
        self.last_cycle_ate = 0

    def update(self):
        logging.debug('Update Worlddddd')
        self.goal_ate = False
        keys = list(self.agents.keys())
        random.shuffle(keys)
        for key in keys:
            self.agents[key].update_next()
            self.agents[key].next_head = self.normalize_pos(self.agents[key].next_head)
            logging.error('wall size:{}'.format(len(self.wall_poses)))
            if self.agents[key].next_head in self.wall_poses:
                logging.error('agent {} in wall body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))
                self.agents[key].reset(self)
                logging.error(
                    'agent {} in wall body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))
                self.agents[key].score -= 5
            elif self.world['board'][self.agents[key].next_head.i][self.agents[key].next_head.j] == self.goal_id:
                self.goal_ate = True
                logging.error('goad id: {}'.format(self.goal_id))
                logging.error(
                    'agent {} in goal body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))

                self.agents[key].head = copy.deepcopy(self.agents[key].next_head)
                self.agents[key].body.insert(0, copy.deepcopy(self.agents[key].next_head))
                self.agents[key].score += 1
                self.world['board'][self.agents[key].next_head.i][self.agents[key].next_head.j] = self.agents[key].id
                self.reset_game()
                self.last_cycle_ate = self.cycle
            else:
                logging.error('elseeeeeeee')
                snake_accident = False
                for s in self.agents:
                    if self.agents[key].next_head in self.agents[s].body[:len(self.agents[s].body) - 1]:
                        snake_accident = True
                        break
                logging.error('afterrrrrrrr forrrrrr')
                if snake_accident:
                    logging.error('agent {} in other'.format(self.agents[key].id))
                    self.agents[key].reset(self)
                    self.agents[key].score -= 5
                else:
                    logging.error('agent {} go body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))
                    end_body = self.agents[key].body[-1]
                    logging.error('agent {} end is {}'.format(self.agents[key].id, end_body))
                    self.world['board'][end_body.i][end_body.j] = 0
                    self.agents[key].body.insert(0, copy.deepcopy(self.agents[key].next_head))
                    del self.agents[key].body[-1]
                    self.agents[key].head = copy.deepcopy(self.agents[key].next_head)
                    logging.error('agent {} next head is {}'.format(self.agents[key].id, self.agents[key].next_head))
                    self.world['board'][self.agents[key].next_head.i][self.agents[key].next_head.j] = self.agents[key].id
                    logging.error('agent {} go body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))
                    self.print_world()

        self.world['heads'].clear()
        for key in self.agents:
            self.world['heads'][self.agents[key].name] = [self.agents[key].head.i, self.agents[key].head.j]
        self.cycle += 1
        if (self.cycle - self.last_cycle_ate) % Conf.change_goal_pos == 0 and not self.goal_ate:
            self.goal_ate = False
            self.reset_game()

    def make_world(self):
        logging.info('make new world')
        self.world['board'] = [[0 for x in range(Conf.max_j)] for y in range(Conf.max_i)]
        self.wall_poses = []
        self.walls = []
        print(Conf.max_i, Conf.max_j)
        temp_positions = [Vector2D(x, y) for x in range(Conf.max_i) for y in range(Conf.max_j)]
        print(temp_positions)
        random.shuffle(temp_positions)
        random.shuffle(temp_positions)
        ok_wall_6_number = 0
        ok_wall_3_number = 0
        ok_wall_2_number = 0
        pos = 0
        for i in range(Conf.max_i):
            self.wall_poses.append(Vector2D(i, 0))
            self.wall_poses.append(Vector2D(i, Conf.max_j - 1))
            self.walls.append(Wall(i, 0))
        for j in range(Conf.max_j):
            self.wall_poses.append(Vector2D(0, j))
            self.wall_poses.append(Vector2D(Conf.max_i - 1, j))
            self.walls.append(Wall(0, j))
        while ok_wall_6_number < Conf.wall_6_number:
            temp_position = temp_positions[pos]
            wall = Wall(temp_position.i, temp_position.j, 2, 3)
            if not wall.is_in_game():
                pos += 1
                continue
            snake_conflict = False
            for s in range(1, 5):
                if wall.is_conflict(self.start_snake_body[s]):
                    snake_conflict = True
                    break
            if snake_conflict:
                pos += 1
                continue
            wall_conflict = False
            for w in self.walls:
                if wall.is_conflict(w):
                    wall_conflict = True
                    break
            if wall_conflict:
                pos += 1
                continue
            self.walls.append(wall)

            print(temp_positions)
            print(wall)
            for w in wall.body:
                print(w)
                self.wall_poses.append(w)
                temp_positions.remove(w)
            ok_wall_6_number += 1
        pos = 0
        while ok_wall_3_number < Conf.wall_3_number:
            temp_position = temp_positions[pos]
            wall = Wall(temp_position.i, temp_position.j, 1, 3)
            if not wall.is_in_game():
                pos += 1
                continue
            snake_conflict = False
            for s in range(1, 5):
                if wall.is_conflict(self.start_snake_body[s]):
                    snake_conflict = True
                    break
            if snake_conflict:
                pos += 1
                continue
            wall_conflict = False
            for w in self.walls:
                if wall.is_conflict(w):
                    wall_conflict = True
                    break
            if wall_conflict:
                pos += 1
                continue
            self.walls.append(wall)
            for w in wall.body:
                self.wall_poses.append(w)
                temp_positions.remove(w)
            ok_wall_3_number += 1
        pos = 0
        while ok_wall_2_number < Conf.wall_2_number:
            temp_position = temp_positions[pos]
            wall = Wall(temp_position.i, temp_position.j, 1, 2)
            if not wall.is_in_game():
                pos += 1
                continue
            snake_conflict = False
            for s in range(1, 5):
                if wall.is_conflict(self.start_snake_body[s]):
                    snake_conflict = True
                    break
            if snake_conflict:
                pos += 1
                continue

            self.walls.append(wall)
            for w in wall.body:
                self.wall_poses.append(w)
                try:
                    temp_positions.remove(w)
                except:
                    print(w)
            ok_wall_2_number += 1

        for w in self.wall_poses:
            self.world['board'][w.i][w.j] = -1

        for key in self.agents:
            self.agents[key].reset(self)

        self.reset_game()

        self.world['heads'].clear()
        for key in self.agents:
            self.world['heads'][self.agents[key].name] = [self.agents[key].head.i, self.agents[key].head.j]
        self.print_world()

    def action_parse(self, msg):
        message = parse(msg[0])
        address = msg[1]
        if message.type is not 'MessageClientAction':
            logging.error('message type is not action, client: {}'
                          .format(self.agents.get(address, Agent()).name))
            return False
        if address not in self.agents:
            logging.error('message from invalid address, address: {}'.format(address))
            return False
        action = action_to_vector(message.string_action)
        self.save_rcl(self.agents[address].id, message.string_message, action)
        if action is None:
            action = self.agents[address].last_action
        self.agents[address].last_action = action
        if self.agents[address].last_action_cycle < self.cycle:
            self.agents[address].last_action_cycle = self.cycle
            self.receive_action += 1
        return True

    def reset_game(self):
        try:
            if not self.goal_ate:
                self.world['board'][self.goal_pos.i][self.goal_pos.j] = 0
        except:
            print()
        temp_positions = [Vector2D(x, y) for x in range(Conf.max_i) for y in range(Conf.max_j)]
        random.shuffle(temp_positions)
        random.shuffle(temp_positions)
        print(self.wall_poses)
        for pos in temp_positions:
            if pos in self.wall_poses:
                print(pos, 'is wall')
                continue
            in_snakes = False
            for k in self.agents:
                if pos in self.agents[k].body:
                    print(pos, 'is snake')
                    in_snakes = True
                    break
            if in_snakes:
                continue
            print(pos, 'is ok')
            self.goal_pos = pos
            print(pos)
            self.world['board'][pos.i][pos.j] = self.goal_id
            break

    def normalize_pos(self, pos):
        if pos.i >= Conf.max_i:
            pos.i = Conf.max_i - 1
        if pos.i < 0:
            pos.i = 0
        if pos.j >= Conf.max_j:
            pos.j = Conf.max_j - 1
        if pos.j < 0:
            pos.j = 0
        return pos

    def print_world(self):
        logging.info('cycle:{}'.format(self.cycle))
        for key in self.agents:
            logging.info('score {} : {}'.format(self.agents[key].name, str(self.agents[key].score)))
        for c in self.world['board']:
            logging.info(str(c))
