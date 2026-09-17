"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import {
  Search,
  Bell,
  ChevronDown,
  Shield,
  X,
  User,
  FileText,
  Settings,
  LogOut,
} from "lucide-react";

export default function Header() {
  const router = useRouter();

  // ==========================================
  // USER
  // ==========================================

 
  // ==========================================
  // SEARCH
  // ==========================================

  const [search, setSearch] = useState("");
  const [showSearchResults, setShowSearchResults] = useState(false);
  const [userName, setUserName] = useState("");
  useEffect(() => {
  const savedUser = localStorage.getItem("user");

  if (savedUser) {
    const user = JSON.parse(savedUser);

    // eslint-disable-next-line react-hooks/set-state-in-effect
    setUserName(user.name);
  }
}, []);
  // ==========================================
  // NOTIFICATION
  // ==========================================

  const [showNotifications, setShowNotifications] = useState(false);

  // ==========================================
  // PROFILE
  // ==========================================

  const [showProfile, setShowProfile] = useState(false);

  // ==========================================
  // LOAD USER
  // ==========================================

  
  // ==========================================
  // SEARCH ITEMS
  // ==========================================

  const searchItems = [
    {
      name: "Dashboard",
      path: "/",
      keywords: "dashboard home overview",
    },

    {
      name: "Predictions",
      path: "/predictions",
      keywords: "predictions prediction risk forecast",
    },

    {
      name: "Alerts",
      path: "/alerts",
      keywords: "alerts alert security threats warning",
    },

    {
      name: "Complaints",
      path: "/complaints",
      keywords: "complaints complaint cases",
    },

    {
      name: "Analytics",
      path: "/analytics",
      keywords: "analytics statistics data",
    },

    {
      name: "Reports",
      path: "/reports",
      keywords: "reports report documents",
    },
  ];

  // ==========================================
  // FILTER SEARCH
  // ==========================================

  const filteredItems = searchItems.filter((item) => {
    const query = search.toLowerCase().trim();

    return (
      item.name.toLowerCase().includes(query) ||
      item.keywords.toLowerCase().includes(query)
    );
  });

  // ==========================================
  // OPEN SEARCH RESULT
  // ==========================================

  const openSearchResult = (path) => {
    router.push(path);

    setSearch("");
    setShowSearchResults(false);
  };

  // ==========================================
  // SEARCH
  // ==========================================

  const handleSearch = (event) => {
    event.preventDefault();

    if (filteredItems.length > 0) {
      openSearchResult(filteredItems[0].path);
    }
  };

  // ==========================================
  // LOGOUT
  // ==========================================

  const handleLogout = () => {
    localStorage.removeItem("loggedIn");
    localStorage.removeItem("user");

    // Remove cookie
    document.cookie =
      "loggedIn=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";

    router.push("/login");
  };

  // ==========================================
  // RETURN
  // ==========================================

  return (
    <header className="header">

      {/* ======================================
          LOGO
      ====================================== */}

      <Link
        href="/"
        className="logo-area"
        aria-label="Go to Dashboard"
      >

        <div className="logo-icon">
          <Shield
            size={38}
            strokeWidth={2}
          />
        </div>

        <div className="logo-text">

          <h2>
            CYBER<span>TRACE</span>
          </h2>

          <p>
            Predict • Prevent • Protect
          </p>

        </div>

      </Link>

      {/* ======================================
          SEARCH
      ====================================== */}

      <div className="header-search-wrapper">

        <form
          className="search-container"
          onSubmit={handleSearch}
        >

          <Search size={19} />

          <input
            type="search"
            value={search}
            onChange={(event) => {
              setSearch(event.target.value);
              setShowSearchResults(true);
            }}
            onFocus={() => {
              if (search) {
                setShowSearchResults(true);
              }
            }}
            placeholder="Search complaints, locations, cases..."
            aria-label="Search"
          />

          <kbd>⌘ K</kbd>

        </form>

        {/* SEARCH RESULTS */}

        {showSearchResults && search && (

          <div className="header-search-results">

            {filteredItems.length > 0 ? (

              filteredItems.map((item) => (

                <button
                  type="button"
                  className="search-result"
                  key={item.path}
                  onClick={() =>
                    openSearchResult(item.path)
                  }
                >

                  <Search size={17} />

                  <div>

                    <strong>
                      {item.name}
                    </strong>

                    <small>
                      {item.keywords}
                    </small>

                  </div>

                </button>

              ))

            ) : (

              <div className="no-search-result">

                <Search size={18} />

                <span>
                  No matching page found
                </span>

              </div>

            )}

          </div>

        )}

      </div>

      {/* ======================================
          RIGHT SIDE
      ====================================== */}

      <div className="header-right">

        {/* ====================================
            NOTIFICATIONS
        ==================================== */}

        <div className="notification">

          <button
            type="button"
            className="notification-button"
            onClick={() =>
              setShowNotifications(
                !showNotifications
              )
            }
            aria-label="Open notifications"
          >

            <Bell size={22} />

            <span>
              1
            </span>

          </button>

          {/* NOTIFICATION DROPDOWN */}

          {showNotifications && (

            <div className="notification-dropdown">

              <div className="dropdown-title">

                <strong>
                  Notifications
                </strong>

                <button
                  type="button"
                  onClick={() =>
                    setShowNotifications(false)
                  }
                  aria-label="Close notifications"
                >

                  <X size={17} />

                </button>

              </div>

              {/* ALERT 1 */}

              <div className="notification-item">

                <div className="notification-dot critical"></div>

                <div>

                  <strong>
                    High Risk Alert
                  </strong>

                  <p>
                    Suspicious activity detected in Indore.
                  </p>

                  <small>
                    2 minutes ago
                  </small>

                </div>

              </div>

              {/* ALERT 2 */}

              <div className="notification-item">

                <div className="notification-dot warning"></div>

                <div>

                  <strong>
                    New Prediction
                  </strong>

                  <p>
                    New cybercrime prediction is available.
                  </p>

                  <small>
                    10 minutes ago
                  </small>

                </div>

              </div>

              <Link
                href="/alerts"
                className="view-all"
                onClick={() =>
                  setShowNotifications(false)
                }
              >
                View all alerts →
              </Link>

            </div>

          )}

        </div>

        {/* ====================================
            PROFILE
        ==================================== */}

        <div className="profile">

          <button
            type="button"
            className="profile-button"
            onClick={() =>
              setShowProfile(!showProfile)
            }
          >

            {/* AVATAR */}

            <div className="avatar">
              <User size={19} />
            </div>

            {/* USER INFORMATION */}

            <div className="profile-info">
<strong>
  {userName || "User"}
</strong>
             <small>Investigator</small>

            </div>

            <ChevronDown
              size={17}
              className={
                showProfile
                  ? "rotate-arrow"
                  : ""
              }
            />

          </button>

          {/* PROFILE DROPDOWN */}

          {showProfile && (

            <div className="profile-dropdown">

              {/* USER */}

              <div className="profile-dropdown-user">

                <div className="avatar">
                  <User size={19} />
                </div>

                <div>

                 <strong>
  {userName || "User"}
</strong>

               <small>Investigator</small>

                </div>

              </div>

              {/* REPORTS */}

              <Link href="/reports">

                <FileText size={16} />

                Reports

              </Link>

              {/* ALERTS */}

              <Link href="/alerts">

                <Bell size={16} />

                Security Alerts

              </Link>

              {/* SETTINGS */}

              <Link href="/settings">

                <Settings size={16} />

                Settings

              </Link>

              {/* LOGOUT */}

              <button
                type="button"
                onClick={handleLogout}
                className="logout-button"
              >

                <LogOut size={16} />

                Logout

              </button>

            </div>

          )}

        </div>

      </div>

    </header>
  );
}