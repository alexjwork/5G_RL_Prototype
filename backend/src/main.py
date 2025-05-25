import json
from environment import NetworkEnvironment
from agent import DQNAgent

def train_dqn(episodes=100, batch_size=32):
    env = NetworkEnvironment(num_nodes=10)
    agent = DQNAgent(num_nodes=10)
    for episode in range(episodes):
        current_node = random.randint(0, 9)
        state = env.get_state()
        total_reward = 0
        for _ in range(10):
            action = agent.act(state)
            next_state, reward, next_node = env.step(action, current_node)
            agent.remember(state, action, reward, next_state, next_node)
            agent.replay(batch_size)
            total_reward += reward
            current_node = next_node
            state = next_state
        # Save data for frontend
        with open('backend/data/network_data.json', 'w') as f:
            json.dump({
                'episode': episode,
                'reward': total_reward,
                'avg_latency': float(np.mean(env.latency_matrix)),
                'avg_throughput': float(np.mean(env.throughput_matrix)),
                'avg_packet_loss': float(np.mean(env.packet_loss_matrix)),
                'nodes': [{'id': i, 'latency': float(np.mean(env.latency_matrix[i, :])), 'throughput': float(np.mean(env.throughput_matrix[i, :])), 'packet_loss': float(np.mean(env.packet_loss_matrix[i, :])), 'anomaly': i in env.anomaly_nodes} for i in range(10)],
                'edges': [{'from': i, 'to': j, 'width': float(env.throughput_matrix[i, j] / 20)} for i in range(10) for j in range(10) if i != j]
            }, f)

if __name__ == "__main__":
    train_dqn(episodes=100)
