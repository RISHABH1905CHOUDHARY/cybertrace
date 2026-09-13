 "use client";

import { useState } from "react";
import {
  FileText,
  Download,
  Printer,
  RefreshCw,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Activity,
  TrendingUp,
  MapPin,
  CalendarDays,
  CheckCircle2,
} from "lucide-react";

const reportData = [
  {
    id: "INC-1042",
    type: "Financial Fraud",
    location: "New Delhi",
    severity: "Critical",
    status: "Investigating",
    date: "12 Sep 2026",
  },
  {
    id: "INC-1041",
    type: "Phishing",
    location: "Mumbai",
    severity: "High",
    status: "Resolved",
    date: "12 Sep 2026",
  },
  {
    id: "INC-1040",
    type: "Identity Theft",
    location: "Bengaluru",
    severity: "High",
    status: "Investigating",
    date: "11 Sep 2026",
  },
  {
    id: "INC-1039",
    type: "Online Scam",
    location: "Bhopal",
    severity: "Medium",
    status: "Resolved",
    date: "11 Sep 2026",
  },
  {
    id: "INC-1038",
    type: "Cyber Attack",
    location: "Hyderabad",
    severity: "Medium",
    status: "Resolved",
    date: "10 Sep 2026",
  },
];

const regions = [
  { name: "Delhi NCR", incidents: 428, risk: 87 },
  { name: "Mumbai", incidents: 361, risk: 76 },
  { name: "Bengaluru", incidents: 294, risk: 69 },
  { name: "Hyderabad", incidents: 217, risk: 54 },
  { name: "Bhopal", incidents: 142, risk: 42 },
];

export default function ReportsPage() {
  const [reportType, setReportType] = useState("Security Overview");
  const [period, setPeriod] = useState("Last 30 Days");
  const [generated, setGenerated] = useState(false);

  const generateReport = () => {
    setGenerated(true);

    setTimeout(() => {
      setGenerated(false);
    }, 1800);
  };

  const exportCSV = () => {
    const headers = [
      "Incident ID",
      "Type",
      "Location",
      "Severity",
      "Status",
      "Date",
    ];

    const rows = reportData.map((report) => [
      report.id,
      report.type,
      report.location,
      report.severity,
      report.status,
      report.date,
    ]);

    const csv = [
      headers.join(","),
      ...rows.map((row) =>
        row.map((value) => "${value}").join(",")
      ),
    ].join("\n");

    const blob = new Blob([csv], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "cybertrace-security-report.csv";

   document.body.appendChild(link);
link.click();
link.remove();

URL.revokeObjectURL(url);
  };

  const printReport = () => {
    window.print();
  };

  return (
    <main className="reports-page">

      {/* HEADER */}
      <section className="reports-header">

        <div className="reports-heading">

          <div className="reports-title-icon">
            <FileText size={27} />
          </div>

          <div>
            <span className="reports-label">
              CYBERTRACE INTELLIGENCE CENTER
            </span>

            <h1>Security Reports</h1>

            <p>
              Generate, analyze and export comprehensive
              cybercrime intelligence reports.
            </p>
          </div>

        </div>

        <div className="report-actions">

          <button
            type="button"
            className="report-secondary-btn"
            onClick={printReport}
          >
            <Printer size={16} />
            Print
          </button>

          <button
            type="button"
            className="report-secondary-btn"
            onClick={exportCSV}
          >
            <Download size={16} />
            Export CSV
          </button>

          <button
            type="button"
            className="generate-report-btn"
            onClick={generateReport}
            disabled={generated}
          >
            <RefreshCw
              size={16}
              className={generated ? "report-spin" : ""}
            />

            {generated ? "Generating..." : "Generate Report"}
          </button>

        </div>

      </section>

      {/* REPORT CONFIGURATION */}
      <section className="report-config-panel">

        <div className="report-config-title">
          <FileText size={18} />

          <div>
            <h2>Report Configuration</h2>
            <p>Choose the information you want to analyze.</p>
          </div>
        </div>

        <div className="report-config-controls">

          <label>
            <span>Report Type</span>

            <select
              value={reportType}
              onChange={(event) =>
                setReportType(event.target.value)
              }
            >
              <option>Security Overview</option>
              <option>Threat Intelligence</option>
              <option>Regional Risk Analysis</option>
              <option>Complaint Analysis</option>
              <option>Incident Report</option>
            </select>
          </label>

          <label>
            <span>Reporting Period</span>

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
          </label>

          <div className="selected-period">
            <CalendarDays size={17} />

            <div>
              <span>Selected Period</span>
              <strong>{period}</strong>
            </div>
          </div>

        </div>

      </section>

      {/* SUMMARY */}
      <section className="report-summary">

        <div className="report-summary-card">
          <div className="summary-icon blue">
            <Activity size={21} />
          </div>

          <div>
            <span>Total Incidents</span>
            <strong>1,842</strong>
            <small>
              <TrendingUp size={12} />
              12.4% increase
            </small>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="summary-icon red">
            <ShieldAlert size={21} />
          </div>

          <div>
            <span>Critical Threats</span>
            <strong>128</strong>
            <small className="warning-text">
              Requires attention
            </small>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="summary-icon orange">
            <AlertTriangle size={21} />
          </div>

          <div>
            <span>Active Cases</span>
            <strong>347</strong>
            <small>
              Under investigation
            </small>
          </div>
        </div>

        <div className="report-summary-card">
          <div className="summary-icon green">
            <ShieldCheck size={21} />
          </div>

          <div>
            <span>Resolution Rate</span>
            <strong>81.6%</strong>
            <small>
              <TrendingUp size={12} />
              5.2% improvement
            </small>
          </div>
        </div>

      </section>

      {/* ANALYTICS GRID */}
      <section className="reports-analytics-grid">

        {/* THREAT DISTRIBUTION */}
        <div className="report-panel">

          <div className="report-panel-heading">
            <div>
              <h2>Threat Distribution</h2>
              <p>Reported incidents by category.</p>
            </div>

            <Activity size={18} />
          </div>

          <div className="distribution-content">

            <div className="donut-chart">
              <div className="donut-center">
                <strong>1,842</strong>
                <span>Incidents</span>
              </div>
            </div>

            <div className="distribution-list">

              <div>
                <span className="distribution-dot fraud"></span>
                <span>Financial Fraud</span>
                <strong>34%</strong>
              </div>

              <div>
                <span className="distribution-dot phishing"></span>
                <span>Phishing</span>
                <strong>26%</strong>
              </div>

              <div>
                <span className="distribution-dot identity"></span>
                <span>Identity Theft</span>
                <strong>18%</strong>
              </div>

              <div>
                <span className="distribution-dot scam"></span>
                <span>Online Scam</span>
                <strong>13%</strong>
              </div>

              <div>
                <span className="distribution-dot other"></span>
                <span>Other</span>
                <strong>9%</strong>
              </div>

            </div>

          </div>

        </div>

        {/* RISK OVERVIEW */}
        <div className="report-panel">

          <div className="report-panel-heading">
            <div>
              <h2>Risk Overview</h2>
              <p>Current national threat assessment.</p>
            </div>

            <ShieldAlert size={18} />
          </div>

          <div className="risk-overview">

            <div className="national-risk">
              <div className="national-risk-score">
                <span>72</span>
                <small>/100</small>
              </div>

              <div>
                <span>National Risk Level</span>
                <strong>HIGH</strong>
              </div>
            </div>

            <div className="risk-meter">
              <div className="risk-meter-fill"></div>
            </div>

            <div className="risk-scale">
              <span>Low</span>
              <span>Medium</span>
              <span>High</span>
              <span>Critical</span>
            </div>

            <div className="risk-note">
              <AlertTriangle size={16} />

              <p>
                Financial fraud and phishing are currently
                the dominant threat categories.
              </p>
            </div>

          </div>

        </div>

      </section>

      {/* REGIONAL REPORT */}
      
      <div className="regional-report-list">
  {regions.map((region) => {
    let riskClass = "medium";
    let riskLabel = "Medium";

    if (region.risk >= 80) {
      riskClass = "critical";
      riskLabel = "Critical";
    } else if (region.risk >= 60) {
      riskClass = "high";
      riskLabel = "High";
    }

    return (
      <div
        className="regional-report-row"
        key={region.name}
      >
        <div className="region-report-name">
          <div className="region-report-icon">
            <MapPin size={15} />
          </div>

          <strong>{region.name}</strong>
        </div>

        <div className="incident-count">
          <span>Incidents</span>
          <strong>{region.incidents}</strong>
        </div>

        <div className="region-risk">
          <div>
            <span>Risk Score</span>
            <strong>{region.risk}/100</strong>
          </div>

          <div className="region-risk-bar">
            <div
              style={{
                width: `${region.risk}%`,
              }}
            />
          </div>
        </div>

        <span className={`region-risk-badge ${riskClass}`}>
          {riskLabel}
        </span>
      </div>
    );
  })}
</div>

      {/* INCIDENT REPORT */}
      <section className="report-panel incident-report">

        <div className="report-panel-heading">

          <div>
            <h2>Recent Incident Summary</h2>
            <p>
              Latest incidents included in this report.
            </p>
          </div>

          <span className="report-count">
            {reportData.length} Records
          </span>

        </div>

        <div className="incident-table">

          <div className="incident-table-head">
            <span>Incident ID</span>
            <span>Threat Type</span>
            <span>Location</span>
            <span>Severity</span>
            <span>Status</span>
            <span>Date</span>
          </div>

          {reportData.map((report) => (

            <div
              className="incident-table-row"
              key={report.id}
            >

              <strong>{report.id}</strong>

              <span>{report.type}</span>

              <span className="table-location">
                <MapPin size={13} />
                {report.location}
              </span>

              <span
                className={`report-severity ${report.severity.toLowerCase()}`}
              >
                {report.severity}
              </span>

              <span
                className={`report-status ${
                  report.status
                    .toLowerCase()
                    .replaceAll(" ", "-")
                }`}
              >
                {report.status}
              </span>

              <span className="report-date">
                {report.date}
              </span>

            </div>

          ))}

        </div>

      </section>

      {/* REPORT FOOTER */}
      <section className="report-footer">

        <div>
          <CheckCircle2 size={17} />

          <span>
            Report data verified by CYBERTRACE intelligence engine
          </span>
        </div>

        <span>
          {reportType} • {period}
        </span>

      </section>

    </main>
  );
}
