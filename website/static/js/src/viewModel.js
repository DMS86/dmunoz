
function viewModel() {
    var self = this;

    self.notaMinima = ko.observable(1);
    self.notaMaxima = ko.observable(7);
    self.totalPuntos = ko.observable(10);
    self.porcentaje = ko.observable(60);
    self.redondear4ParaAbajo = ko.observable(false);

    self.puntajeNota4 = ko.computed(
        function() {
            var puntaje = parseFloat(this.totalPuntos());
            puntaje *= 2;

            if (this.redondear4ParaAbajo()) {
                puntaje = Math.floor(puntaje * parseInt(this.porcentaje())/100);
            } else {
                puntaje = Math.round(puntaje * parseInt(this.porcentaje())/100);
            }
            return puntaje / 2;
        }, self
    );

    self.sumaEnRojos = ko.computed(
        function() { 
            return (4 - parseFloat(self.notaMinima())) / (self.puntajeNota4()); 
        }, self
    );

    self.sumaEnAzules = ko.computed(
        function() { 
            return (7 - 4) / (parseInt(this.totalPuntos()) - (this.puntajeNota4())); 
        }, self
    );

    self.redondearNotaUnDecimal = function(nota) {
        return Math.round( nota * 10 ) / 10;
    }

    self.calcularNota = function (indice) {
        var notaMinima = parseFloat(self.notaMinima());
        var puntaje = indice / 2;
        var nota;
        var rojo = false;
        if (puntaje < self.puntajeNota4()) {
            nota = notaMinima;
            rojo = true;
        } else {
            nota = 4;
        }
        if (rojo) {
            nota = nota + (puntaje * self.sumaEnRojos());
        } else {
            nota = nota + ((puntaje - self.puntajeNota4()) * self.sumaEnAzules());
        }
        nota = self.redondearNotaUnDecimal(nota);
        return nota;
    }
}

var vm = new viewModel();