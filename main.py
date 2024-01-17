from flask import flash, Flask, render_template, request, url_for, redirect, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from modelo.dao import db, Usuario, Barbero, Publicacion, HistorialCompra, Comentario, Barberia, Producto, Carrito
from datetime import date, time, datetime, timedelta
from flask_bootstrap import Bootstrap
from uuid import uuid4

app= Flask(__name__)
Bootstrap(app)

app.secret_key = 'laliboriza'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/barberia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message='Tu sesión expiró'
login_manager.login_message_category='info'

@login_manager.user_loader
def cargar_usuario(userId):
    return Usuario.query.get(int(userId))

@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def raiz():
    return render_template('inicio.html')

@app.route('/login', methods=['get','post'])
def login():
    if(request.method == 'POST'):   
        correo=request.form['correo']
        contrasena=request.form['contrasena']
        usuario = Usuario()
        usuario = usuario.validar(correo)
        if(usuario != None and usuario.contrasena == contrasena):
            login_user(usuario)
            return redirect(url_for('publicaciones'))
        else:
            return render_template('login.html', msg = "Datos incorrectos")
    else:
        return render_template('login.html')

@app.route('/regUsuario', methods=['get', 'post'])
def registrarUsuario():
    try:
        if request.method == 'POST':
            usuario = Usuario()
            usuario.nombre = request.form['nombre']
            usuario.apellido = request.form['apellido']
            usuario.correo = request.form['correo']
            usuario.contrasena = request.form['contrasena']
            usuario.telefono = request.form['telefono']
            usuario.fechaNacimiento = request.form['fechaNacimiento']
            usuario.sexo = request.form['sexo']
            usuario.foto = request.files['foto'].stream.read()
            usuario.agregar()
            return redirect(url_for('login'))
        else:
            return render_template('registrarUsuario.html')
    except Exception:
        return render_template('registrarUsuario.html')
    

@app.route('/regBarbero', methods=['get', 'post'])
@login_required
def registrarBarbero():
    barberias = Barberia().consultaGeneral()
    usuarioActual = current_user.userId  # Retrieve user ID from the session
    if request.method == 'POST':
         barbero = Barbero()
         barbero.userId = usuarioActual
         barbero.precios = request.form['precios']
         barbero.especialidad = request.form['especialidad']
         barbero.horario = request.form['horario']
         barbero.barberiaId = request.form['barberia']
         barbero.agregar()
         return redirect(url_for('publicaciones'))
    else:
         return render_template('registrarBarbero.html',esUsuario=True, barberias = barberias)

@app.route('/registrarBarberia', methods=['get', 'post'])
@login_required
def registrarBarberia():
    if request.method == 'POST':
         barberia = Barberia()
         barberia.nombre = request.form['nombre']
         barberia.ubicacion = request.form['ubicacion']
         barberia.calificacion = request.form['calificacion']
         barberia.servicios = request.form['servicios']
         barberia.agregar()
         return redirect(url_for('registrarBarbero'))
    else:
         return render_template('registrarBarberia.html', esUsuario=True)

@app.route('/mostrarPublicaciones')
@login_required
def publicaciones():
    try:
        publicaciones = Publicacion().consultaGeneral()
        esBarbero = False
        barber = Barbero().consultaPorUsuario(current_user.userId)

        if barber:
            esBarbero = True
            barber_id = barber.barberoId
        else:
            barber_id = None


        return render_template('publicaciones.html', esBarbero=esBarbero, publicaciones=publicaciones, barberId=barber_id, esUsuario=True, idUser=current_user.userId)
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        # Handle the error appropriately, redirect to an error page, or show a message
        return render_template('error.html', error_message="Error occurred while fetching publications")


@app.route('/crearPublicacion', methods=['get', 'post'])
@login_required
def crearPublicacion():
    if request.method == 'POST':
        publicacion = Publicacion()
        publicacion.barberoId = Barbero().consultaPorUsuario(current_user.userId).barberoId
        publicacion.titulo = request.form['titulo']
        publicacion.contenido = request.form['contenido']
        publicacion.fecha = date.today()
        publicacion.hora = datetime.now().time()
        publicacion.foto = request.files['foto'].stream.read()
        publicacion.agregar()
        return redirect(url_for('publicaciones'))
    else:
        barber = Barbero().consultaPorUsuario(current_user.userId)

        if barber:
            return render_template('crearPublicacion.html', esUsuario=True)
        else:
            return redirect(url_for('publicaciones'))
        

@app.route('/editarPublicacion/<int:idPub>', methods=['post', 'get'])
@login_required
def editar(idPub):
    pubM = Publicacion()
    pubM=pubM.consultaIndividual(idPub)
    if(request.method == 'POST'):
        pubM.titulo = request.form['titulo']
        pubM.contenido = request.form['contenido']
        pubM.fecha = date.today()
        pubM.hora = datetime.now().time()
        pubM.foto = request.files['fotoP'].stream.read()
        pubM.editar()
        return redirect(url_for('publicaciones'))
    else:
        barber = Barbero().consultaPorUsuario(current_user.userId)

        if barber:
            return render_template('editarPublicacion.html', pubM=pubM, esUsuario=True)
        else:
            return redirect(url_for('publicaciones'))
        
    
@app.route('/eliminarPublicacion/<int:idPub>', methods=['post', 'get'])
@login_required
def eliminar(idPub):
    pubE = Publicacion().consultaIndividual(idPub)
    if request.method == 'POST':
        pubE.eliminar()
        return redirect(url_for('publicaciones'))
    else:
        barber = Barbero().consultaPorUsuario(current_user.userId)

        if barber:
            return render_template('eliminarPublicacion.html', pubE=pubE, esUsuario=True)
        else:
            return redirect(url_for('publicaciones'))
        



@app.route('/crearComentario/<int:idPub>', methods=['get', 'post'])
@login_required
def crearComentario(idPub):
    if request.method == 'POST':
        comentario = Comentario()
        comentario.publicacionId = idPub
        comentario.userId = current_user.userId
        comentario.contenido = request.form['comentario']
        comentario.fecha = date.today()
        comentario.hora = datetime.now().time()
        comentario.agregar()
        return redirect(url_for('publicaciones'))
        

@app.route('/mostrarProductos')
@login_required
def productos():
    try:
        productos = Producto().consultaGeneral()
        return render_template('productos.html', productos = productos, idUser=current_user.userId, esUsuario=True)
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        # Handle the error appropriately, redirect to an error page, or show a message
        return render_template('error.html', error_message="Error occurred while fetching publications")

@app.route('/crearProducto', methods=['get', 'post'])
@login_required
def crearProducto():
    if request.method == 'POST':
        producto = Producto()
        producto.productoId = int(uuid4().int%100)
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = request.form['precio']
        producto.stock = request.form['stock']
        producto.foto = request.files['foto'].stream.read()
        producto.agregar()
        return redirect(url_for('productos'))
    else:
        return render_template('crearProducto.html', esUsuario=True)


@app.route('/mostrarDetallesProducto/<int:idProd>')
@login_required
def detallesProducto(idProd):
    prod = Producto().consultaIndividual(idProd)
    return render_template('detallesProducto.html', producto = prod, esUsuario=True)

@app.route('/carrito/<int:product_id>')
@login_required
def agregar_al_carrito(product_id):
    # Lógica para agregar un producto al carrito
    # Puedes utilizar sesiones para mantener el carrito por usuario
    # Por ejemplo:
    cart_item = Carrito.query.filter_by(userId=current_user.userId, productoId=product_id).first()

    if cart_item:
        # Si el producto ya está en el carrito, incrementa la cantidad
        cart_item.cantidad += 1
        flash('Producto agregado al carrito', 'success')
    else:
        # Si no está en el carrito, crea un nuevo item en el carrito
        new_cart_item = Carrito(userId=current_user.userId, productoId=product_id, cantidad=1)
        db.session.add(new_cart_item)
        flash('Producto agregado al carrito', 'success')

    db.session.commit()
    
    return redirect(url_for('productos'))


@app.route('/verCarrito',methods=['POST', 'GET'])
@login_required
def ver_carrito():
    cart_items = Carrito.query.filter_by(userId=current_user.userId).all()
    return render_template('carrito.html', cart_items=cart_items, esUsuario=True)

@app.route('/eliminarProductoCarrito/<int:product_id>', methods=['POST'])
@login_required
def eliminar_producto_carrito(product_id):
    cart_item = Carrito.query.filter_by(userId=current_user.userId, productoId=product_id).first()

    if cart_item:
        cart_item.eliminar()
        flash('Producto eliminado del carrito', 'success')

    return redirect(url_for('ver_carrito'))

@app.route('/eliminarCarrito', methods=['POST'])
@login_required
def eliminar_carrito():
    cart_items = Carrito.query.filter_by(userId=current_user.userId).all()

    if cart_items:
        for cart_item in cart_items:
            cart_item.eliminar()
        flash('Carrito eliminado', 'success')

    return redirect(url_for('ver_carrito'))


@app.route('/completarCompra', methods=['POST'])
@login_required
def completar_compra():
    try:
        cart_items = Carrito.query.filter_by(userId=current_user.userId).all()

        if cart_items:
            for cart_item in cart_items:
                producto = Producto.query.get(cart_item.productoId)
                if producto.stock >= cart_item.cantidad:
                    # Reduce el stock del producto según la cantidad en el carrito
                    producto.stock -= cart_item.cantidad


                    historial_compra = HistorialCompra(
                    userId=current_user.userId,
                    productoId=cart_item.productoId,
                    cantidad=cart_item.cantidad,
                    fecha=datetime.now()  
                    )
                    historial_compra.agregar()
                    # Elimina el elemento del carrito
                    cart_item.eliminar()
                else:
                    flash(f'No hay suficiente stock para {producto.nombre}', 'danger')
                    return redirect(url_for('ver_carrito'))

            # Commit de los cambios en la base de datos
            db.session.commit()
            flash('¡Compra completada con éxito!', 'success')
        else:
            flash('El carrito está vacío', 'warning')

        return redirect(url_for('ver_carrito'))

    except Exception as e:
        flash('Ocurrió un error al completar la compra', 'danger')
        print(f"Error occurred: {str(e)}")
        return redirect(url_for('ver_carrito'))

@app.route('/historialCompras')
@login_required
def historial_compras():
    try:
        historial = HistorialCompra.query.filter_by(userId=current_user.userId).all()
        # Puedes pasar este historial a un template para mostrarlo al usuario
        return render_template('historialCompras.html', historial=historial, esUsuario = True)

    except Exception as e:
        flash('Ocurrió un error al mostrar el historial de compras', 'danger')
        print(f"Error occurred: {str(e)}")
        return redirect(url_for('ver_carrito'))


@app.route('/perfil/<int:idUser>', methods = ['get', 'post'])
@login_required
def perfil(idUser):
    user = Usuario().consultaIndividual(idUser)
    barber = Barbero().consultaPorUsuario(idUser)
    return render_template('perfil.html', user=user,  barber = barber, esUsuario=True)

@app.route('/consultarFotoPerfil/<int:idUser>')
def imgUser(idUser):
    user = Usuario()
    return user.consultarImagen(idUser)

@app.route('/consultarImgPub/<int:idPub>')
def imgPub(idPub):
    pub = Publicacion()
    return pub.consultarImagen(idPub)

@app.route('/consultarImgProd/<int:idProd>')
def imgProd(idProd):
    prod = Producto()
    return prod.consultarImagen(idProd)

if __name__=='__main__':
    db.init_app(app)
    app.run(debug=True) #se habilita el debug para que la app web sea sensible a l-os cambios