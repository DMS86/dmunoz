
function viewModel() {
    var self = this;

    self.notaMinima = ko.observable(1);
    self.notaMaxima = ko.observable(7);
    self.totalPuntos = ko.observable(10);
    self.porcentaje = ko.observable(60);
    self.redondearNotaLimiteParaAbajo = ko.observable(false);
    self.notaLimite = ko.observable(4);

    self.checkValoresNotas = function() {
        if (self.notaMaxima() <= self.notaMinima()) {
            alert("La nota máxima debe ser mayor que la nota mínima. Los datos de la tabla no serán correctos.");
        }
    }

    self.puntajeNotaLimite = ko.computed(
        function() {
            var puntaje = parseFloat(this.totalPuntos());
            puntaje *= 2;
            var porcentaje = parseFloat(this.porcentaje())/100;

            if (this.redondearNotaLimiteParaAbajo()) {
                puntaje = Math.floor(puntaje * porcentaje);
            } else {
                puntaje = Math.round(puntaje * porcentaje);
            }
            return puntaje / 2;
        }, self
    );

    self.sumaEnRojos = ko.computed(
        function() {
            var notaLimite = parseFloat(self.notaLimite()); 
            var notaMinima = parseFloat(self.notaMinima());
            var puntajeNotaLimite = parseFloat(self.puntajeNotaLimite());
            var resultado = (notaLimite - notaMinima) / puntajeNotaLimite; 
            return (resultado == Infinity) ? 0 : resultado;
        }, self
    );

    self.sumaEnAzules = ko.computed(
        function() { 
            var notaMaxima = parseFloat(this.notaMaxima());
            var notaLimite = parseFloat(this.notaLimite());
            var totalPuntos = parseFloat(this.totalPuntos());
            var puntajeNotaLimite = parseFloat(this.puntajeNotaLimite())
            var resultado = (notaMaxima - notaLimite) / (totalPuntos - puntajeNotaLimite)
            return (resultado == Infinity) ? 0 : resultado; 
        }, self
    );

    self.redondearNotaUnDecimal = function(nota) {
        return Math.round( nota * 10 ) / 10;
    }

    self.calcularNota = function (indice) {
        var notaMinima = parseFloat(self.notaMinima());
        var notaLimite = parseFloat(self.notaLimite());
        var puntaje = indice / 2;
        var nota;
        var rojo = false;
        if (puntaje < self.puntajeNotaLimite()) {
            nota = notaMinima;
            rojo = true;
        } else {
            nota = notaLimite;
        }
        if (rojo) {
            nota = nota + (puntaje * self.sumaEnRojos());
        } else {
            nota = nota + ((puntaje - self.puntajeNotaLimite()) * self.sumaEnAzules());
        }
        nota = self.redondearNotaUnDecimal(nota);
        return nota;
    }
}

var vm = new viewModel();