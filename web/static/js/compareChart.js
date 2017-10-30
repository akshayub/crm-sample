function chart1() {

    // Doing a Async GET request
    var response = "";
    var chartData;

    // var chartData = {
    //     labels: [10, 100, 1000],
    //     datasets: [{
    //         label: 'JSON',
    //         backgroundColor: 'rgba(255, 99, 132, 0.2)',
    //         borderColor: 'rgba(255,99,132,1)',
    //         data: [1, 9.73, 100],
    //         yAxisID: 'first-y-axis'
    //     },{
    //         label: 'XML',
    //         backgroundColor: 'rgba(54, 162, 235, 0.2)',
    //         borderColor: 'rgba(54, 162, 235, 1)',
    //         data: [2, 24, 150],
    //         yAxisID: 'first-y-axis'
    //     }]
    // };
    //
    // response = JSON.stringify(chartData);

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            response = this.responseText;
        }
    };

    var local = window.location.origin;


    // TODO: Again, plase forgive me for using Sync requests.
    xhttp.open("GET", local + "/chart/", false);
    xhttp.send();

    chartData = JSON.parse(response);
    console.log(response);

    var ctx = document.getElementById("serverspeed").getContext('2d');
    var serverspeed = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            scales: {
                yAxes: [{
                    id: 'first-y-axis',
                    type: 'linear'
                }]
            },
            responsive: true,
            legend: {
                position: 'top'
            },
            title: {
                display: true,
                text: 'XML vs JSON'
            }
        }
    });
}