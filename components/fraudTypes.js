const fraudTypes = [

  ["Phishing", "38%", "blue"],
  ["UPI Fraud", "27%", "red"],
  ["Investment", "18%", "yellow"],
  ["Identity Theft", "10%", "green"],
  ["Others", "7%", "purple"]

];


export default function FraudTypes() {

  return (

    <section className="chart-panel">

      <div className="chart-header">

        <h2>
          ◉ Fraud Types
        </h2>

      </div>


      <div className="fraud-content">

        <div className="donut-chart">

          <div className="donut-center">

            <strong>
              1,842
            </strong>

            <span>
              Total
            </span>

          </div>

        </div>


        <div className="fraud-legend">

          {fraudTypes.map(
            ([name, percentage, color]) => (

              <div
                className="fraud-item"
                key={name}
              >

                <i className={color}></i>

                <span>
                  {name}
                </span>

                <strong>
                  {percentage}
                </strong>

              </div>

            )
          )}

        </div>

      </div>

    </section>

  );
}