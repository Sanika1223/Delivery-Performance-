
import './App.css';
import { useEffect, useState } from 'react';

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts';

const COLORS = ['#171717', '#737373', '#d4d4d4'];

function App() {
  const [regionalData, setRegionalData] = useState([]);
  const [deliveryStatusData, setDeliveryStatusData] = useState([]);

useEffect(() => {
  fetch('http://127.0.0.1:8000/api/regional-performance')
    .then((response) => response.json())
    .then((data) => setRegionalData(data))
    .catch((error) => console.error('Error fetching regional data:', error));

  fetch('http://127.0.0.1:8000/api/delivery-status')
    .then((response) => response.json())
    .then((data) => setDeliveryStatusData(data))
    .catch((error) => console.error('Error fetching delivery status:', error));
}, []);
  return (
    <div className="dashboard">

      {/* Sidebar */}
      <aside className="sidebar">
        <h2>
          Delivery<span>Flow</span>
        </h2>

        <nav>
          <a className="active" href="#">Dashboard</a>
          <a href="#">Deliveries</a>
          <a href="#">Partners</a>
          <a href="#">Regions</a>
        </nav>

        <div className="sidebar-bottom">
          <p>Delivery Analytics</p>
          <small>Data Analyst Project</small>
        </div>
      </aside>

      {/* Main Dashboard */}
      <main className="main-content">

        {/* Header */}
        <header className="topbar">
          <div>
            <h1>Delivery Performance</h1>
            <p>Monitor and analyze delivery operations</p>
          </div>

          <div className="date-label">
            DATA OVERVIEW
          </div>
        </header>

        {/* KPI Cards */}
        <section className="kpi-grid">

          <div className="kpi-card">
            <p>Total Deliveries</p>
            <h2>25,000</h2>
            <span>All delivery records</span>
          </div>

          <div className="kpi-card">
            <p>Delivered</p>
            <h2>18,331</h2>
            <span>Successful deliveries</span>
          </div>

          <div className="kpi-card">
            <p>Delayed</p>
            <h2>5,341</h2>
            <span>Delayed deliveries</span>
          </div>

          <div className="kpi-card">
            <p>Failed</p>
            <h2>1,328</h2>
            <span>Failed deliveries</span>
          </div>

        </section>

        {/* Charts */}
        <section className="content-grid">

          {/* Delivery Status Pie Chart */}
          <div className="chart-card">
            <h3>Delivery Status</h3>
            <p>Distribution of delivery outcomes</p>

            <div className="chart-container">
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={deliveryStatusData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={65}
                    outerRadius={100}
                    paddingAngle={3}
                  >
                    {deliveryStatusData.map((entry, index) => (
                      <Cell
                        key={entry.name}
                        fill={COLORS[index]}
                      />
                    ))}
                  </Pie>

                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Regional Performance */}
<div className="chart-card">
  <h3>Regional Performance</h3>
  <p>Delivery volume by region</p>

  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={regionalData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="region" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="total_deliveries" fill="#333333" />
    </BarChart>
  </ResponsiveContainer>
</div>

        </section>

        {/* Delivery Insights */}
        <section className="bottom-card">
          <h3>Delivery Insights</h3>

          <p>
            Explore delivery status, partner performance,
            regional trends, and delivery costs.
          </p>
        </section>

      </main>
    </div>
  );
}

export default App;
