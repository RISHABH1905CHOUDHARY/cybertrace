"use client";

import {
  LayoutDashboard,
  Shield,
  Bell,
  FileText,
  BarChart3,
  FileBarChart,
  Zap,
  Users,
  Info,
} from "lucide-react";

const menuItems = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "Predictions",
    icon: Shield,
  },
  {
    label: "Alerts",
    icon: Bell,
  },
  {
    label: "Complaints",
    icon: FileText,
  },
  {
    label: "Analytics",
    icon: BarChart3,
  },
  {
    label: "Reports",
    icon: FileBarChart,
  },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">

      {/* Logo */}
      <div className="logo-area">
        <h2>CYBERTRACE</h2>
        
      </div>

      {/* Main Navigation */}
      <nav className="sidebar-nav">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              type="button"
              className="sidebar-item"
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </button>
          );
        })}

        {/* Simulate Fraud */}
        <button
          type="button"
          className="sidebar-item active"
          onClick={() => {
            window.dispatchEvent(
              new CustomEvent("simulate-fraud")
            );
          }}
        >
          <Zap size={20} />
          <span>Simulate Fraud</span>
        </button>

      </nav>

      {/* Bottom Section */}
      <div className="sidebar-bottom">

        <button
          type="button"
          className="sidebar-item"
        >
          <Users size={20} />
          <span>Users</span>
        </button>

        <button
          type="button"
          className="sidebar-item"
        >
          <Info size={20} />
          <span>About Digital Future</span>
        </button>

      </div>

    </aside>
  );
}