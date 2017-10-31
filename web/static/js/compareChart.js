function XMLReq(callback) {
    var response = '';
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            response = this.responseText;
            callback(response);
        }
    };
    return xhttp;
}


function updateChart(callback) {
    var xhttp = XMLReq(callback);
    var local = window.location.origin;
    xhttp.open("GET", local + "/" + callback.name + "/", true);
    xhttp.send();
}


function chart1(response) {
    var chartData = JSON.parse(response);
    var ctx = document.getElementById("serverspeed").getContext('2d');
    var serverspeed = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            scales: {
                yAxes: [{
                    id: 'first-y-axis',
                    type: 'linear',
                    scaleLabel: {
                        display: true,
                        labelString: 'Time in milliseconds'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'No. of objects transferred'
                    }
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

function chart2(response) {
    var data = JSON.parse(response);
    var json_data = data['json'];
    var xml_data = data['xml'];

    // Now I have the variables, I need to do the async requests to all the variables.
    var json_time = [];
    var xml_time = [];

    for (var item in json_data) {
        var startTime = new Date().getMilliseconds();
        var json_str = JSON.parse(json_data[item]);
        for (var obj in json_str) {
            var json_d = eval(json_str[obj]);
            var name = json_d.fields.name;
            var email = json_d.fields.email;
            var address = json_d.fields.address;
            var status = json_d.fields.status;
        }
        var endTime = new Date().getMilliseconds();
        var total = endTime - startTime;
        json_time.push(total);
    }

    console.log(json_time);

    // var parser = new DOMParser();
    //
    // for (var xitem in xml_data) {
    //     var sTime = new Date().getMilliseconds();
    //     var xmlDoc = parser.parseFromString(xml_data[xitem], "text/xml");
    //
    // }

}


