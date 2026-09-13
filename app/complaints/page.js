"use client";

import { useState } from "react";
import {
  MessageSquareWarning,
  Search,
  Filter,
  Clock3,
  CheckCircle2,
  AlertTriangle,
  Users,
  Plus,
  X,
  MapPin,
  UserRound,
} from "lucide-react";

const initialComplaints = [
  {
    id: "CMP-2048",
    title: "Unauthorized Bank Transaction",
    description: "A suspicious transaction was reported by the account holder.",
    category: "Financial Fraud",
    priority: "Critical",
    status: "Under Investigation",
    location: "New Delhi",
    complainant: "Amit Sharma",
    time: "12 min ago",
  },
  {
    id: "CMP-2047",
    title: "Online Shopping Scam",
    description: "Customer reported payment made for an order that was never delivered.",
    category: "Online Scam",
    priority: "High",
    status: "Open",
    location: "Mumbai",
    complainant: "Priya Verma",
    time: "35 min ago",
  },
  {
    id: "CMP-2046",
    title: "Suspicious Phishing Email",
    description: "A malicious email containing a suspicious login link was reported.",
    category: "Phishing",
    priority: "High",
    status: "Under Investigation",
    location: "Bengaluru",
    complainant: "Rahul Singh",
    time: "1 hour ago",
  },
  {
    id: "CMP-2045",
    title: "Identity Misuse",
    description: "Personal information appears to have been used without authorization.",
    category: "Identity Theft",
    priority: "Medium",
    status: "Open",
    location: "Bhopal",
    complainant: "Neha Gupta",
    time: "2 hours ago",
  },
  {
    id: "CMP-2044",
    title: "Social Media Fraud",
    description: "Complaint regarding a fraudulent social media account.",
    category: "Online Fraud",
    priority: "Medium",
    status: "Resolved",
    location: "Hyderabad",
    complainant: "Arjun Patel",
    time: "4 hours ago",
  },
];

export default function ComplaintsPage() {
  const [complaints, setComplaints] = useState(initialComplaints);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("All");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const [newComplaint, setNewComplaint] = useState({
    title: "",
    category: "Online Fraud",
    priority: "Medium",
    location: "",
    complainant: "",
    description: "",
  });

  const filteredComplaints = complaints.filter((complaint) => {
    const searchText = search.toLowerCase();

    const matchesSearch =
      complaint.id.toLowerCase().includes(searchText) ||
      complaint.title.toLowerCase().includes(searchText) ||
      complaint.location.toLowerCase().includes(searchText) ||
      complaint.complainant.toLowerCase().includes(searchText);

    const matchesStatus =
      statusFilter === "All" ||
      complaint.status === statusFilter;

    const matchesCategory =
      categoryFilter === "All" ||
      complaint.category === categoryFilter;

    return matchesSearch && matchesStatus && matchesCategory;
  });

  const resolveComplaint = (id) => {
    setComplaints((current) =>
      current.map((complaint) =>
        complaint.id === id
          ? { ...complaint, status: "Resolved" }
          : complaint
      )
    );

    if (selectedComplaint?.id === id) {
      setSelectedComplaint({
        ...selectedComplaint,
        status: "Resolved",
      });
    }
  };

  const addComplaint = (event) => {
    event.preventDefault();

    if (!newComplaint.title || !newComplaint.complainant) {
      return;
    }

    
  

  const complaint = {
    id: `CMP-${2050 + complaints.length}`,
    title: newComplaint.title,
    description: newComplaint.description,
    category: newComplaint.category,
    priority: newComplaint.priority,
    status: "Open",
    location: newComplaint.location || "Not specified",
    complainant: newComplaint.complainant,
    time: "Just now",
  };

  setComplaints((current) => [
    complaint,
    ...current,
  ]);

  setNewComplaint({
    title: "",
    category: "Online Fraud",
    priority: "Medium",
    location: "",
    complainant: "",
    description: "",
  });

  setShowForm(false);
};

  const totalComplaints = complaints.length;

  const openComplaints = complaints.filter(
    (complaint) => complaint.status === "Open"
  ).length;

  const investigatingComplaints = complaints.filter(
    (complaint) => complaint.status === "Under Investigation"
  ).length;

  const resolvedComplaints = complaints.filter(
    (complaint) => complaint.status === "Resolved"
  ).length;

  return (
    <main className="complaints-page">

      {/* HEADER */}
      <section className="complaints-header">

        <div className="complaints-heading">

          <div className="complaints-title-icon">
            <MessageSquareWarning size={27} />
          </div>

          <div>
            <span className="complaints-label">
              CITIZEN CYBERCRIME REPORTING
            </span>

            <h1>Complaints</h1>

            <p>
              Manage, investigate and track reported cybercrime
              complaints.
            </p>
          </div>

        </div>

        <button
          type="button"
          className="add-complaint-btn"
          onClick={() => setShowForm(true)}
        >
          <Plus size={18} />
          New Complaint
        </button>

      </section>

      {/* STATISTICS */}
      <section className="complaint-stats">

        <div className="complaint-stat-card">
          <div className="complaint-stat-icon total">
            <MessageSquareWarning size={21} />
          </div>

          <div>
            <span>Total Complaints</span>
            <strong>{totalComplaints}</strong>
            <small>All reported cases</small>
          </div>
        </div>

        <div className="complaint-stat-card">
          <div className="complaint-stat-icon open">
            <AlertTriangle size={21} />
          </div>

          <div>
            <span>Open</span>
            <strong>{openComplaints}</strong>
            <small>Awaiting action</small>
          </div>
        </div>

        <div className="complaint-stat-card">
          <div className="complaint-stat-icon investigation">
            <Users size={21} />
          </div>

          <div>
            <span>Under Investigation</span>
            <strong>{investigatingComplaints}</strong>
            <small>Currently being reviewed</small>
          </div>
        </div>

        <div className="complaint-stat-card">
          <div className="complaint-stat-icon resolved">
            <CheckCircle2 size={21} />
          </div>

          <div>
            <span>Resolved</span>
            <strong>{resolvedComplaints}</strong>
            <small>Successfully closed</small>
          </div>
        </div>

      </section>

      {/* MAIN PANEL */}
      <section className="complaints-panel">

        {/* TOOLBAR */}
        <div className="complaints-toolbar">

          <div className="complaint-search">
            <Search size={17} />

            <input
              type="text"
              placeholder="Search complaint, ID, person or location..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>

          <div className="complaint-filter">
            <Filter size={16} />

            <select
              value={statusFilter}
              onChange={(event) => setStatusFilter(event.target.value)}
            >
              <option value="All">All Status</option>
              <option value="Open">Open</option>
              <option value="Under Investigation">
                Under Investigation
              </option>
              <option value="Resolved">Resolved</option>
            </select>
          </div>

          <div className="complaint-filter">

            <select
              value={categoryFilter}
              onChange={(event) => setCategoryFilter(event.target.value)}
            >
              <option value="All">All Categories</option>
              <option value="Financial Fraud">
                Financial Fraud
              </option>
              <option value="Online Scam">
                Online Scam
              </option>
              <option value="Phishing">
                Phishing
              </option>
              <option value="Identity Theft">
                Identity Theft
              </option>
              <option value="Online Fraud">
                Online Fraud
              </option>
            </select>

          </div>

        </div>

        {/* LIST HEADER */}
        <div className="complaints-list-header">

          <div>
            <h2>Recent Complaints</h2>
            <span>
              Showing {filteredComplaints.length} complaints
            </span>
          </div>

          <div className="complaints-live">
            <span>Complaint system active</span>
            
          </div>

        </div>

        {/* COMPLAINT LIST */}
        <div className="complaints-list">

          {filteredComplaints.length === 0 ? (

            <div className="no-complaints">
              <CheckCircle2 size={42} />
              <h3>No complaints found</h3>
              <p>Try changing your search or filter.</p>
            </div>

          ) : (

            filteredComplaints.map((complaint) => (

              <article
                className="complaint-row"
                key={complaint.id}
              >

                <div
                  className={`complaint-priority ${complaint.priority.toLowerCase()}`}
                ></div>

                <div className="complaint-main-icon">
                  <MessageSquareWarning size={20} />
                </div>

                <div className="complaint-content">

                  <div className="complaint-title-row">

                    <h3>{complaint.title}</h3>

                    <span
                      className={`complaint-priority-badge ${complaint.priority.toLowerCase()}`}
                    >
                      {complaint.priority}
                    </span>

                  </div>

                  <p>{complaint.description}</p>

                  <div className="complaint-meta">

                    <span>{complaint.id}</span>

                    <span>
                      <MapPin size={13} />
                      {complaint.location}
                    </span>

                    <span>
                      <UserRound size={13} />
                      {complaint.complainant}
                    </span>

                    <span>
                      <Clock3 size={13} />
                      {complaint.time}
                    </span>

                  </div>

                </div>

                <div className="complaint-actions">

                  <span
                    className={`complaint-status ${complaint.status
                      .toLowerCase()
                      .replaceAll(" ", "-")}`}
                  >
                    {complaint.status}
                  </span>

                  <button
                    type="button"
                    className="complaint-view-btn"
                    onClick={() =>
                      setSelectedComplaint(complaint)
                    }
                  >
                    View
                  </button>

                  {complaint.status !== "Resolved" && (
                    <button
                      type="button"
                      className="complaint-resolve-btn"
                      onClick={() =>
                        resolveComplaint(complaint.id)
                      }
                    >
                      <CheckCircle2 size={14} />
                      Resolve
                    </button>
                  )}

                </div>

              </article>

            ))

          )}

        </div>

      </section>

      {/* DETAILS MODAL */}
      {selectedComplaint && (
        <div className="complaint-modal-overlay">

          <div className="complaint-modal">

            <div className="complaint-modal-header">

              <div>
                <span>COMPLAINT DETAILS</span>
                <h2>{selectedComplaint.title}</h2>
              </div>

              <button
                type="button"
                className="complaint-close-btn"
                onClick={() => setSelectedComplaint(null)}
                aria-label="Close complaint details"
              >
                <X size={19} />
              </button>

            </div>

            <div className="complaint-modal-id">
              {selectedComplaint.id}
            </div>

            <div className="complaint-detail-grid">

              <div>
                <span>Category</span>
                <strong>{selectedComplaint.category}</strong>
              </div>

              <div>
                <span>Priority</span>
                <strong>{selectedComplaint.priority}</strong>
              </div>

              <div>
                <span>Status</span>
                <strong>{selectedComplaint.status}</strong>
              </div>

              <div>
                <span>Location</span>
                <strong>{selectedComplaint.location}</strong>
              </div>

              <div>
                <span>Complainant</span>
                <strong>{selectedComplaint.complainant}</strong>
              </div>

              <div>
                <span>Reported</span>
                <strong>{selectedComplaint.time}</strong>
              </div>

            </div>

            <div className="complaint-description">
              <span>Description</span>
              <p>{selectedComplaint.description}</p>
            </div>

            {selectedComplaint.status !== "Resolved" && (
              <button
                type="button"
                className="modal-resolve-btn"
                onClick={() =>
                  resolveComplaint(selectedComplaint.id)
                }
              >
                <CheckCircle2 size={17} />
                Mark Complaint as Resolved
              </button>
            )}

          </div>

        </div>
      )}

      {/* ADD COMPLAINT MODAL */}
      {showForm && (
        <div className="complaint-modal-overlay">

          <div className="complaint-modal add-modal">

            <div className="complaint-modal-header">

              <div>
                <span>NEW CASE</span>
                <h2>Register Complaint</h2>
              </div>

              <button
                type="button"
                className="complaint-close-btn"
                onClick={() => setShowForm(false)}
                aria-label="Close new complaint form"
              >
                <X size={19} />
              </button>

            </div>

            <form onSubmit={addComplaint}>

              <label>
                Complaint Title

                <input
                  type="text"
                  placeholder="Enter complaint title"
                  value={newComplaint.title}
                  onChange={(event) =>
                    setNewComplaint({
                      ...newComplaint,
                      title: event.target.value,
                    })
                  }
                  required
                />
              </label>

              <div className="form-two-columns">

                <label>
                  Category

                  <select
                    value={newComplaint.category}
                    onChange={(event) =>
                      setNewComplaint({
                        ...newComplaint,
                        category: event.target.value,
                      })
                    }
                  >
                    <option>Online Fraud</option>
                    <option>Financial Fraud</option>
                    <option>Phishing</option>
                    <option>Online Scam</option>
                    <option>Identity Theft</option>
                  </select>
                </label>

                <label>
                  Priority

                  <select
                    value={newComplaint.priority}
                    onChange={(event) =>
                      setNewComplaint({
                        ...newComplaint,
                        priority: event.target.value,
                      })
                    }
                  >
                    <option>Critical</option>
                    <option>High</option>
                    <option>Medium</option>
                    <option>Low</option>
                  </select>
                </label>

              </div>

              <div className="form-two-columns">

                <label>
                  Complainant

                  <input
                    type="text"
                    placeholder="Full name"
                    value={newComplaint.complainant}
                    onChange={(event) =>
                      setNewComplaint({
                        ...newComplaint,
                        complainant: event.target.value,
                      })
                    }
                    required
                  />
                </label>

                <label>
                  Location

                  <input
                    type="text"
                    placeholder="City / Region"
                    value={newComplaint.location}
                    onChange={(event) =>
                      setNewComplaint({
                        ...newComplaint,
                        location: event.target.value,
                      })
                    }
                  />
                </label>

              </div>

              <label>
                Description

                <textarea
                  placeholder="Describe the complaint..."
                  value={newComplaint.description}
                  onChange={(event) =>
                    setNewComplaint({
                      ...newComplaint,
                      description: event.target.value,
                    })
                  }
                ></textarea>
              </label>

              <button
                type="submit"
                className="submit-complaint-btn"
              >
                <Plus size={17} />
                Register Complaint
              </button>

            </form>

          </div>

        </div>
      )}

    </main>
  );
}