import pygame
from Player import TURN_DISPOSE, TURN_PLAY

class ActionWait:
    def __init__(self, callback, duration):
        self.duration = duration
        self._callback = callback

    def update(self, elapsed):
        pass

    def finished(self):
        self._callback()


class ActionMoveCard:
    def __init__(self, painter, callback, action):
        self.duration = 400
        self._painter = painter
        self._callback = callback
        self._action = action

        card_no = action[1]
        self._card = self._painter.cards[card_no]
        self._card.blind = False
        self._card.zorder = 2
        if action[0] == TURN_DISPOSE:
            self._card.enabled = False
        self._origin = (self._card.x, self._card.y)
        self._dest = self._painter.deck_position

    def update(self, elapsed):
        ratio = float(elapsed) / self.duration
        self._card.x = int(self._origin[0] + ratio * (self._dest[0] - self._origin[0]))
        self._card.y = int(self._origin[1] + ratio * (self._dest[1] - self._origin[1]))

    def finished(self):
        self._card.zorder = 0
        self._painter.cards['deck'] = self._card
        self._callback(self._action)


class Animation:
    def __init__(self, painter):
        self._current_action = None
        self._start_timestamp = 0
        self._painter = painter

    def start_game(self, callback):
        self._new_action()
        self._current_action = ActionWait(callback, 800)

    def animate_move(self, action, callback):
        self._new_action()
        self._current_action = ActionMoveCard(self._painter, callback, action)

    def wait_before_next_turn(self, callback):
        self._new_action()
        self._current_action = ActionWait(callback, 500)

    def ai_thinking(self, callback):
        self._new_action()
        self._current_action = ActionWait(callback, 800)

    def tick(self):
        if not self._current_action:
            return

        action = self._current_action
        now = pygame.time.get_ticks()
        elapsed = now - self._start_timestamp
        elapsed = min(elapsed, action.duration)
        action.update(elapsed)
        if elapsed >= action.duration:
            self._current_action = None
            action.finished()

    def _new_action(self):
        self._start_timestamp = pygame.time.get_ticks()

