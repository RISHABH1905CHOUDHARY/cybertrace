"use client";

import { useState } from "react";
import {
  User,
  Shield,
  Bell,
  Palette,
  Database,
  Lock,
  Brain,
  Save,
} from "lucide-react";

export default function SettingsPage() {
  const [notifications, setNotifications] = useState(true);
  const [securityAlerts, setSecurityAlerts] = useState(true);
  const [darkMode, setDarkMode] = useState(true);
  const [autoPrediction, setAutoPrediction] = useState(true);

  return (
    <main className="settings-page">

      {/* Header */}
      <div className="settings-header">
        <div>
          <h1>Settings</h1>
          <p>
            Manage your CYBERTRACE account, security and system preferences.
          </p>
        </div>

        <button className="save-btn">
          <Save size={18} />
          Save Changes
        </button>
      </div>

      {/* Profile */}
      <section className="settings-card">
        <div className="settings-title">
          <User size={22} />
          <div>
            <h2>Profile</h2>
            <p>Manage your investigator profile.</p>
          </div>
        </div>
<div className="settings-grid">

  <div className="input-group">
    <label htmlFor="full-name">Full Name</label>
    <input
      id="full-name"
      type="text"
      defaultValue="Rishabh Choudhary"
    />
  </div>

  <div className="input-group">
    <label htmlFor="role">Role</label>
    <input
      id="role"
      type="text"
      defaultValue="Investigator"
      disabled
    />
  </div>

  <div className="input-group">
    <label htmlFor="email">Email</label>
    <input
      id="email"
      type="email"
      defaultValue="rishabh@gmail.com"
    />
  </div>

  <div className="input-group">
    <label htmlFor="department">Department</label>
    <input
      id="department"
      type="text"
      placeholder="Enter department"
    />
  </div>

</div>
        
      </section>

      {/* Security */}
      <section className="settings-card">

        <div className="settings-title">
          <Shield size={22} />
          <div>
            <h2>Security</h2>
            <p>Control your account security settings.</p>
          </div>
        </div>

        <SettingRow
          icon={<Lock size={20} />}
          title="Two-Factor Authentication"
          description="Add an extra layer of protection to your account."
          action={
            <button className="outline-btn">
              Configure
            </button>
          }
        />

        <SettingRow
          icon={<Shield size={20} />}
          title="Login Activity"
          description="Review recent login and account activity."
          action={
            <button className="outline-btn">
              View Activity
            </button>
          }
        />

      </section>

      {/* Notifications */}
      <section className="settings-card">

        <div className="settings-title">
          <Bell size={22} />
          <div>
            <h2>Notifications</h2>
            <p>Choose which alerts you want to receive.</p>
          </div>
        </div>

        <ToggleRow
          title="System Notifications"
          description="Receive important system updates."
          enabled={notifications}
          setEnabled={setNotifications}
        />

        <ToggleRow
          title="Security Alerts"
          description="Receive high-risk fraud and security alerts."
          enabled={securityAlerts}
          setEnabled={setSecurityAlerts}
        />

      </section>

      {/* Fraud Detection */}
      <section className="settings-card">

        <div className="settings-title">
          <Brain size={22} />
          <div>
            <h2>Fraud Detection</h2>
            <p>Configure AI prediction preferences.</p>
          </div>
        </div>

        <ToggleRow
          title="Automatic Risk Prediction"
          description="Automatically analyze submitted transactions."
          enabled={autoPrediction}
          setEnabled={setAutoPrediction}
        />

        <div className="input-group">
  <label htmlFor="risk-threshold">Risk Threshold</label>

  <select id="risk-threshold" defaultValue="medium">
    <option value="low">Low</option>
    <option value="medium">Medium</option>
    <option value="high">High</option>
  </select>
</div>
      </section>

      {/* Appearance */}
      <section className="settings-card">

        <div className="settings-title">
          <Palette size={22} />
          <div>
            <h2>Appearance</h2>
            <p>Customize the CYBERTRACE interface.</p>
          </div>
        </div>

        <ToggleRow
          title="Dark Mode"
          description="Use the dark interface for CYBERTRACE."
          enabled={darkMode}
          setEnabled={setDarkMode}
        />

      </section>

      {/* Privacy */}
      <section className="settings-card">

        <div className="settings-title">
          <Database size={22} />
          <div>
            <h2>Privacy & Data</h2>
            <p>Manage your application data.</p>
          </div>
        </div>

        <SettingRow
          icon={<Database size={20} />}
          title="Export Investigation Data"
          description="Download investigation and report data."
          action={
            <button className="outline-btn">
              Export
            </button>
          }
        />

        <SettingRow
          icon={<Database size={20} />}
          title="Clear Local Data"
          description="Remove locally stored application data."
          action={
            <button className="danger-btn">
              Clear Data
            </button>
          }
        />

      </section>

    </main>
  );
}


/* Toggle Component */

function ToggleRow({
  title,
  description,
  enabled,
  setEnabled,
}) {
  return (
    <div className="setting-row">

      <div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>

      <button
        type="button"
        className={`toggle ${enabled ? "toggle-on" : ""}`}
        onClick={() => setEnabled(!enabled)}
      >
        <span />
      </button>

    </div>
  );
}


/* Normal Setting Row */

function SettingRow({
  icon,
  title,
  description,
  action,
}) {
  return (
    <div className="setting-row">

      <div className="setting-left">
        <div className="setting-icon">
          {icon}
        </div>

        <div>
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
      </div>

      {action}

    </div>
  );
}