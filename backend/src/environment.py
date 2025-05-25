import numpy as np
import random

class NetworkEnvironment:
    def __init__(self, num_nodes=10):
        self.num_nodes = num_nodes
        self.latency_matrix = np.random.uniform(1, 20, (num_nodes, num_nodes))
        self.throughput_matrix = np.random.uniform(10, 100, (num_nodes, num_nodes))
        self.packet_loss_matrix = np.random.uniform(0, 5, (num_nodes, num_nodes))
        np.fill_diagonal(self.latency_matrix, 0)
        np.fill_diagonal(self.throughput_matrix, 0)
        np.fill_diagonal(self.packet_loss_matrix, 0)
        self.anomaly_nodes = set()

    def introduce_anomaly(self):
        self.anomaly_nodes.clear()
        for i in range(self.num_nodes):
            if random.random() < 0.2:  # 20% chance per node
                self.anomaly_nodes.add(i)
                self.latency_matrix[i, :] *= 2
                self.throughput_matrix[i, :] *= 0.5
                self.packet_loss_matrix[i, :] *= 2

    def reset_anomaly(self):
        for i in self.anomaly_nodes:
            self.latency_matrix[i, :] /= 2
            self.throughput_matrix[i, :] /= 0.5
            self.packet_loss_matrix[i, :] /= 2
        self.anomaly_nodes.clear()

    def step(self, action, current_node):
        self.reset_anomaly()
        self.introduce_anomaly()
        latency = self.latency_matrix[current_node, action]
        throughput = self.throughput_matrix[current_node, action]
        packet_loss = self.packet_loss_matrix[current_node, action]
        reward = -latency + 0.1 * throughput - 10 * packet_loss
        if action in self.anomaly_nodes:
            reward -= 20
        state = self.get_state()
        return state, reward, action

    def get_state(self):
        return {
            'latency': self.latency_matrix.copy(),
            'throughput': self.throughput_matrix.copy(),
            'packet_loss': self.packet_loss_matrix.copy(),
            'anomaly_nodes': list(self.anomaly_nodes)
        }
