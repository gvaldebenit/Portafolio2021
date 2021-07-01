
// Lector de Funcion de Botones
$(document).ready(function() { 
    google.charts.load('current', {'packages':['corechart','controls','controls']});
    document.getElementById('btn-today').addEventListener("click", function() { //Boton Para ventas de hoy
      grafico(document.getElementById('btn-today'));
    });
    document.getElementById('btn-week').addEventListener("click", function() { //Boton para ventas semanal
      grafico(document.getElementById('btn-week'));
    });
    document.getElementById('btn-month').addEventListener("click", function() { //Boton para ventas mensual
      grafico(document.getElementById('btn-month'));
    });
    document.getElementById('btn-year').addEventListener("click", function() { //Boton para ventas anual
      grafico(document.getElementById('btn-year'));
    });
    document.getElementById('btn-today-doc').addEventListener("click", function() { //Boton Para ventas de hoy
      graficoDoc(document.getElementById('btn-today-doc'));
    });
    document.getElementById('btn-week-doc').addEventListener("click", function() { //Boton para ventas semanal
      graficoDoc(document.getElementById('btn-week-doc'));
    });
    document.getElementById('btn-month-doc').addEventListener("click", function() { //Boton para ventas mensual
      graficoDoc(document.getElementById('btn-month-doc'));
    });
    document.getElementById('btn-year-doc').addEventListener("click", function() { //Boton para ventas anual
      graficoDoc(document.getElementById('btn-year-doc'));
    });
    // Botones Secundarios
    document.getElementById('btn-producto').addEventListener("click", function() {
      $('.venta-doc').hide(); //Hide others groups
      $('.venta-producto').show(); //Show clicked group
    });
    document.getElementById('btn-doc').addEventListener("click", function() {
      $('.venta-producto').hide(); //Hide others groups
      $('.venta-doc').show(); //Show clicked group
    });
});


// Crear Dashboard
function drawMainDashboard(list) {
  var dashboard = new google.visualization.Dashboard(
      document.getElementById('data-container'));
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
  var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'data-control-cat',
    'options': {
      'filterColumnIndex': 3,
      'ui': {
        'labelStacking': 'vertical',
        'label': 'Familia Producto:',
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
  // Total Ventas
  // Grafico de Pie
  var pieTotal = new google.visualization.ChartWrapper({
    'chartType': 'PieChart',
    'containerId': 'data-pie-total',
    'options': {
      'width': 600,
      'height': 600,
      'legend': 'none',
      'chartArea': {'left': 15, 'top': 15, 'right': 0, 'bottom': 0},
      'pieSliceText': 'label'
    },
    'view': {'columns': [0, 2]}
  });
  var table = new google.visualization.ChartWrapper({
    'chartType': 'Table',
    'containerId': 'data-chart',
    'options': {
    }
  });
  
  if(list.length > 1){
    try{
      var data = google.visualization.arrayToDataTable(list);
      dashboard.bind([cantslider, categoryPicker], [pie, pieTotal, table]);
      dashboard.draw(data);
    } catch (e) {
      $("#data-container").html("Error al procesar los datos. Intente Recargar la Página");
    }
  } else{
    $("#data-container").html("No hay Datos Para Mostrar");
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

// Dashboard para Documentos
function drawMainDashboardDocs(list) {
  var dashboard = new google.visualization.Dashboard(
      document.getElementById('data-container'));
  // Control para tipo Doc
  var categoryPicker = new google.visualization.ControlWrapper({
    'controlType': 'CategoryFilter',
    'containerId': 'data-control-cat',
    'options': {
      'filterColumnIndex': 0,
      'ui': {
        'labelStacking': 'vertical',
        'label': 'Tipo Documento:',
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
  // Total Ventas
  // Grafico de Pie
  var pieTotal = new google.visualization.ChartWrapper({
    'chartType': 'PieChart',
    'containerId': 'data-pie-total',
    'options': {
      'width': 600,
      'height': 600,
      'legend': 'none',
      'chartArea': {'left': 15, 'top': 15, 'right': 0, 'bottom': 0},
      'pieSliceText': 'label'
    },
    'view': {'columns': [0, 2]}
  });
  var table = new google.visualization.ChartWrapper({
    'chartType': 'Table',
    'containerId': 'data-chart',
    'options': {
    }
  });
  
  if(list.length > 1){
    try{
      var data = google.visualization.arrayToDataTable(list);
      dashboard.bind([categoryPicker], [pie, pieTotal, table]);
      dashboard.draw(data);
    } catch (e) {
      $("#data-container").html("Error al procesar los datos. Intente Recargar la Página");
    }
  } else{
    $("#data-container").html("No hay Datos Para Mostrar");
  };
};

function graficoDoc(d){
  var _url = d.getAttribute("data-url")
  $.ajax({
      url: _url,
      dataType: 'json',
      success: function (data) {
          google.setOnLoadCallback(drawMainDashboardDocs(data));
      }
      });
};
