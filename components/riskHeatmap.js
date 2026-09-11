"use client";
import { useState } from "react";


import {
  Map,
  ZoomIn,
  ZoomOut,
  ChevronDown
} from "lucide-react";


const locations = [

  {
    name: "Vijay Nagar, Indore",
    risk: 88,
    type: "critical"
  },

  {
    name: "Palasia, Indore",
    risk: 79,
    type: "high"
  },

  {
    name: "MG Road, Indore",
    risk: 68,
    type: "medium"
  },

  {
    name: "Civil Lines, Bhopal",
    risk: 62,
    type: "medium"
  },

  {
    name: "Hazratganj, Lucknow",
    risk: 58,
    type: "low"
  }

];


export default function RiskHeatmap() {

  const [selected, setSelected] = useState(
    locations[0]
  );

  return (

    <section className="heatmap-panel">

      {/* Header */}

      <div className="panel-header">

        <div className="panel-title">

          <Map size={23} />

          <div>

            <h2>
              Risk Heatmap
            </h2>

            <p>
              Predicted cash-withdrawal risk across regions
            </p>

          </div>

        </div>


        <div className="map-filters">

          <button>
            Next 24 Hours
            <ChevronDown size={15} />
          </button>

          <button>
            All States
            <ChevronDown size={15} />
          </button>

        </div>

      </div>


      {/* Map */}

      <div className="heatmap-content">

        <div className="map-container">

         {/*<img
            src="/risk-map.jpg"
            alt="India risk heatmap"
            className="map-image"
          />*/}


          {/* Zoom */}

          <div className="zoom-buttons">

            <button>
              <ZoomIn size={17} />
            </button>

            <button>
              <ZoomOut size={17} />
            </button>

          </div>


          {/* Hotspots */}

          <button
            className="hotspot critical"
            style={{
              left: "47%",
              top: "29%"
            }}
            onClick={() =>
              setSelected(locations[0])
            }
          />

          <button
            className="hotspot high"
            style={{
              left: "51%",
              top: "43%"
            }}
            onClick={() =>
              setSelected(locations[1])
            }
          />

          <button
            className="hotspot medium"
            style={{
              left: "44%",
              top: "54%"
            }}
            onClick={() =>
              setSelected(locations[2])
            }
          />

          <button
            className="hotspot medium"
            style={{
              left: "34%",
              top: "71%"
            }}
            onClick={() =>
              setSelected(locations[3])
            }
          />


          {/* Popup */}

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

            <button>
              View Details →
            </button>

          </div>


          {/* Legend */}

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


        {/* Predicted locations */}

        <div className="predicted-list">

          <div className="list-header">

            <h3>
              Top Predicted Locations
            </h3>

            <button>
              View All
            </button>

          </div>


          {locations.map((location, index) => (

            <div
              className="location"
              key={location.name}
            >

              <div className={`rank ${location.type}`}>
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
                      width: `${location.risk}%`
                    }}
                  />

                </div>

              </div>

            </div>

          ))}

        </div>

      </div>

    </section>

  );
}