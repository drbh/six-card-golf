from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def flip_initial_cards(self, hand):
        pass
