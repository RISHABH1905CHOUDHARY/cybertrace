"use client";

import { useState } from "react";

export default function SimulateFraud() {
  const [form, setForm] = useState({
    amount: "",
    location: "",
    transactionType: "ATM Withdrawal",
    accountAge: "",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  // ✅ PUT THE FUNCTION HERE
  const simulateFraud = (e) => {
    e.preventDefault();

    const amount = Number(form.amount);

    let risk = "Low";
    let score = 25;
    let message = "Transaction appears relatively safe.";

    if (amount > 50000) {
      risk = "High";
      score = 88;
      message = "Suspicious transaction detected.";
    } else if (amount > 20000) {
      risk = "Medium";
      score = 65;
      message = "Transaction requires additional verification.";
    }

    setResult({
      risk,
      score,
      message,
    });
  };

  return (
    <div className="fraud-page">

      <div className="page-header">
        <div>
          <h1>Simulate Fraud</h1>
          <p>
            Test a transaction and analyze its potential fraud risk.
          </p>
        </div>
      </div>
      <div className="fraud-grid">

        {/* FORM */}
        <div className="fraud-card">

          <h2>Transaction Details</h2>

          <form onSubmit={simulateFraud}>

          <label htmlFor="amount">Transaction Amount</label>

<input
  id="amount"
  type="number"
  name="amount"
  placeholder="Enter amount"
  value={form.amount}
  onChange={handleChange}
  required
/>

            <label htmlFor="location">Location</label>

<input
  id="location"
  type="text"
  name="location"
  placeholder="Enter location"
  value={form.location}
  onChange={handleChange}
  required
/>

            <label htmlFor="transactionType">Transaction Type</label>

            <select
              name="transactionType"
              value={form.transactionType}
              onChange={handleChange}
            >
              <option>ATM Withdrawal</option>
              <option>Online Payment</option>
              <option>UPI Transaction</option>
              <option>Card Transaction</option>
              <option>Bank Transfer</option>
            </select>

            <label htmlFor="accountAge">Account Age</label>

<input
  id="accountAge"
  type="number"
  name="accountAge"
  placeholder="Age of account in months"
  value={form.accountAge}
  onChange={handleChange}
  required
/>

            <button type="submit">
              ⚡ Simulate Fraud
            </button>

          </form>
        </div>

        {/* RESULT */}
        <div className="fraud-card result-card">

          <h2>Prediction Result</h2>

          {!result ? (
            <div className="empty-result">
              <div className="result-icon">🛡️</div>

              <h3>No Simulation Yet</h3>

              <p>
  Enter transaction details and click{" "}
  <strong>Simulate Fraud</strong>{" "}
  to generate a risk prediction.
</p>
            </div>
          ) : (
            <div>

              <div className={`risk-result ${result.risk.toLowerCase()}`}>
                <span>Risk Level</span>
                <strong>{result.risk} Risk</strong>
              </div>

              <div className="score">
                <span>Fraud Risk Score</span>

                <strong>{result.score}%</strong>

                <div className="score-bar">
                  <div
                    style={{
                      width: `${result.score}%`,
                    }}
                  ></div>
                </div>
              </div>

              <div className="prediction-message">
                {result.message}
              </div>

              <div className="transaction-summary">

                <p>
                  <b>Amount:</b> ₹{form.amount}
                </p>

                <p>
                  <b>Location:</b> {form.location}
                </p>

                <p>
                  <b>Type:</b> {form.transactionType}
                </p>

              </div>

            </div>
          )}

        </div>

      </div>
    </div>
  );
}