function jsontolist(data){
    result = [];
    for(var i in data)
        result.push([data[i]]);
    return result;
};

$(document).ready(function() { 
    google.charts.load('current', {'packages':['corechart']});
    document.getElementById('btn-donut').addEventListener("click", function() {
        grafico_productos(document.getElementById('btn-donut'));
    });
    document.getElementById('btn-bar').addEventListener("click", function() {
        tabla_productos(document.getElementById('btn-bar'));
    });
});

function chartPie(list) {
    var data = google.visualization.arrayToDataTable(list);
    var options = {
        title: 'Stock de Productos'
    };
    var chart = new google.visualization.PieChart(document.getElementById('data-container'));
    chart.draw(data, options);
};

function chartBar(list) {
    var data = google.visualization.arrayToDataTable(list);
    var options = {
        title: 'Stock de Productos'
    };
    var chart = new google.visualization.BarChart(document.getElementById('data-container'));
    chart.draw(data, options);
};

function grafico_productos(d){
    var _url = d.getAttribute("data-url")
    $.ajax({
        url: _url,
        dataType: 'json',
        success: function (data) {
            google.setOnLoadCallback(chartPie(data));
        }
        });
};

function tabla_productos(d){
    var _url = d.getAttribute("data-url")
    $.ajax({
        url: _url,
        dataType: 'json',
        success: function (data) {
            google.setOnLoadCallback(chartBar(data));
        }
        });
};