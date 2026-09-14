 "use client";

import { useState } from "react";
import {useRouter} from "next/navigation";
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
} from "lucide-react";

export default function Header() {
  const router = useRouter();

  const [search, setSearch] = useState("");
  const [showSearchResults, setShowSearchResults] = useState(false);

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

  const filteredItems = searchItems.filter((item) => {
    const query = search.toLowerCase().trim();

    return (
      item.name.toLowerCase().includes(query) ||
      item.keywords.toLowerCase().includes(query)
    );
  });

  const openSearchResult = (path) => {
    router.push(path);
    setSearch("");
    setShowSearchResults(false);
  };

  const handleSearch = (event) => {
    event.preventDefault();

    if (filteredItems.length > 0) {
      openSearchResult(filteredItems[0].path);
    }
  };
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);

  return (
    <header className="header">

     {/* LOGO - CLICK TO DASHBOARD */}
<Link href="/" className="logo-area" aria-label="Go to Dashboard">

  <div className="logo-icon">
    <Shield size={38} strokeWidth={2} />
  </div>

  <div className="logo-text">
    <h2>
      CYBER<span>TRACE</span>
    </h2>

    <p>Predict • Prevent • Protect</p>
  </div>

</Link>


     {/* SEARCH */}
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
            onClick={() => openSearchResult(item.path)}
          >

            <Search size={17} />

            <div>
              <strong>{item.name}</strong>

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


      {/* RIGHT */}
      <div className="header-right">

        {/* NOTIFICATION */}
        <div className="notification">

          <button
            type="button"
            className="notification-button"
            onClick={() =>
              setShowNotifications(!showNotifications)
            }
            aria-label="Open notifications"
          >
            <Bell size={22} />

            <span>1</span>
          </button>


          {/* Notification dropdown */}
          {showNotifications && (
            <div className="notification-dropdown">

              <div className="dropdown-title">
                <strong>Notifications</strong>

                <button
                  type="button"
                  onClick={() => setShowNotifications(false)}
                  aria-label="Close notifications"
                >
                  <X size={17} />
                </button>
              </div>


              <div className="notification-item">
                <div className="notification-dot critical"></div>

                <div>
                  <strong>High Risk Alert</strong>
                  <p>
                    Suspicious activity detected in Indore.
                  </p>
                  <small>2 minutes ago</small>
                </div>
              </div>


              <div className="notification-item">
                <div className="notification-dot warning"></div>

                <div>
                  <strong>New Prediction</strong>
                  <p>
                    New cybercrime prediction is available.
                  </p>
                  <small>10 minutes ago</small>
                </div>
              </div>


              <Link
                href="/alerts"
                className="view-all"
                onClick={() => setShowNotifications(false)}
              >
                View all alerts →
              </Link>

            </div>
          )}

        </div>


        {/* PROFILE */}
        <div className="profile">

          <button
            type="button"
            className="profile-button"
            onClick={() => setShowProfile(!showProfile)}
          >

            <div className="avatar">
              <User size={19} />
            </div>

            <div className="profile-info">

              <strong>
                Rishabh Choudhary
              </strong>

              <small>
                Investigator
              </small>

            </div>

            <ChevronDown
              size={17}
              className={showProfile ? "rotate-arrow" : ""}
            />

          </button>


          {/* Profile dropdown */}
          {showProfile && (
            <div className="profile-dropdown">

              <div className="profile-dropdown-user">

                <div className="avatar">
                  <User size={19} />
                </div>

                <div>
                  <strong>Rishabh Choudhary</strong>
                  <small>Investigator</small>
                </div>

              </div>


              <Link href="/reports">
                <FileText size={16} />
                Reports
              </Link>


              <Link href="/alerts">
                <Bell size={16} />
                Security Alerts
              </Link>


              <Link href="/settings">
                <Settings size={16} />
                Settings
              </Link>

            </div>
          )}

        </div>

      </div>

    </header>
  );
}