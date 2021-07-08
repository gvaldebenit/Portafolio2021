// Lector de Funcion de Botones
$(document).ready(function() { 
  google.charts.load('current', {'packages':['corechart','controls', 'line']});
  document.getElementById('btn-today').addEventListener("click", function() { //Boton Para ventas de hoy
    grafico(document.getElementById('btn-today'));
  });
  document.getElementById('btn-week').addEventListener("click", function() { //Boton para ventas semanal
    grafico(document.getElementById('btn-week'));
  });
  document.getElementById('btn-month').addEventListener("click", function() { //Boton para ventas mensual
    grafico(document.getElementById('btn-month'));
  });
});


// Crear Dashboard
function drawMainDashboard(list) {

// Grafico de line
var combochart = new google.visualization.ComboChart(document.getElementById('data-linegraph'));

$("#data-error").html("");
// Total Ventas
var table = new google.visualization.ChartWrapper({
  'chartType': 'Table',
  'containerId': 'data-chart',
  'options': {
  }
});
var options = {
  title : 'Visitas a la Pagina (Separados en Anonimos y Autenticados)',
  vAxis: {title: 'Visitas'},
  hAxis: {title: 'Tiempo'},
  seriesType: 'bars',
};

if(list.length > 1){
  try{
    var data = google.visualization.arrayToDataTable(list);
    combochart.draw(data, options);
    document.getElementById('btn-export').style.display='block';
      $('#csv').click(function () {
        var csv = google.visualization.dataTableToCsv(data);
        var encodedUri = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);
        this.href = encodedUri;
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "my_data.csv");
        document.body.appendChild(link); // Required for FF

        link.click(); // This will download the data file named "my_data.csv".
      });
  } catch (e) {
    $("#data-error").html("Error al procesar los datos. Intente Recargar la Página");
  }
} else{
  $("#data-error").html("No hay Datos Para Mostrar");
};
};

function grafico(d){
  var _url = d.getAttribute("data-url")
  $.ajax({
      url: _url,
      dataType: 'json',
      success: function (data) {
          google.setOnLoadCallback(drawMainDashboard(data));
      }
      });
};