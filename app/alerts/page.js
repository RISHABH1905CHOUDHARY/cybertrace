"use client";

import { useState } from "react";
import {
  AlertTriangle,
  ShieldAlert,
  ShieldCheck,
  Clock3,
  Search,
  Filter,
  CheckCircle2,
  MapPin,
  Activity,
  X,
} from "lucide-react";

const initialAlerts = [
  {
    id: "ALT-1001",
    title: "Suspicious Transaction Detected",
    description: "Unusual cash withdrawal pattern detected.",
    severity: "Critical",
    location: "New Delhi",
    time: "2 min ago",
    status: "Open",
  },
  {
    id: "ALT-1002",
    title: "Multiple Failed Login Attempts",
    description: "Repeated authentication failures detected.",
    severity: "High",
    location: "Mumbai",
    time: "12 min ago",
    status: "Open",
  },
  {
    id: "ALT-1003",
    title: "Unusual Network Activity",
    description: "Unexpected traffic pattern identified.",
    severity: "High",
    location: "Bengaluru",
    time: "28 min ago",
    status: "Investigating",
  },
  {
    id: "ALT-1004",
    title: "Suspicious Account Activity",
    description: "Account activity differs from normal behavior.",
    severity: "Medium",
    location: "Bhopal",
    time: "41 min ago",
    status: "Open",
  },
  {
    id: "ALT-1005",
    title: "Potential Phishing Attempt",
    description: "Suspicious email activity detected.",
    severity: "Medium",
    location: "Hyderabad",
    time: "1 hour ago",
    status: "Resolved",
  },
  {
    id: "ALT-1006",
    title: "Unknown Device Connected",
    description: "New device detected on protected network.",
    severity: "Low",
    location: "Pune",
    time: "2 hours ago",
    status: "Resolved",
  },
];

export default function AlertsPage() {
  const [alerts, setAlerts] = useState(initialAlerts);
  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("All");
  const [status, setStatus] = useState("All");
  const [selectedAlert, setSelectedAlert] = useState(null);

  const acknowledgeAlert = (id) => {
    setAlerts((currentAlerts) =>
      currentAlerts.map((alert) =>
        alert.id === id
          ? { ...alert, status: "Resolved" }
          : alert
      )
    );
  };

  const filteredAlerts = alerts.filter((alert) => {
    const matchesSearch =
      alert.title.toLowerCase().includes(search.toLowerCase()) ||
      alert.location.toLowerCase().includes(search.toLowerCase()) ||
      alert.id.toLowerCase().includes(search.toLowerCase());

    const matchesSeverity =
      severity === "All" || alert.severity === severity;

    const matchesStatus =
      status === "All" || alert.status === status;

    return matchesSearch && matchesSeverity && matchesStatus;
  });

  const criticalCount = alerts.filter(
    (alert) => alert.severity === "Critical"
  ).length;

  const highCount = alerts.filter(
    (alert) => alert.severity === "High"
  ).length;

  const openCount = alerts.filter(
    (alert) => alert.status === "Open"
  ).length;

  const resolvedCount = alerts.filter(
    (alert) => alert.status === "Resolved"
  ).length;

  return (
    <main className="alerts-page">

      {/* Header */}
      <section className="alerts-header">
        <div>
          <div className="alerts-title-row">
            <div className="alerts-title-icon">
              <ShieldAlert size={26} />
            </div>

            <div>
              <h1>Security Alerts</h1>
              <p>
                Monitor, investigate and manage detected cyber threats.
              </p>
            </div>
          </div>
        </div>

        <div className="system-live">
          <span className="live-dot"> Live Monitoring</span>
         
        </div>
      </section>

      {/* Statistics */}
      <section className="alert-stats">

        <div className="alert-stat-card critical-card">
          <div className="stat-icon critical-icon">
            <AlertTriangle size={22} />
          </div>

          <div>
            <span>Critical Alerts</span>
            <strong>{criticalCount}</strong>
          </div>
        </div>

        <div className="alert-stat-card high-card">
          <div className="stat-icon high-icon">
            <ShieldAlert size={22} />
          </div>

          <div>
            <span>High Risk</span>
            <strong>{highCount}</strong>
          </div>
        </div>

        <div className="alert-stat-card open-card">
          <div className="stat-icon open-icon">
            <Activity size={22} />
          </div>

          <div>
            <span>Open Alerts</span>
            <strong>{openCount}</strong>
          </div>
        </div>

        <div className="alert-stat-card resolved-card">
          <div className="stat-icon resolved-icon">
            <ShieldCheck size={22} />
          </div>

          <div>
            <span>Resolved</span>
            <strong>{resolvedCount}</strong>
          </div>
        </div>

      </section>

      {/* Filters */}
      <section className="alerts-panel">

        <div className="alerts-toolbar">

          <div className="alert-search">
            <Search size={18} />

            <input
              type="text"
              placeholder="Search alerts, location or ID..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

          <div className="filter-control">
            <Filter size={17} />

            <select
              value={severity}
              onChange={(event) => setSeverity(event.target.value)}
            >
              <option value="All">All Severity</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>
          </div>

          <div className="filter-control">
            <select
              value={status}
              onChange={(event) => setStatus(event.target.value)}
            >
              <option value="All">All Status</option>
              <option value="Open">Open</option>
              <option value="Investigating">Investigating</option>
              <option value="Resolved">Resolved</option>
            </select>
          </div>

        </div>

        {/* Alert List */}
        <div className="alerts-list">

          <div className="alerts-list-header">
            <div>
              <h2>Recent Alerts</h2>
              <span>
                {filteredAlerts.length} alerts found
              </span>
            </div>

            <div className="security-status">
              <span> Security engine active </span>
            </div>
          </div>

          {filteredAlerts.length === 0 ? (
            <div className="no-alerts">
              <ShieldCheck size={42} />
              <h3>No alerts found</h3>
              <p>
                Try changing your search or filter options.
              </p>
            </div>
          ) : (
            filteredAlerts.map((alert) => (
              <article className="alert-row" key={alert.id}>

                <div className={`severity-indicator ${alert.severity.toLowerCase()}`}></div>

                <div className="alert-main-icon">
                  <AlertTriangle size={21} />
                </div>

                <div className="alert-content">

                  <div className="alert-name-row">
                    <h3>{alert.title}</h3>

                    <span
                      className={`severity-badge ${alert.severity.toLowerCase()}`}
                    >
                      {alert.severity}
                    </span>
                  </div>

                  <p>{alert.description}</p>

                  <div className="alert-meta">

                    <span>
                      <Activity size={14} />
                      {alert.id}
                    </span>

                    <span>
                      <MapPin size={14} />
                      {alert.location}
                    </span>

                    <span>
                      <Clock3 size={14} />
                      {alert.time}
                    </span>

                  </div>

                </div>

                <div className="alert-actions">

                  <span
                    className={`status-badge ${alert.status
                      .toLowerCase()
                      .replace(" ", "-")}`}
                  >
                    {alert.status}
                  </span>

                  <button
                    type="button"
                    className="view-alert-btn"
                    onClick={() => setSelectedAlert(alert)}
                  >
                    View Details
                  </button>

                  {alert.status !== "Resolved" && (
                    <button
                      type="button"
                      className="acknowledge-btn"
                      onClick={() => acknowledgeAlert(alert.id)}
                    >
                      <CheckCircle2 size={15} />
                      Acknowledge
                    </button>
                  )}

                </div>

              </article>
            ))
          )}

        </div>

      </section>

      {/* Details Modal */}
      {selectedAlert && (
  <div className="alert-modal-overlay">
    <div className="alert-modal">

      <div className="modal-header">
        <div>
          <span className="modal-label">
            ALERT DETAILS
          </span>

          <h2>{selectedAlert.title}</h2>
        </div>

        <button
          type="button"
          className="modal-close"
          onClick={() => setSelectedAlert(null)}
          aria-label="Close alert details"
        >
          <X size={20} />
        </button>
      </div>

      <div className="modal-severity">
        <span
          className={`severity-badge ${selectedAlert.severity.toLowerCase()}`}
        >
          {selectedAlert.severity} Risk
        </span>

        <span>{selectedAlert.id}</span>
      </div>

      <div className="modal-details">

        <div>
          <span>Description</span>
          <strong>{selectedAlert.description}</strong>
        </div>

        <div>
          <span>Location</span>
          <strong>{selectedAlert.location}</strong>
        </div>

        <div>
          <span>Detected</span>
          <strong>{selectedAlert.time}</strong>
        </div>

        <div>
          <span>Status</span>
          <strong>{selectedAlert.status}</strong>
        </div>

      </div>

      {selectedAlert.status !== "Resolved" && (
        <button
          type="button"
          className="modal-acknowledge"
          onClick={() => {
            acknowledgeAlert(selectedAlert.id);
            setSelectedAlert({
              ...selectedAlert,
              status: "Resolved",
            });
          }}
        >
          <CheckCircle2 size={18} />
          Mark as Resolved
        </button>
      )}

    </div>
  </div>
)}

    </main>
  );
}