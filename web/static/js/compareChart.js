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
                        labelString: 'Time in seconds'
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
                text: 'Data transfer speed'
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

    var parser = new DOMParser();

    for (var xitem in xml_data) {
        var sTime = new Date().getMilliseconds();
        var xmlText = xml_data[xitem];
        var xdoc = parser.parseFromString(xmlText, "text/xml");
        var objs = xdoc.getElementsByTagName("object");
        for (var count = 0; count < objs.length; count++) {
            var xmlobj = objs[count];
            var fields = xmlobj.childNodes;
            var xmlname = fields[1].innerHTML;
            var xmlemail = fields[4].innerHTML;
            var xmladdress = fields[2].innerHTML;
            var xmlstatus = fields[5].innerHTML;
        }
        var eTime = new Date().getMilliseconds();
        total = eTime - sTime;
        xml_time.push(total);
    }

    var dataset = {
        labels: [10, 100, 200, 500, 1000],
        datasets: [
            {
                label: 'JSON',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                data: json_time,
                borderWidth: 2,
                yAxisID: 'first-y-axis'
            },
            {
                label: 'XML',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                data: xml_time,
                borderWidth: 2,
                yAxisID: 'first-y-axis'
            }
        ]
    };


    var ctx = document.getElementById("clientresolve").getContext('2d');
    var clientResolve = new Chart(ctx, {
        type: 'bar',
        data: dataset,
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
                        labelString: 'No. of objects resolved'
                    }
                }]
            },
            responsive: true,
            legend: {
                position: 'top'
            },
            title: {
                display: true,
                text: 'Client Resolving Speed'
            }
        }
    });
}


function chart3(response) {
    var data = JSON.parse(response);
    var json_data = data['json'];
    var xml_data = data['xml'];

    var dataset = {
        labels: [10, 100, 200, 500, 1000],
        datasets: [
            {
                label: 'JSON',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                data: json_data,
                borderWidth: 2,
                yAxisID: 'first-y-axis'
            },
            {
                label: 'XML',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                data: xml_data,
                borderWidth: 2,
                yAxisID: 'first-y-axis'
            }
        ]
    };

    var ctx = document.getElementById("datasize").getContext('2d');
    var serverspeed = new Chart(ctx, {
        type: 'bar',
        data: dataset,
        options: {
            scales: {
                yAxes: [{
                    id: 'first-y-axis',
                    type: 'linear',
                    scaleLabel: {
                        display: true,
                        labelString: 'Size in kilobytes'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'No. of objects'
                    }
                }]
            },
            responsive: true,
            legend: {
                position: 'top'
            },
            title: {
                display: true,
                text: 'Data size'
            }
        }
    });
}