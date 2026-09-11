import "./global.css";

export const metadata = {
  title: "CYBERTRACE",
  description: "AI-powered cybercrime monitoring and predictive risk analysis",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}


