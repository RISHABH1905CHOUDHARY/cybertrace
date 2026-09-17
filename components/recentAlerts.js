"use client";

import { useState } from "react";
import { initialAlerts } from "../app/data/Alert";
 
export default function RecentAlerts() {

  const [showAllAlerts, setShowAllAlerts] = useState(false);

  const visibleAlerts = showAllAlerts
    ? initialAlerts
    : initialAlerts.slice(0, 5);

  return (

    <section className="side-panel">

      <div className="side-header">

        <h2>
          ◈ Recent Alerts
        </h2>

       <button className="view_all"
  onClick={() => setShowAllAlerts(!showAllAlerts)}
>
  {showAllAlerts ? "Show Less" : "View All"}
</button>

      </div>


      <div className="alerts-list">
{visibleAlerts.map((alert) => (
  <div
    className="alert-item"
    key={alert.id}
  >
    <div
      className={`alert-dot ${alert.severity.toLowerCase()}`}
    />

    <div className="alert-content">

      <div>
        <span
          className={`severity ${alert.severity.toLowerCase()}`}
        >
          {alert.severity}
        </span>

        <strong>
          {alert.location}
        </strong>
      </div>

      <p>
        {alert.description}
      </p>

      <span className="alert-time">
        {alert.time}
      </span>

    </div>
  </div>
))}

      </div>

    </section>

  );
}