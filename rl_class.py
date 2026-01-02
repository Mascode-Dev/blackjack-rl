import numpy as np
import random

class BlackjackEnv:
    def __init__(self):
        self.card_value = {
            "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, 
            "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":11
        }
        self.reset()

    def _card_initialization(self):
        list_of_cards_available = [
            "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
        ]
        list_flush = ["♥", "♦", "♣", "♠"]
        list_cards = []
        for i in list_of_cards_available:
            for j in list_flush:
                list_cards.append(f"{i} {j}")
        return list_cards

    def reset(self):
        """Reset the game and return the initial state."""
        self.deck = self._card_initialization()
        self.player_hand, _, self.deck = self._give_card(self.deck, 2)
        self.dealer_hand, _, self.deck = self._give_card(self.deck, 1)
        return self._get_obs()

    def _get_obs(self):
        """Return the state: (Player sum, Dealer card, Usable ace)."""
        # Simplify the score for the AI (best score <= 21)
        res = self._compute_best_score(self.player_hand)
        return (res['score'], self.card_value[self.dealer_hand[0].split(" ")[0]], res['usable_ace'])

    def _give_card(self, deck, nb):
        """Deal 'nb' cards from the deck and return hand, score and updated deck."""
        hand = []
        for _ in range(nb):
            card = deck[random.randint(0, len(deck)-1)]
            deck.remove(card)
            hand.append(card)
        return hand, self._compute_best_score(hand), deck
    
    def _add_card(self, hand, deck):
        """Add a card to the hand and return updated hand, deck and score."""
        card = deck[random.randint(0, len(deck)-1)]
        hand.append(card)
        deck.remove(card)
        return hand, deck, self._compute_best_score(hand)
    
    def step(self, action):
        """
        Action 0: Stand, Action 1: Hit
        Return: (new state, reward, done)
        """
        if action == 1: # HIT
            self.player_hand, self.deck, _ = self._add_card(self.player_hand, self.deck)
            score = self._compute_best_score(self.player_hand)['score']
            if score > 21:
                return self._get_obs(), -1, True # Lost
            else:
                return self._get_obs(), 0, False
        
        else: # STAND

            while self._compute_best_score(self.dealer_hand)['score'] < 17:
                self.dealer_hand, self.deck, _ = self._add_card(self.dealer_hand, self.deck)

            player_score = self._compute_best_score(self.player_hand)['score']
            dealer_score = self._compute_best_score(self.dealer_hand)['score']

            if dealer_score > 21 or player_score > dealer_score:
                reward = 1  # Win
            elif player_score < dealer_score:
                reward = -1 # Lost
            else:
                reward = 0  # Draw

            return self._get_obs(), reward, True
        
    def _compute_best_score(self, hand):
        """
        Calculate the best possible score for a given hand.
        Returns a dictionary with the score and a boolean for usable ace.
        """
        score = 0
        aces = 0
        
        # First pass: count base scores (Ace = 11)
        for card in hand:
            card_name = card.split(" ")[0]
            val = self.card_value[card_name]
            score += val
            if card_name == "A":
                aces += 1
        
        # Second pass: if over 21, convert Aces (11 -> 1)
        usable_ace = False
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        
        # Check if there is at least one Ace counted as 11
        # This is crucial information for the AI strategy
        if aces > 0 and score <= 21:
            usable_ace = True
            
        return {"score": score, "usable_ace": usable_ace}
    
class QLearningAgent:
    def __init__(self, epsilon=0.1, lr=0.01, gamma=0.95, epsilon_decay=0.99995):
        self.q_table = {} # (state): [value_stand, value_hit]
        self.epsilon = epsilon
        self.lr = lr
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay # Decay rate per episode
        self.min_lr = 0.001
        self.min_epsilon = 0.01

    def get_action(self, state):
        # Exploration vs Exploitation
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, 1) # Random
        return np.argmax(self.q_table.get(state, [0, 0])) # Best action

    def learn(self, state, action, reward, next_state, done):
        """Update Q-value based on the action taken and the reward received."""
        old_value = self.q_table.get(state, [0, 0])[action]
        next_max = np.max(self.q_table.get(next_state, [0, 0])) # Max Q-value for next state
        
        # Bellman equation - Q-learning update
        new_value = old_value + self.lr * (reward + self.gamma * next_max - old_value)
        
        if state not in self.q_table:
            self.q_table[state] = [0, 0] # Initialize if not present
        self.q_table[state][action] = new_value # Update Q-value

        if done:
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
            self.lr = max(self.min_lr, self.lr * self.epsilon_decay)