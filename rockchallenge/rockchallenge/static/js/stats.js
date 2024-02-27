const renderChart = (data, labels) => {
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Total de Investido: R$",
            data: data,
            backgroundColor: [
              "rgba(255, 99, 132)",
              "rgba(54, 162, 235)",
              "rgba(255, 206, 86)",
              "rgba(75, 192, 192)",
              "rgba(153, 102, 255)",
              "rgba(255, 159, 64)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
            hoverOffset: 4
          },
        ],
      },
      options: {
        title: {
          display: true,
          text: "Investimento por incorporadora",
        },
      },
    });
  };

const getChartData = () => {
    console.log("fetching");
    fetch("/investment_category_summary")
      .then((res) => res.json())
      .then((results) => {
        console.log("results", results,);
        const category_data = results.investment_category_data;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
  
        renderChart(data, labels);
      });
  };

document.onload = getChartData();
