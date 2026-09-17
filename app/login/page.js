"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Shield, User, Mail, Lock } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    setError("");

    // Check fields
    if (!name.trim() || !email.trim() || !password.trim()) {
      setError("Please fill in all fields.");
      return;
    }

    // Save login information
    localStorage.setItem("loggedIn", "true");

    localStorage.setItem(
      "user",
      JSON.stringify({
        name: name.trim(),
        email: email.trim(),
      })
    );

    // Go to dashboard
    router.push("/");
  };

  return (
    <main className="login-page">

      <div className="login-card">

        {/* LOGO */}

        <div className="login-logo">
          <div className="login-logo-icon">
            <Shield size={42} />
          </div>

          <h1>
            CYBER<span>TRACE</span>
          </h1>

          <p>Predict • Prevent • Protect</p>
        </div>


        <h2>Welcome Back</h2>

        <p className="login-subtitle">
          Sign in to access your cybercrime intelligence dashboard.
        </p>


        <form onSubmit={handleLogin}>

          {/* NAME */}
<div className="login-field">
  <label htmlFor="name">Name</label>

  <div className="input-box">
    <User size={18} />

    <input
      id="name"
      type="text"
      placeholder="Enter your name"
      value={name}
      onChange={(e) => setName(e.target.value)}
    />
  </div>
</div>
          {/* EMAIL */}

          <div className="login-field">
  <label htmlFor="email">Email</label>

  <div className="input-box">
    <Mail size={18} />

    <input
      id="email"
      type="email"
      placeholder="Enter your email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
    />
  </div>
</div>


          {/* PASSWORD */}

          <div className="login-field">
  <label htmlFor="password">Password</label>

  <div className="input-box">
    <Lock size={18} />

    <input
      id="password"
      type="password"
      placeholder="Enter your password"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
    />
  </div>
</div>


          {/* ERROR */}

          {error && (
            <p className="login-error">
              {error}
            </p>
          )}


          {/* BUTTON */}

          <button
            type="submit"
            className="login-button"
          >
            Sign In
          </button>

        </form>

      </div>

    </main>
  );
}