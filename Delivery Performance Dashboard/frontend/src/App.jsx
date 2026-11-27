
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

const COLORS = ['#3B82F6', '#EF4444', '#60A5FA'];
const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [regionalData, setRegionalData] = useState([]);
  const [deliveryStatusData, setDeliveryStatusData] = useState([]);
  const [totalDeliveries, setTotalDeliveries] = useState(0);
  const [regions, setRegions] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState('All');

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Fetch available regions
  useEffect(() => {
    fetch(`${API_URL}/api/regions`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Unable to load regions.');
        }
        return response.json();
      })
      .then((data) => {
        setRegions(data);
      })
      .catch((error) => {
        console.error('Error fetching regions:', error);
        setError('Unable to load dashboard regions.');
      });
  }, []);

  // Fetch dashboard data when region changes
  useEffect(() => {
    const regionParameter = encodeURIComponent(selectedRegion);

    const fetchDashboardData = async () => {
      setLoading(true);
      setError('');

      try {
        const [totalResponse, statusResponse, regionalResponse] =
          await Promise.all([
            fetch(
              `${API_URL}/api/total-deliveries?region=${regionParameter}`
            ),
            fetch(
              `${API_URL}/api/delivery-status?region=${regionParameter}`
            ),
            fetch(
              `${API_URL}/api/regional-performance?region=${regionParameter}`
            )
          ]);

        if (
          !totalResponse.ok ||
          !statusResponse.ok ||
          !regionalResponse.ok
        ) {
          throw new Error('Unable to fetch dashboard data.');
        }

        const totalData = await totalResponse.json();
        const statusData = await statusResponse.json();
        const regionalResult = await regionalResponse.json();

        if (
          !Array.isArray(statusData) ||
          !Array.isArray(regionalResult)
        ) {
          throw new Error('The API returned invalid dashboard data.');
        }

        setTotalDeliveries(totalData.total_deliveries || 0);
        setDeliveryStatusData(statusData);
        setRegionalData(regionalResult);
      } catch (error) {
        console.error('Dashboard data error:', error);
        setError(
          'Unable to load dashboard data. Please check that the backend is running.'
        );
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [selectedRegion]);

  const getStatusCount = (status) => {
    const result = deliveryStatusData.find(
      (item) => item.name === status
    );

    return result ? result.value : 0;
  };

  const deliveredCount = getStatusCount('Delivered');
  const delayedCount = getStatusCount('Delayed');
  const failedCount = getStatusCount('Failed');

  const delayRate =
    totalDeliveries > 0
      ? ((delayedCount / totalDeliveries) * 100).toFixed(1)
      : '0.0';

  const successRate =
    totalDeliveries > 0
      ? ((deliveredCount / totalDeliveries) * 100).toFixed(1)
      : '0.0';

  const highestStatus = [...deliveryStatusData].sort(
    (a, b) => b.value - a.value
  )[0];

  const regionLabel =
    selectedRegion === 'All'
      ? 'All Regions'
      : selectedRegion.charAt(0).toUpperCase() +
        selectedRegion.slice(1);

  const formatNumber = (value) =>
    Number(value).toLocaleString('en-IN');

  const formatRegion = (region) =>
    region
      ? region.charAt(0).toUpperCase() + region.slice(1)
      : '';

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

        {/* Region Filter */}
        <div className="filter-container">
          <label htmlFor="region-filter">
            Filter by Region:
          </label>

          <select
            id="region-filter"
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            disabled={loading}
          >
            <option value="All">All Regions</option>

            {regions.map((region) => (
              <option key={region} value={region}>
                {formatRegion(region)}
              </option>
            ))}
          </select>
        </div>

        {/* Loading and Error Messages */}
        {loading && (
          <div className="status-message">
            Loading dashboard data...
          </div>
        )}

        {error && !loading && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Dashboard Content */}
        {!loading && !error && (
          <>
            {/* KPI Cards */}
            <section className="kpi-grid">

              <div className="kpi-card">
                <p>Total Deliveries</p>
                <h2>{formatNumber(totalDeliveries)}</h2>
                <span>{regionLabel}</span>
              </div>

              <div className="kpi-card">
                <p>Delivered</p>
                <h2>{formatNumber(deliveredCount)}</h2>
                <span>Successful deliveries</span>
              </div>

              <div className="kpi-card">
                <p>Delayed</p>
                <h2>{formatNumber(delayedCount)}</h2>
                <span>Delayed deliveries</span>
              </div>

              <div className="kpi-card">
                <p>Failed</p>
                <h2>{formatNumber(failedCount)}</h2>
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
                            fill={COLORS[index % COLORS.length]}
                          />
                        ))}
                      </Pie>

                      <Tooltip
                        formatter={(value, name) => [
                          formatNumber(value),
                          name
                        ]}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Regional Performance */}
              <div className="chart-card">
                <h3>Regional Performance</h3>
                <p>
                  {selectedRegion === 'All'
                    ? 'Delivery volume by region'
                    : `Delivery volume for ${regionLabel}`}
                </p>

                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={regionalData}
                    margin={{
                      top: 10,
                      right: 10,
                      left: 10,
                      bottom: 5
                    }}
                  >
                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                    />

                    <XAxis
                      dataKey="region"
                      tickFormatter={formatRegion}
                    />

                    <YAxis tickFormatter={formatNumber} />

                    <Tooltip
                      formatter={(value) => [
                        formatNumber(value),
                        'Total Deliveries'
                      ]}
                      labelFormatter={formatRegion}
                    />

                    <Bar
                      dataKey="total_deliveries"
                      name="Total Deliveries"
                      fill="#333333"
                      radius={[5, 5, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>

            </section>

            {/* Quick Insights */}
            <section
              className="bottom-card"
              style={{ marginTop: '24px' }}
            >
              <h3>Quick Insights</h3>
              <p>
                Automatically calculated insights for {regionLabel}.
              </p>

              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns:
                    'repeat(auto-fit, minmax(180px, 1fr))',
                  gap: '16px',
                  marginTop: '20px'
                }}
              >
                <div
                  style={{
                    background: '#f5f5f5',
                    padding: '18px',
                    borderRadius: '10px'
                  }}
                >
                  <p style={{ color: '#666', margin: 0 }}>
                    Highest Delivery Status
                  </p>

                  <h2 style={{ margin: '10px 0' }}>
                    {highestStatus
                      ? highestStatus.name
                      : 'No Data'}
                  </h2>

                  <span style={{ color: '#666' }}>
                    {highestStatus
                      ? `${formatNumber(highestStatus.value)} deliveries`
                      : 'No delivery records'}
                  </span>
                </div>

                <div
                  style={{
                    background: '#f5f5f5',
                    padding: '18px',
                    borderRadius: '10px'
                  }}
                >
                  <p style={{ color: '#666', margin: 0 }}>
                    Delay Rate
                  </p>

                  <h2 style={{ margin: '10px 0' }}>
                    {delayRate}%
                  </h2>

                  <span style={{ color: '#666' }}>
                    Of total deliveries
                  </span>
                </div>

                <div
                  style={{
                    background: '#f5f5f5',
                    padding: '18px',
                    borderRadius: '10px'
                  }}
                >
                  <p style={{ color: '#666', margin: 0 }}>
                    Delivery Success Rate
                  </p>

                  <h2 style={{ margin: '10px 0' }}>
                    {successRate}%
                  </h2>

                  <span style={{ color: '#666' }}>
                    Successfully delivered
                  </span>
                </div>
              </div>
            </section>
          </>
        )}

      </main>
    </div>
  );
}

export default App;
