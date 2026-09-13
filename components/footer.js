import { ShieldCheck, Mail } from "lucide-react";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="footer">

      {/* Left */}
      <div className="footer-left">
        <div className="footer-logo">
          <ShieldCheck size={20} />
          <span>CYBERTRACE</span>
        </div>

        <p>
          AI-powered cybercrime monitoring & predictive risk analysis.
        </p>
      </div>

      {/* Links */}
      <div className="footer-links">
      <Link href="/">Dashboard </Link>
       <Link  href="/analytics">Analytics </Link>
    <Link  href="/reports">Reports </Link>
       <Link  href="/about">About </Link>
      </div>

      {/* Contact */}
      <div className="footer-right">

        <a
          href="https://github.com/"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="GitHub"
        >
          GitHub
        </a>

        <a
          href="mailto:contact@cybertrace.in"
          aria-label="Email"
        >
          <Mail size={18} />
        </a>

      </div>

      {/* Bottom */}
      <div className="footer-bottom">
        <span>© 2026 CYBERTRACE. All rights reserved.</span>
        <span>Built for Smart India Hackathon</span>
      </div>

    </footer>
  );
}