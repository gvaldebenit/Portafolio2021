// Lector de Funcion de Botones
$(document).ready(function() { 
    google.charts.load('current', {'packages':['corechart','controls','controls']});
    document.getElementById('btn-stock').addEventListener("click", function() { //Boton Para ventas de hoy
        grafico(document.getElementById('btn-stock'));
    });
});

// Crear Dashboard
function drawMainDashboard(list) {
  var dashboard = new google.visualization.Dashboard(
      document.getElementById('data-container'));
  $("#data-error").html("");
  // Control para la cantidad  
  var cantslider = new google.visualization.ControlWrapper({
    'controlType': 'NumberRangeFilter',
    'containerId': 'data-control-cant',
    'options': {
      'filterColumnIndex': 1,
      'ui': {
        'labelStacking': 'vertical',
        'label': 'Cantidad:'
      }
    }
  });
  // Control para la Familia del Producto
  var familyPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'data-control-fam',
    'options': {
      'filterColumnIndex': 2,
      'ui': {
        'labelStacking': 'vertical',
        'label': 'Familia Producto:',
        'allowTyping': false,
        'allowMultiple': true
      }
    }
  });
  // Control para el Tipo de Producto
  var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'data-control-cat',
    'options': {
      'filterColumnIndex': 3,
      'ui': {
        'labelStacking': 'vertical',
        'label': 'Tipo Producto:',
        'allowTyping': false,
        'allowMultiple': true
      }
    }
  });
  // Grafico de Pie
  var pie = new google.visualization.ChartWrapper({
    'chartType': 'PieChart',
    'containerId': 'data-pie',
    'options': {
      'width': 600,
      'height': 600,
      'legend': 'none',
      'chartArea': {'left': 15, 'top': 15, 'right': 0, 'bottom': 0},
      'pieSliceText': 'label'
    },
    'view': {'columns': [0, 1]}
  });
  // Tabla
  var table = new google.visualization.ChartWrapper({
    'chartType': 'Table',
    'containerId': 'data-chart',
    'options': {
    }
  });
  
  if(list.length > 1){
    try {
      var data = google.visualization.arrayToDataTable(list);
      dashboard.bind([cantslider, familyPicker, categoryPicker], [pie,table]);
      dashboard.draw(data);
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
    } catch (e){
      $("#data-error").html("Error al procesar los datos. Intente Recargar la P??gina");
    }
  } else{
    $("#data-error").html("No hay Datos Para Mostrar");
  } 
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