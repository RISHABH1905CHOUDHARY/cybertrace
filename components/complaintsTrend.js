"use client";

import { useState } from "react";


const values = [
  42,
  68,
  96,
  80,
  78,
  100,
  128,
  112,
  120,
  172
];


export default function ComplaintsTrend() {

  const [period, setPeriod] =
    useState("Last 7 Days");

    const handleStatusCardClick = (status) => {
  setStatusFilter(status);
};

  const points = values
    .map((value, index) => {

      const x = 10 + index * 30;

      const y =
        150 - (value / 200) * 120;

      return `${x},${y}`;

    })
    .join(" ");


  return (

    <section className="chart-panel">

      <div className="chart-header">

        <h2>
          ⌁ Complaints Trend
        </h2>

        <select
          value={period}
          onChange={(e) =>
            setPeriod(e.target.value)
          }
        >

          <option>
            Last 7 Days
          </option>

          <option>
            Last 30 Days
          </option>

        </select>

      </div>


      <div className="line-chart">

        <div className="y-axis">

          <span>200</span>
          <span>150</span>
          <span>100</span>
          <span>50</span>
          <span>0</span>

        </div>


        <svg
          viewBox="0 0 300 160"
          preserveAspectRatio="none"
        >

          {[20, 50, 80, 110, 140].map(
            (y) => (

              <line
                key={y}
                x1="10"
                x2="295"
                y1={y}
                y2={y}
              />

            )
          )}


          <polyline
            points={points}
            fill="none"
            className="trend-line"
          />


          {values.map((value, index) => {

            const x = 10 + index * 30;

            const y =
              150 - (value / 200) * 120;

            return (

              <circle
                key={index}
                cx={x}
                cy={y}
                r="3"
              />

            );

          })}

        </svg>


        <div className="x-axis">

          <span>30 Aug</span>
          <span>31 Aug</span>
          <span>1 Sep</span>
          <span>2 Sep</span>
          <span>3 Sep</span>
          <span>4 Sep</span>
          <span>5 Sep</span>

        </div>

      </div>

    </section>

  );
}