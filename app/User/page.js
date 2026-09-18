"use client";

import { useState } from "react";

export default function Users() {

  const [users, setUsers] = useState([
    {
      id: 1,
      name: "Rishabh Choudhary",
      email: "rishabh@gmail.com",
      role: "Investigator",
      status: "Active",
    },
    {
      id: 2,
      name: "Rahul Sharma",
      email: "rahul@gmail.com",
      role: "Analyst",
      status: "Active",
    },
    {
      id: 3,
      name: "Priya Verma",
      email: "priya@gmail.com",
      role: "Investigator",
      status: "Inactive",
    },
  ]);

  const [search, setSearch] = useState("");

  const filteredUsers = users.filter(
    (user) =>
      user.name.toLowerCase().includes(search.toLowerCase()) ||
      user.email.toLowerCase().includes(search.toLowerCase())
  );

  const toggleStatus = (id) => {

    setUsers(
      users.map((user) =>
        user.id === id
          ? {
              ...user,
              status:
                user.status === "Active"
                  ? "Inactive"
                  : "Active",
            }
          : user
      )
    );
  };

  return (
    <div className="users-page">

      <div className="page-header">

        <div>
          <h1>Users</h1>

          <p>
            Manage CYBERTRACE investigators and system users.
          </p>
        </div>

        <button className="add-user">
          + Add User
        </button>

      </div>

      <div className="users-card">

        <div className="users-toolbar">

          <input
            type="text"
            placeholder="Search users..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

        </div>

        <div className="table-wrapper">

          <table>

            <thead>
              <tr>
                <th>User</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>

              {filteredUsers.map((user) => (

                <tr key={user.id}>

                  <td>
                    <div className="user-name">
                      <div className="avatar">
                        {user.name.charAt(0)}
                      </div>

                      {user.name}
                    </div>
                  </td>

                  <td>{user.email}</td>

                  <td>
                    <span className="role">
                      {user.role}
                    </span>
                  </td>

                  <td>

                    <span
                      className={
                        user.status === "Active"
                          ? "status active"
                          : "status inactive"
                      }
                    >
                      {user.status}
                    </span>

                  </td>

                  <td>

                    <button
                      className="status-btn"
                      onClick={() => toggleStatus(user.id)}
                    >
                      Change Status
                    </button>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>
    </div>
  );
}