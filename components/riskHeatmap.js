"use client";

import { useState } from "react";

import {
  Map,
  ZoomIn,
  ZoomOut,
  ChevronDown,
} from "lucide-react";

const locations = [
  {
    name: "Vijay Nagar, Indore",
    risk: 88,
    type: "critical",
  },

  {
    name: "Palasia, Indore",
    risk: 79,
    type: "high",
  },

  {
    name: "MG Road, Indore",
    risk: 68,
    type: "medium",
  },

  {
    name: "Civil Lines, Bhopal",
    risk: 62,
    type: "medium",
  },

  {
    name: "Hazratganj, Lucknow",
    risk: 58,
    type: "low",
  },
];

export default function RiskHeatmap() {
  const [selected, setSelected] = useState(locations[0]);

  const [timeFilter, setTimeFilter] =
    useState("Next 24 Hours");

  const [stateFilter, setStateFilter] =
    useState("All States");

  const [openDropdown, setOpenDropdown] =
    useState(null);

  const [showDetails, setShowDetails] = 
    useState(false);

  return (
    <section className="heatmap-panel">

      {/* Header */}
      <div className="panel-header">

        <div className="panel-title">
          <Map size={23} />

          <div>
            <h2>Risk Heatmap</h2>

            <p>
              Predicted cash-withdrawal risk across regions
            </p>
          </div>
        </div>


        {/* FILTERS */}
        <div className="map-filters">

          {/* TIME DROPDOWN */}
          <div className="dropdown">

            <button
              type="button"
              className="dropdown-btn"
              onClick={() =>
                setOpenDropdown(
                  openDropdown === "time"
                    ? null
                    : "time"
                )
              }
            >
              {timeFilter}

              <ChevronDown size={15} />
            </button>


            {openDropdown === "time" && (
              <div className="dropdown-menu">

                {[
                  "Next 24 Hours",
                  "Next 48 Hours",
                  "Next 7 Days",
                ].map((option) => (
                  <button
                    type="button"
                    key={option}
                    className="dropdown-option"
                    onClick={() => {
                      setTimeFilter(option);
                      setOpenDropdown(null);
                    }}
                  >
                    {option}
                  </button>
                ))}

              </div>
            )}

          </div>


          {/* STATE DROPDOWN */}
          <div className="dropdown">

            <button
              type="button"
              className="dropdown-btn"
              onClick={() =>
                setOpenDropdown(
                  openDropdown === "state"
                    ? null
                    : "state"
                )
              }
            >
              {stateFilter}

              <ChevronDown size={15} />
            </button>


            {openDropdown === "state" && (
              <div className="dropdown-menu">

                {[
                  "All States",
                  "Madhya Pradesh",
                  "Uttar Pradesh",
                  "Maharashtra",
                  "Karnataka",
                  "Delhi",
                ].map((state) => (
                  <button
                    type="button"
                    key={state}
                    className="dropdown-option"
                    onClick={() => {
                      setStateFilter(state);
                      setOpenDropdown(null);
                    }}
                  >
                    {state}
                  </button>
                ))}

              </div>
            )}

          </div>

        </div>
        {/* END OF map-filters */}

      </div>
      {/* END OF panel-header */}


      {/* HEATMAP CONTENT */}
      <div className="heatmap-content">

        {/* MAP */}
        <div className="map-container">

          {/* Map Image */}
          {/*
          <img
            src="/risk-map.jpg"
            alt="India risk heatmap"
            className="map-image"
          />
          */}


          {/* Zoom Buttons */}
          <div className="zoom-buttons">

            <button type="button">
              <ZoomIn size={17} />
            </button>

            <button type="button">
              <ZoomOut size={17} />
            </button>

          </div>


          {/* HOTSPOTS */}

          {/* Vijay Nagar */}
          <button
            type="button"
            className="hotspot critical"
            style={{
              left: "47%",
              top: "29%",
            }}
            onClick={() =>
              setSelected(locations[0])
            }
          />


          {/* Palasia */}
          <button
            type="button"
            className="hotspot high"
            style={{
              left: "51%",
              top: "43%",
            }}
            onClick={() =>
              setSelected(locations[1])
            }
          />


          {/* MG Road */}
          <button
            type="button"
            className="hotspot medium"
            style={{
              left: "44%",
              top: "54%",
            }}
            onClick={() =>
              setSelected(locations[2])
            }
          />


          {/* Civil Lines */}
          <button
            type="button"
            className="hotspot medium"
            style={{
              left: "34%",
              top: "71%",
            }}
            onClick={() =>
              setSelected(locations[3])
            }
          />


       {/* MAP POPUP */}
<div className="map-popup">

  <h3>
    {selected.name}
  </h3>

  <p>
    <strong>Risk:</strong>{" "}
    {selected.risk}%
  </p>

  <p>
    <strong>Confidence:</strong>{" "}
    82%
  </p>

  <p>
    <strong>Predicted Window:</strong>{" "}
    6 PM – 10 PM
  </p>

  <button
    type="button"
    onClick={() => setShowDetails(true)}
  >
    View Details →
  </button>

</div>

{showDetails && (
  <div
    className="details-overlay"
    onClick={() => setShowDetails(false)}
  >
    <div
      className="details-modal"
      onClick={(e) => e.stopPropagation()}
    >
      <button
        type="button"
        className="details-close"
        onClick={() => setShowDetails(false)}
      >
        ×
      </button>

      <span className={`details-badge ${selected.type}`}>
        {selected.type.toUpperCase()}
      </span>

      <h2>{selected.name}</h2>

      <div className="details-grid">

        <div className="detail-card">
          <span>Risk Score</span>
          <strong>{selected.risk}%</strong>
        </div>

        <div className="detail-card">
          <span>Confidence</span>
          <strong>82%</strong>
        </div>

        <div className="detail-card">
          <span>Predicted Window</span>
          <strong>6 PM – 10 PM</strong>
        </div>

        <div className="detail-card">
          <span>Status</span>
          <strong>Monitoring</strong>
        </div>

      </div>

      <div className="details-description">
        <h3>Risk Analysis</h3>

        <p>
          Elevated cash-withdrawal activity has been
          predicted in this region. The system has
          identified this location as a potential
          risk area based on recent activity and
          historical patterns.
        </p>
      </div>

      <button
        type="button"
        onClick={() => setShowDetails(false)}
      >
        Close
      </button>

    </div>
  </div>
)}


          {/* LEGEND */}
          <div className="map-legend">

            <div className="legend-item">
              <span className="legend-dot critical"></span>
              <span>Critical Risk</span>
            </div>

            <div className="legend-item">
              <span className="legend-dot high"></span>
              <span>High Risk</span>
            </div>

            <div className="legend-item">
              <span className="legend-dot medium"></span>
              <span>Medium Risk</span>
            </div>

            <div className="legend-item">
              <span className="legend-dot low"></span>
              <span>Low Risk</span>
            </div>

          </div>

        </div>
        {/* END OF map-container */}


        {/* PREDICTED LOCATIONS */}
        <div className="predicted-list">

          <div className="list-header">

            <h3>
              Top Predicted Locations
            </h3>

            <button
              type="button"
              className="view_all"
            >
              View All
            </button>

          </div>


          {/* LOCATION LIST */}
          {locations.map((location, index) => (

            <div
              className="location"
              key={location.name}
            >

              <div
                className={`rank ${location.type}`}
              >
                {index + 1}
              </div>


              <div className="location-data">

                <div className="location-name">

                  <span>
                    {location.name}
                  </span>

                  <strong>
                    {location.risk}%
                  </strong>

                </div>


                <div className="risk-bar">

                  <div
                    className={location.type}
                    style={{
                      width: `${location.risk}%`,
                    }}
                  />

                </div>

              </div>

            </div>

          ))}

        </div>
        {/* END OF predicted-list */}

      </div>
      {/* END OF heatmap-content */}

    </section>
  );
}