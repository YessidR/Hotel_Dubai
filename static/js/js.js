
function actualizarRe(){
    document.getElementById('form').action="{{ url_for('reserva_editar',idreserva=r['idreserva'], idhab=r['idhabitacion']) }}";
}
function eliminarRe(){
    document.getElementById('form').action="{{ url_for('reserva_delete',id=r['idreserva'])}}";
}
