const alerts = [
  {
    level: "CRITICAL",
    place: "Vijay Nagar, Indore",
    message: "High withdrawal risk detected",
    time: "2 min ago",
    type: "critical",
  },
  {
    level: "HIGH",
    place: "Palasia, Indore",
    message: "Unusual transaction pattern",
    time: "18 min ago",
    type: "high",
  },
  {
    level: "HIGH",
    place: "MG Road, Indore",
    message: "Multiple linked accounts",
    time: "42 min ago",
    type: "high",
  },
  {
    level: "MEDIUM",
    place: "Civil Lines, Bhopal",
    message: "Potential cash-out activity",
    time: "1 hr ago",
    type: "medium",
  },
  {
    level: "MEDIUM",
    place: "Hazratganj, Lucknow",
    message: "Suspicious ATM activity",
    time: "2 hr ago",
    type: "medium",
  },
];

export default function RecentAlerts() {
  return (
    <section className="side-panel">

      {/* Header */}
      <div className="side-header">

        <h2>◈ Recent Alerts</h2>

        <button>
          View All
        </button>

      </div>


      {/* Alerts */}
      <div className="alerts-list">

        {alerts.map((alert) => (
          <div
            className="alert-item"
            key={`${alert.place}-${alert.message}`}
          >

            {/* Alert dot */}
            <div
              className={`alert-dot ${alert.type}`}
            ></div>


            {/* Alert information */}
            <div className="alert-content">

              <div className="alert-title">

                <span
                  className={`severity ${alert.type}`}
                >
                  {alert.level}
                </span>

                <strong>
                  {alert.place}
                </strong>

              </div>


              <p>
                {alert.message}
              </p>

            </div>


            {/* Time */}
            <small>
              {alert.time}
            </small>

          </div>
        ))}

      </div>

    </section>
  );
}