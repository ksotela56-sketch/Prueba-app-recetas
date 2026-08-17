from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import categoria as categoria_model
from models import receta as receta_model

recetas_bp = Blueprint("recetas", __name__)


def _validar_formulario(form):
    """Valida los datos del formulario de receta y devuelve (datos, errores)."""
    errores = []

    nombre = form.get("nombre", "").strip()
    ingredientes = form.get("ingredientes", "").strip()
    pasos = form.get("pasos", "").strip()
    descripcion = form.get("descripcion", "").strip()
    tiempo_raw = form.get("tiempo_preparacion", "").strip()
    porciones_raw = form.get("porciones", "").strip()
    categoria_raw = form.get("categoria_id", "").strip()

    if not nombre:
        errores.append("El nombre es obligatorio.")
    if not ingredientes:
        errores.append("Los ingredientes son obligatorios.")
    if not pasos:
        errores.append("Los pasos son obligatorios.")

    tiempo_preparacion = None
    if tiempo_raw:
        if tiempo_raw.isdigit():
            tiempo_preparacion = int(tiempo_raw)
        else:
            errores.append("El tiempo de preparación debe ser un número entero.")

    porciones = None
    if porciones_raw:
        if porciones_raw.isdigit():
            porciones = int(porciones_raw)
        else:
            errores.append("Las porciones deben ser un número entero.")

    categoria_id = int(categoria_raw) if categoria_raw.isdigit() else None

    datos = {
        "nombre": nombre,
        "descripcion": descripcion or None,
        "ingredientes": ingredientes,
        "pasos": pasos,
        "tiempo_preparacion": tiempo_preparacion,
        "porciones": porciones,
        "categoria_id": categoria_id,
    }
    return datos, errores


@recetas_bp.route("/")
def index():
    nombre_buscado = request.args.get("q", "").strip() or None
    categoria_id = request.args.get("categoria", "").strip()
    categoria_id = int(categoria_id) if categoria_id.isdigit() else None

    recetas = receta_model.get_all(nombre=nombre_buscado, categoria_id=categoria_id)
    categorias = categoria_model.get_all()
    return render_template(
        "recetas/index.html",
        recetas=recetas,
        categorias=categorias,
        filtro_q=nombre_buscado or "",
        filtro_categoria=categoria_id,
    )


@recetas_bp.route("/recetas/<int:receta_id>")
def detalle(receta_id):
    receta = receta_model.get_by_id(receta_id)
    if receta is None:
        flash("La receta solicitada no existe.", "error")
        return redirect(url_for("recetas.index"))
    return render_template("recetas/detalle.html", receta=receta)


@recetas_bp.route("/recetas/nueva", methods=["GET", "POST"])
def nueva():
    if request.method == "POST":
        datos, errores = _validar_formulario(request.form)
        if errores:
            for error in errores:
                flash(error, "error")
            categorias = categoria_model.get_all()
            return render_template(
                "recetas/form.html", receta=datos, categorias=categorias, modo="crear"
            )
        receta_id = receta_model.create(datos)
        flash("Receta creada correctamente.", "success")
        return redirect(url_for("recetas.detalle", receta_id=receta_id))

    categorias = categoria_model.get_all()
    return render_template(
        "recetas/form.html", receta=None, categorias=categorias, modo="crear"
    )


@recetas_bp.route("/recetas/<int:receta_id>/editar", methods=["GET", "POST"])
def editar(receta_id):
    receta_existente = receta_model.get_by_id(receta_id)
    if receta_existente is None:
        flash("La receta solicitada no existe.", "error")
        return redirect(url_for("recetas.index"))

    if request.method == "POST":
        datos, errores = _validar_formulario(request.form)
        if errores:
            for error in errores:
                flash(error, "error")
            categorias = categoria_model.get_all()
            return render_template(
                "recetas/form.html", receta=datos, categorias=categorias, modo="editar", receta_id=receta_id
            )
        receta_model.update(receta_id, datos)
        flash("Receta actualizada correctamente.", "success")
        return redirect(url_for("recetas.detalle", receta_id=receta_id))

    categorias = categoria_model.get_all()
    return render_template(
        "recetas/form.html",
        receta=receta_existente,
        categorias=categorias,
        modo="editar",
        receta_id=receta_id,
    )


@recetas_bp.route("/recetas/<int:receta_id>/eliminar", methods=["POST"])
def eliminar(receta_id):
    receta_model.delete(receta_id)
    flash("Receta eliminada correctamente.", "success")
    return redirect(url_for("recetas.index"))
