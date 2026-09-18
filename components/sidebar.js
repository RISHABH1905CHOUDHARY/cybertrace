"use client";

import { useRouter , usePathname  } from "next/navigation";

import Link from "next/link";

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
    href:"/",
  },
  {
    label: "Predictions",
    icon: Shield,
    href: "/predictions",
  },
  {
    label: "Alerts",
    icon: Bell,
    href: "/alerts",
  },
  {
    label: "Complaints",
    icon: FileText,
    href: "/complaints",
  },
  {
    label: "Analytics",
    icon: BarChart3,
    href: "/analytics",
  },
  {
    label: "Reports",
    icon: FileBarChart,
    href: "/reports",
  },
 
  
];

export default function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();
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
            <Link
  key={item.label}
  href={item.href}
  className={`sidebar-item ${
  pathname === item.href ? "active" : ""
}`}
>
  <Icon size={20} />
  <span>{item.label}</span>
</Link>
          );
        })}

        {/* Simulate Fraud */}
       <button
  type="button"
  className="sidebar-item "
 onClick={() => {
  router.push("/SimulateFraud");
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
  onClick={() => {
    router.push("/User");
  }}
>
  <Users size={20} />
  <span>Users</span>
</button>

       <button
  type="button"
  className="sidebar-item"
  onClick={() => {
    router.push("/AboutDigitalFuture");
  }}
>
  <Info size={20} />
  <span>About Digital Future</span>
</button>

      </div>

    </aside>
  );
}