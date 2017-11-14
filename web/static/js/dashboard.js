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

function chart_update(callback){
    var xhttp = XMLReq(callback);
    var local = window.location.origin;
    xhttp.open("GET", local + "/api/" + callback.name + "/", true);
    xhttp.send();
}

function lead_db(response) {
    var chartData = JSON.parse(response);
    var ctx = document.getElementById("leadstatus").getContext('2d');
    var lead = new Chart(ctx, {
        type: 'doughnut',
        data: chartData,
        options: {
            responsive: true,
            legend: {
                position: 'top'
            },
            title: {
                display: true,
                text: 'Lead status'
            }
        }
    });
}

function oppo_db(response) {
    var chartData = JSON.parse(response);
    var ctx = document.getElementById("oppostatus").getContext('2d');
    var lead = new Chart(ctx, {
        type: 'doughnut',
        data: chartData,
        options: {
            responsive: true,
            legend: {
                position: 'top'
            },
            title: {
                display: true,
                text: 'Opportunities status'
            }
        }
    });
}


function fill(callback) {
    var xhttp = XMLReq(callback);
    var local = window.location.origin;
    xhttp.open("GET", local + "/api/recent_leads", true);
    xhttp.send();
}


function fill_leads(response) {
    var parsed = JSON.parse(JSON.parse(response));

    for (var obj in parsed) {
        var ob = parsed[obj];
        var pk = ob['pk'];
        var fields = ob['fields'];
        var name = fields['name'];
        $('#leadlist').append('<li><a href="/leads/'+ pk +'">' + name +'</a></li>');
    }
}