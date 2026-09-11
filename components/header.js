"use client";
import {
  Search,
  Bell,
  ChevronDown,
  Shield
} from "lucide-react";

export default function Header() {

  return (

    <header className="header">

      {/* Logo */}

      <div className="logo-area">

        <div className="logo-icon">
          <Shield size={38} />
        </div>

        <div>

          <h2>
            CYBER<span>TRACE</span>
          </h2>

          <p>
            Predict • Prevent • Protect
          </p>

        </div>

      </div>


      {/* Search */}

      <div className="search-container">

        <Search size={19} />

        <input
          type="text"
          placeholder="Search complaints, locations, cases..."
        />

        <kbd>⌘ K</kbd>

      </div>


      {/* Right */}

      <div className="header-right">

        <div className="notification">

          <Bell size={22} />

          <span>1</span>

        </div>


        <div className="profile">

          <div className="avatar">
            👤
          </div>

          <div className="profile-info">

            <strong>
              Rishabh Choudhary
            </strong>

            <small>
              Investigator
            </small>

          </div>

          <ChevronDown size={17} />

        </div>

      </div>

    </header>

  );
}