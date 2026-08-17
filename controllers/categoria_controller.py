import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import categoria as categoria_model

categorias_bp = Blueprint("categorias", __name__)


@categorias_bp.route("/categorias")
def index():
    categorias = categoria_model.get_all()
    return render_template("categorias/index.html", categorias=categorias)


@categorias_bp.route("/categorias/nueva", methods=["POST"])
def nueva():
    nombre = request.form.get("nombre", "").strip()
    if not nombre:
        flash("El nombre de la categoría es obligatorio.", "error")
    else:
        try:
            categoria_model.create(nombre)
            flash("Categoría creada correctamente.", "success")
        except sqlite3.IntegrityError:
            flash(f"Ya existe una categoría llamada '{nombre}'.", "error")
    return redirect(url_for("categorias.index"))
