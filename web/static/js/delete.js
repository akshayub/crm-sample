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

function do_nothing(data) {
}


function deleteObj(url)
{
    var xhttp = XMLReq(do_nothing);
    var local = window.location.origin;
    xhttp.open("GET", local + url, true);
    xhttp.send();
}