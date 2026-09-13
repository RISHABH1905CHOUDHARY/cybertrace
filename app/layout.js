import "./global.css";
import Sidebar from "../components/sidebar";
import Header from "../components/header";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div className="app-layout">

          <Sidebar />

          <div className="page-area">
            <Header />

            <main className="main-content">
              {children}
            </main>
          </div>

        </div>
      </body>
    </html>
  );
}