const ctxReward = document.getElementById('rewardChart').getContext('2d');
const ctxLatency = document.getElementById('latencyChart').getContext('2d');
const ctxThroughput = document.getElementById('throughputChart').getContext('2d');
const ctxPacketLoss = document.getElementById('packetLossChart').getContext('2d');

const rewardChart = new Chart(ctxReward, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Reward', data: [], borderColor: '#4CAF50', fill: false }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'Cumulative Reward' } } }
});
const latencyChart = new Chart(ctxLatency, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Avg Latency (ms)', data: [], borderColor: '#2196F3', fill: false }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'Average Latency' } } }
});
const throughputChart = new Chart(ctxThroughput, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Avg Throughput (Mbps)', data: [], borderColor: '#FF9800', fill: false }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'Average Throughput' } } }
});
const packetLossChart = new Chart(ctxPacketLoss, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Avg Packet Loss (%)', data: [], borderColor: '#F44336', fill: false }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { title: { display: true, text: 'Average Packet Loss' } } }
});

const nodes = new vis.DataSet(Array.from({ length: 10 }, (_, i) => ({ id: i, label: `Node ${i}` })));
const edges = new vis.DataSet([]);
const container = document.getElementById('network');
const network = new vis.Network(container, { nodes, edges }, {
    physics: { enabled: true },
    edges: { arrows: 'to', smooth: { type: 'continuous' } }
});

let episode = 0;
const maxEpisodes = 100;

function updateDashboard() {
    fetch('../backend/data/network_data.json')
        .then(response => response.json())
        .then(data => {
            if (episode >= maxEpisodes) {
                document.getElementById('status').textContent = 'Status: Training Complete';
                return;
            }

            rewardChart.data.labels.push(data.episode);
            rewardChart.data.datasets[0].data.push(data.reward);
            latencyChart.data.labels.push(data.episode);
            latencyChart.data.datasets[0].data.push(data.avg_latency);
            throughputChart.data.labels.push(data.episode);
            throughputChart.data.datasets[0].data.push(data.avg_throughput);
            packetLossChart.data.labels.push(data.episode);
            packetLossChart.data.datasets[0].data.push(data.avg_packet_loss);

            rewardChart.update();
            latencyChart.update();
            throughputChart.update();
            packetLossChart.update();

            const tableBody = document.getElementById('metrics-table-body');
            tableBody.innerHTML = '';
            data.nodes.forEach(node => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${node.id}</td>
                    <td>${node.latency.toFixed(2)}</td>
                    <td>${node.throughput.toFixed(2)}</td>
                    <td>${node.packet_loss.toFixed(2)}</td>
                    <td>${node.anomaly ? 'Yes' : 'No'}</td>
                `;
                tableBody.appendChild(row);
            });

            edges.clear();
            edges.add(data.edges);
            network.setData({ nodes, edges });

            document.getElementById('status').textContent = `Status: Training Episode ${data.episode + 1}/${maxEpisodes}`;
            episode++;

            setTimeout(updateDashboard, 1000);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('status').textContent = 'Status: Error fetching data';
            setTimeout(updateDashboard, 1000);
        });
}

updateDashboard();
