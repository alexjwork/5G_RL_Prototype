import numpy as np
import tensorflow as tf
from collections import deque
import random

class DQNAgent:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, input_dim=self.num_nodes * 3, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(self.num_nodes, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return model

    def act(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.num_nodes)
        state_array = np.concatenate([state['latency'].flatten(), state['throughput'].flatten(), state['packet_loss'].flatten()])
        q_values = self.model.predict(state_array.reshape(1, -1), verbose=0)
        return np.argmax(q_values[0])

    def remember(self, state, action, reward, next_state, next_node):
        self.memory.append((state, action, reward, next_state, next_node))

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, next_node in minibatch:
            state_array = np.concatenate([state['latency'].flatten(), state['throughput'].flatten(), state['packet_loss'].flatten()])
            next_state_array = np.concatenate([next_state['latency'].flatten(), next_state['throughput'].flatten(), next_state['packet_loss'].flatten()])
            target = reward + self.gamma * np.amax(self.model.predict(next_state_array.reshape(1, -1), verbose=0)[0])
            target_f = self.model.predict(state_array.reshape(1, -1), verbose=0)
            target_f[0][action] = target
            self.model.fit(state_array.reshape(1, -1), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
