import Header from "../components/header";
import Sidebar from "../components/sidebar";
import StatCards from "../components/statcards";
import RiskHeatmap from "../components/riskHeatmap";
import RecentAlerts from "../components/recentAlerts";
import RecentActivities from "../components/recentActivities";
import ComplaintsTrend from "../components/complaintsTrend";
import FraudTypes from "../components/fraudTypes";
import PredictionPerformance from "../components/predictionperformance";
import Footer from "../components/footer";


export default function Home() {
  return (
    <div className="app">

      <Header />

      <Sidebar />

      <main className="main-content">

        {/* Welcome Section */}
        <section className="welcome-section">

          <div>
            <h1>Good Evening, Investigator</h1>

            <p>
              Here&apos; your current cybercrime intelligence overview.
            </p>
          </div>

          <div className="welcome-right">

            <div className="date-time">

              <span>
                📅 Fri, 5 Sep 2026
              </span>

              <span>
                🕒 08:24 PM
              </span>

            </div>

            <button className="simulate-btn">
              <span>⚡ Simulate Fraud </span>
              <span>→</span>
            </button>

          </div>

        </section>

        {/* Statistics */}
        <StatCards />

        {/* Main Dashboard */}
        <section className="dashboard-grid">

          <div className="dashboard-left">

            <RiskHeatmap />

            <section className="bottom-charts">

              <ComplaintsTrend />

              <FraudTypes />

              <PredictionPerformance />

            </section>

          </div>

          <div className="dashboard-right">

            <RecentAlerts />

            <RecentActivities />

          </div>

        </section>

      </main>
      <Footer/>

    </div>
  );
}