import {
  FileText,
  AlertTriangle,
  ShieldCheck,
  TrendingUp,
  Users
} from "lucide-react";


const stats = [

  {
    title: "Total Complaints",
    value: "1,842",
    change: "12%",
    icon: FileText,
    color: "blue"
  },

  {
    title: "High Risk Locations",
    value: "24",
    change: "8%",
    icon: AlertTriangle,
    color: "red"
  },

  {
    title: "Predictions Today",
    value: "126",
    change: "15%",
    icon: ShieldCheck,
    color: "green"
  },

  {
    title: "Top-3 Accuracy",
    value: "72%",
    change: "6%",
    icon: TrendingUp,
    color: "purple"
  },

  {
    title: "Active Cases",
    value: "13",
    change: "4%",
    icon: Users,
    color: "orange"
  }

];


export default function StatCards() {

  return (

    <section className="stats-grid">

      {stats.map((stat) => {

        const Icon = stat.icon;

        return (

          <div
            className={`stat-card ${stat.color}`}
            key={stat.title}
          >

            <div className="stat-icon">
              <Icon size={23} />
            </div>


            <div className="stat-info">

              <h2>
                {stat.value}
              </h2>

              <p>
                {stat.title}
              </p>

              <span>
                ↑ {stat.change}
              </span>

            </div>


            <div className="mini-chart">

              <svg viewBox="0 0 100 40">

                <polyline
                  points="2,32 15,29 28,31 40,20 52,25 65,15 78,18 98,5"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="3"
                />

              </svg>

            </div>

          </div>

        );

      })}

    </section>

  );
}