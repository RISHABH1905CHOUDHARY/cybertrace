"use client";

import { useState } from "react";
import {
  Brain,
  ShieldCheck,
  ShieldAlert,
  TrendingUp,
  TrendingDown,
  MapPin,
  Activity,
  RefreshCw,
  Search,
  Target,
  Zap,
} from "lucide-react";

const regions = [
  {
    region: "Delhi NCR",
    risk: 87,
    level: "Critical",
    threat: "Financial Fraud",
    confidence: 94,
  },
  {
    region: "Mumbai",
    risk: 76,
    level: "High",
    threat: "Phishing",
    confidence: 91,
  },
  {
    region: "Bengaluru",
    risk: 69,
    level: "High",
    threat: "Cyber Attack",
    confidence: 88,
  },
  {
    region: "Hyderabad",
    risk: 54,
    level: "Medium",
    threat: "Identity Theft",
    confidence: 84,
  },
  {
    region: "Bhopal",
    risk: 42,
    level: "Medium",
    threat: "Online Scam",
    confidence: 81,
  },
];

const trendData = [
  { day: "Mon", value: 48 },
  { day: "Tue", value: 55 },
  { day: "Wed", value: 51 },
  { day: "Thu", value: 63 },
  { day: "Fri", value: 68 },
  { day: "Sat", value: 74 },
  { day: "Sun", value: 71 },
];

const threats = [
  {
    name: "Financial Fraud",
    percentage: 82,
    change: "+14%",
    direction: "up",
  },
  {
    name: "Phishing",
    percentage: 71,
    change: "+9%",
    direction: "up",
  },
  {
    name: "Identity Theft",
    percentage: 56,
    change: "-4%",
    direction: "down",
  },
  {
    name: "Cyber Attack",
    percentage: 49,
    change: "+6%",
    direction: "up",
  },
];

export default function PredictionsPage() {
  const [regionsData, setRegionsData] = useState(regions);
  const [search, setSearch] = useState("");
  const [running, setRunning] = useState(false);
  const [lastUpdated, setLastUpdated] = useState("Just now");

  const runPrediction = () => {
  setRunning(true);

  setTimeout(() => {
    setRegionsData((current) =>
      current.map((region) => {
        const randomValues = new Uint32Array(1);
        crypto.getRandomValues(randomValues);

        const change = Number(randomValues[0] % 11) - 5;

        const newRisk = Math.max(
          20,
          Math.min(95, region.risk + change)
        );

        let newLevel = "Medium";

        if (newRisk >= 80) {
          newLevel = "Critical";
        } else if (newRisk >= 60) {
          newLevel = "High";
        }

        return {
          ...region,
          risk: newRisk,
          level: newLevel,
        };
      })
    );

    setLastUpdated("Just now");
    setRunning(false);
  }, 900);
};

  const filteredRegions = regionsData.filter((region) =>
    region.region.toLowerCase().includes(search.toLowerCase())
  );

  const averageRisk = Math.round(
    regionsData.reduce((total, region) => total + region.risk, 0) /
      regionsData.length
  );

  let overallLevel = "Medium";

  if (averageRisk >= 80) {
    overallLevel = "Critical";
  } else if (averageRisk >= 60) {
    overallLevel = "High";
  }

  return (
    <main className="predictions-page">

      {/* HEADER */}
      <section className="predictions-header">

        <div className="prediction-heading">

          <div className="prediction-title-icon">
            <Brain size={27} />
          </div>

          <div>
            <div className="prediction-label">
              AI THREAT INTELLIGENCE
            </div>

            <h1>Crime Predictions</h1>

            <p>
              AI-powered analysis of emerging cybercrime risks
              across regions.
            </p>
          </div>

        </div>

        <button
          type="button"
          className="run-prediction-btn"
          onClick={runPrediction}
          disabled={running}
        >
          <RefreshCw
            size={17}
            className={running ? "spin-icon" : ""}
          />

          {running ? "Analyzing..." : "Run New Prediction"}
        </button>

      </section>

      {/* TOP CARDS */}
      <section className="prediction-overview">

        <div className="prediction-score-card">

          <div className="score-top">

            <div>
              <span className="card-label">
                OVERALL RISK SCORE
              </span>

              <div className="big-risk-score">
                {averageRisk}
                <small>/100</small>
              </div>
            </div>

            <div className="score-shield">
              <Target size={25} />
            </div>

          </div>

          <div className="risk-progress">
            <div
              className="risk-progress-fill"
              style={{ width: `${averageRisk}%` }}
            ></div>
          </div>

          <div className="score-bottom">
            <span>Current threat level</span>

            <strong className={`prediction-level ${overallLevel.toLowerCase()}`}>
              {overallLevel}
            </strong>
          </div>

        </div>

        <div className="prediction-mini-card">

          <div className="mini-card-icon">
            <ShieldAlert size={22} />
          </div>

          <div>
            <span>High Risk Regions</span>
            <strong>
              {regionsData.filter(
                (region) =>
                  region.level === "High" ||
                  region.level === "Critical"
              ).length}
            </strong>

            <small>
              <TrendingUp size={13} />
              Areas requiring attention
            </small>
          </div>

        </div>

        <div className="prediction-mini-card">

          <div className="mini-card-icon confidence">
            <Brain size={22} />
          </div>

          <div>
            <span>Model Confidence</span>
            <strong>91%</strong>

            <small>
              <ShieldCheck size={13} />
              High confidence
            </small>
          </div>

        </div>

        <div className="prediction-mini-card">

          <div className="mini-card-icon active">
            <Activity size={22} />
          </div>

          <div>
            <span>Prediction Status</span>
            <strong>Active</strong>

            <small>
              <Zap size={13} />
              Updated {lastUpdated}
            </small>
          </div>

        </div>

      </section>

      {/* MAIN GRID */}
      <section className="prediction-main-grid">

        {/* TREND */}
        <div className="prediction-panel trend-panel">

          <div className="panel-heading">

            <div>
              <h2>Threat Risk Trend</h2>
              <p>Predicted threat intensity over the last 7 days.</p>
            </div>

            <div className="trend-indicator">
              <TrendingUp size={15} />
              +18.4%
            </div>

          </div>

          <div className="trend-chart">

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

              <div className="chart-bars">

                {trendData.map((item) => (
                  <div className="chart-column" key={item.day}>

                    <div className="chart-value">
                      {item.value}
                    </div>

                    <div
                      className="chart-bar"
                      style={{
                        height: `${item.value}%`,
                      }}
                    ></div>

                    <span>{item.day}</span>

                  </div>
                ))}

              </div>

            </div>

          </div>

        </div>

        {/* THREAT CATEGORIES */}
        <div className="prediction-panel">

          <div className="panel-heading">

            <div>
              <h2>Threat Categories</h2>
              <p>Predicted probability by threat type.</p>
            </div>

          </div>

          <div className="threat-list">

            {threats.map((threat) => (
              <div className="threat-item" key={threat.name}>

                <div className="threat-name-row">
                  <span>{threat.name}</span>

                  <strong>
                    {threat.percentage}%
                  </strong>
                </div>

                <div className="threat-progress">
                  <div
                    style={{
                      width: `${threat.percentage}%`,
                    }}
                  ></div>
                </div>

                <div
                  className={`threat-change ${threat.direction}`}
                >
                  {threat.direction === "up" ? (
                    <TrendingUp size={13} />
                  ) : (
                    <TrendingDown size={13} />
                  )}

                  {threat.change} from previous period
                </div>

              </div>
            ))}

          </div>

        </div>

      </section>

      {/* REGIONAL PREDICTIONS */}
      <section className="prediction-panel regional-panel">

        <div className="regional-header">

          <div>
            <h2>Regional Risk Predictions</h2>

            <p>
              AI-generated risk assessment by geographic region.
            </p>
          </div>

          <div className="region-search">
            <Search size={16} />

            <input
              type="text"
              placeholder="Search region..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

        </div>

        <div className="prediction-table">

          <div className="table-head">
            <span>Region</span>
            <span>Risk Score</span>
            <span>Threat Level</span>
            <span>Predicted Threat</span>
            <span>Confidence</span>
          </div>

          {filteredRegions.map((region) => (
            <div className="table-row" key={region.region}>

              <div className="region-name">
                <div className="region-icon">
                  <MapPin size={16} />
                </div>

                <strong>{region.region}</strong>
              </div>

              <div className="table-risk">

                <div className="small-risk-bar">
                  <div
                    style={{
                      width: `${region.risk}%`,
                    }}
                  ></div>
                </div>

                <strong>{region.risk}</strong>

              </div>

              <div>
                <span
                  className={`table-level ${region.level.toLowerCase()}`}
                >
                  {region.level}
                </span>
              </div>

              <div className="predicted-threat">
                {region.threat}
              </div>

              <div className="confidence-value">
                {region.confidence}%
              </div>

            </div>
          ))}

        </div>

      </section>

      {/* FOOTER INFO */}
      <section className="prediction-footer-info">

        <div>
          <ShieldCheck size={18} />

          <span>
            Prediction engine is operating normally
          </span>
        </div>

        <span>
          Model: CYBERTRACE-AI v2.4
        </span>

      </section>

    </main>
  );
}