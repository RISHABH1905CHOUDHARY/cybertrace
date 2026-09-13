"use client";

import { useState } from "react";
import {
  BarChart3,
  Activity,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
  TrendingDown,
  MapPin,
  RefreshCw,
  Download,
  CalendarDays,
  Target,
  Zap,
} from "lucide-react";

const regions = [
  {
    name: "Delhi NCR",
    incidents: 428,
    risk: 87,
    change: 14,
  },
  {
    name: "Mumbai",
    incidents: 361,
    risk: 76,
    change: 9,
  },
  {
    name: "Bengaluru",
    incidents: 294,
    risk: 69,
    change: -3,
  },
  {
    name: "Hyderabad",
    incidents: 217,
    risk: 54,
    change: 6,
  },
  {
    name: "Bhopal",
    incidents: 142,
    risk: 42,
    change: -5,
  },
];

const fraudCategories = [
  {
    name: "Financial Fraud",
    value: 34,
    count: 626,
  },
  {
    name: "Phishing",
    value: 26,
    count: 479,
  },
  {
    name: "Identity Theft",
    value: 18,
    count: 332,
  },
  {
    name: "Online Scam",
    value: 13,
    count: 239,
  },
  {
    name: "Cyber Attack",
    value: 9,
    count: 166,
  },
];

const activityData = [
  42, 55, 48, 67, 59, 74, 68,
  81, 72, 88, 79, 92, 84, 96,
];

export default function AnalyticsPage() {
  const [period, setPeriod] = useState("Last 30 Days");
  const [refreshing, setRefreshing] = useState(false);

  const refreshAnalytics = () => {
    setRefreshing(true);

    setTimeout(() => {
      setRefreshing(false);
    }, 900);
  };

  const exportAnalytics = () => {
    const rows = [
      ["Region", "Incidents", "Risk Score", "Change"],
      ...regions.map((region) => [
        region.name,
        region.incidents,
        region.risk,
        `${region.change}%`,
      ]),
    ];

    const csv = rows
      .map((row) =>
        row.map((value) => `${value}`).join(",")
      )
      .join("\n");

    const blob = new Blob([csv], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "cybertrace-analytics.csv";

   document.body.appendChild(link);
link.click();
link.remove();

URL.revokeObjectURL(url);
  };

  return (
    <main className="analytics-page">

      {/* HEADER */}
      <section className="analytics-header">

        <div className="analytics-heading">

          <div className="analytics-title-icon">
            <BarChart3 size={27} />
          </div>

          <div>
            <span className="analytics-label">
              CYBERTRACE INTELLIGENCE CENTER
            </span>

            <h1>Security Analytics</h1>

            <p>
              Real-time cybercrime intelligence,
              trends and regional risk analysis.
            </p>
          </div>

        </div>

        <div className="analytics-actions">

          <div className="analytics-period">
            <CalendarDays size={15} />

            <select
              value={period}
              onChange={(event) =>
                setPeriod(event.target.value)
              }
            >
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
              <option>Last 90 Days</option>
              <option>This Year</option>
            </select>
          </div>

          <button
            type="button"
            className="analytics-action-btn"
            onClick={exportAnalytics}
          >
            <Download size={16} />
            Export
          </button>

          <button
            type="button"
            className="analytics-refresh-btn"
            onClick={refreshAnalytics}
            disabled={refreshing}
          >
            <RefreshCw
              size={16}
              className={
                refreshing ? "analytics-spin" : ""
              }
            />

            {refreshing ? "Refreshing..." : "Refresh"}
          </button>

        </div>

      </section>

      {/* KPI CARDS */}
      <section className="analytics-kpis">

        <div className="analytics-kpi-card">

          <div className="analytics-kpi-icon blue">
            <Activity size={21} />
          </div>

          <div className="analytics-kpi-content">
            <span>Total Incidents</span>

            <strong>1,842</strong>

            <small className="positive">
              <TrendingUp size={12} />
              12.4% vs previous period
            </small>
          </div>

        </div>

        <div className="analytics-kpi-card">

          <div className="analytics-kpi-icon red">
            <ShieldAlert size={21} />
          </div>

          <div className="analytics-kpi-content">
            <span>Critical Threats</span>

            <strong>128</strong>

            <small className="negative">
              <TrendingUp size={12} />
              8.2% increase
            </small>
          </div>

        </div>

        <div className="analytics-kpi-card">

          <div className="analytics-kpi-icon orange">
            <Target size={21} />
          </div>

          <div className="analytics-kpi-content">
            <span>Detection Accuracy</span>

            <strong>94.7%</strong>

            <small className="positive">
              <TrendingUp size={12} />
              3.8% improvement
            </small>
          </div>

        </div>

        <div className="analytics-kpi-card">

          <div className="analytics-kpi-icon green">
            <ShieldCheck size={21} />
          </div>

          <div className="analytics-kpi-content">
            <span>Threats Resolved</span>

            <strong>81.6%</strong>

            <small className="positive">
              <TrendingUp size={12} />
              5.2% improvement
            </small>
          </div>

        </div>

      </section>

      {/* TOP ANALYTICS */}
      <section className="analytics-main-grid">

        {/* THREAT ACTIVITY */}
        <div className="analytics-panel activity-panel">

          <div className="analytics-panel-header">

            <div>
              <h2>Threat Activity</h2>

              <p>
                Cybercrime activity during {period.toLowerCase()}.
              </p>
            </div>

            <div className="live-indicator">
              <span>Live</span>
              
            </div>

          </div>

          <div className="activity-chart">

            <div className="chart-y-axis">
              <span>100</span>
              <span>75</span>
              <span>50</span>
              <span>25</span>
              <span>0</span>
            </div>

            <div className="chart-area">

              <div className="chart-grid-line line-1"></div>
              <div className="chart-grid-line line-2"></div>
              <div className="chart-grid-line line-3"></div>
              <div className="chart-grid-line line-4"></div>

              <div className="bar-chart">

                {activityData.map((value, index) => (
                  <div
                    className="activity-bar-wrapper"
                    key={`${value}-${index}`}
                  >
                    <div
                      className="activity-bar"
                      style={{
                        height: `${value}%`,
                      }}
                      title={`${value} incidents`}
                    ></div>

                    <span>
                      {index + 1}
                    </span>
                  </div>
                ))}

              </div>

            </div>

          </div>

        </div>

        {/* RISK DISTRIBUTION */}
        <div className="analytics-panel">

          <div className="analytics-panel-header">

            <div>
              <h2>Risk Distribution</h2>

              <p>
                Current threat severity breakdown.
              </p>
            </div>

            <ShieldAlert size={18} />

          </div>

          <div className="risk-distribution">

            <div className="risk-ring">

              <div className="risk-ring-center">
                <strong>72</strong>
                <span>Risk Score</span>
              </div>

            </div>

            <div className="risk-legend">

              <div>
                <span className="risk-dot critical"></span>
                <span>Critical</span>
                <strong>7%</strong>
              </div>

              <div>
                <span className="risk-dot high"></span>
                <span>High</span>
                <strong>28%</strong>
              </div>

              <div>
                <span className="risk-dot medium"></span>
                <span>Medium</span>
                <strong>41%</strong>
              </div>

              <div>
                <span className="risk-dot low"></span>
                <span>Low</span>
                <strong>24%</strong>
              </div>

            </div>

          </div>

          <div className="risk-warning">

            <Zap size={15} />

            <p>
              National risk remains above the
              recommended safety threshold.
            </p>

          </div>

        </div>

      </section>

      {/* SECOND ROW */}
      <section className="analytics-secondary-grid">

        {/* FRAUD CATEGORIES */}
        <div className="analytics-panel">

          <div className="analytics-panel-header">

            <div>
              <h2>Fraud Categories</h2>

              <p>
                Distribution of reported cybercrime types.
              </p>
            </div>

            <BarChart3 size={18} />

          </div>

          <div className="fraud-category-list">

            {fraudCategories.map((category) => (

              <div
                className="fraud-category"
                key={category.name}
              >

                <div className="fraud-category-top">

                  <span>{category.name}</span>

                  <strong>
                    {category.count}
                  </strong>

                </div>

                <div className="fraud-progress">

                  <div
                    style={{
                      width: `${category.value}%`,
                    }}
                  ></div>

                </div>

                <div className="fraud-category-bottom">
                  <span>{category.value}% of incidents</span>
                </div>

              </div>

            ))}

          </div>

        </div>

        {/* DETECTION PERFORMANCE */}
        <div className="analytics-panel">

          <div className="analytics-panel-header">

            <div>
              <h2>Detection Performance</h2>

              <p>
                CYBERTRACE prediction engine performance.
              </p>
            </div>

            <Target size={18} />

          </div>

          <div className="performance-score">

            <div className="performance-circle">

              <div>
                <strong>94.7</strong>
                <span>%</span>
              </div>

            </div>

            <div>
              <span>Overall Accuracy</span>

              <strong className="performance-good">
                Excellent
              </strong>
            </div>

          </div>

          <div className="performance-metrics">

            <div>
              <span>Precision</span>
              <strong>93.2%</strong>
            </div>

            <div>
              <span>Recall</span>
              <strong>91.8%</strong>
            </div>

            <div>
              <span>F1 Score</span>
              <strong>92.5%</strong>
            </div>

            <div>
              <span>False Positive</span>
              <strong>2.4%</strong>
            </div>

          </div>

        </div>

      </section>

      {/* REGIONAL ANALYSIS */}
      <section className="analytics-panel regional-analytics">

        <div className="analytics-panel-header">

          <div>
            <h2>Regional Threat Analysis</h2>

            <p>
              Compare incident volume and predicted
              cybercrime risk across regions.
            </p>
          </div>

          <MapPin size={18} />

        </div>

        <div className="regional-table">

          <div className="regional-table-header">
            <span>Region</span>
            <span>Incidents</span>
            <span>Risk Score</span>
            <span>Risk Level</span>
            <span>Trend</span>
          </div>

          {regions.map((region) => {

            let riskLevel = "Medium";

if (region.risk >= 80) {
  riskLevel = "Critical";
} else if (region.risk >= 60) {
  riskLevel = "High";
}

            return (
              <div
                className="regional-table-row"
                key={region.name}
              >

                <div className="region-name">

                  <div className="region-icon">
                    <MapPin size={14} />
                  </div>

                  <strong>{region.name}</strong>

                </div>

                <strong className="incident-number">
                  {region.incidents}
                </strong>

                <div className="regional-score">

                  <div className="regional-score-top">
                    <span>{region.risk}/100</span>
                  </div>

                  <div className="regional-progress">
                    <div
                      style={{
                        width: `${region.risk}%`,
                      }}
                    ></div>
                  </div>

                </div>

                <span
                  className={`regional-risk ${riskLevel.toLowerCase()}`}
                >
                  {riskLevel}
                </span>

                <div
                  className={`regional-trend ${
                    region.change >= 0
                      ? "up"
                      : "down"
                  }`}
                >
                  {region.change >= 0 ? (
                    <TrendingUp size={13} />
                  ) : (
                    <TrendingDown size={13} />
                  )}

                  `{Math.abs(region.change)}%`
                </div>

              </div>
            );
          })}

        </div>

      </section>

      {/* BOTTOM INSIGHT */}
      <section className="analytics-insight">

        <div className="insight-icon">
          <Activity size={19} />
        </div>

        <div>
          <span>AI SECURITY INSIGHT</span>

          <h3>
            Financial fraud is currently the
            dominant cybercrime pattern.
          </h3>

          <p>
            Delhi NCR has the highest predicted regional
            risk. Increased monitoring of financial
            transactions and phishing activity is recommended.
          </p>
        </div>

      </section>

    </main>
  );
}