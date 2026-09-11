const performance = [

  {
    name: "Top-1",
    value: 58,
    color: "blue"
  },

  {
    name: "Top-3",
    value: 72,
    color: "green"
  },

  {
    name: "Top-5",
    value: 84,
    color: "purple"
  }

];


export default function PredictionPerformance() {

  return (

    <section className="chart-panel">

      <div className="chart-header">

        <h2>
          ▣ Prediction Performance
        </h2>

      </div>


      <div className="performance-list">

        {performance.map((item) => (

          <div
            className="performance-item"
            key={item.name}
          >

            <span>
              {item.name}
            </span>


            <div className="performance-bar">

              <div
                className={item.color}
                style={{
                  width: `${item.value}%`
                }}
              />

            </div>


            <strong>
              {item.value}%
            </strong>

          </div>

        ))}

      </div>

    </section>

  );
}