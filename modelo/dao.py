from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, BLOB, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__='Usuarios' 
    userId = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    correo = Column(String)
    contrasena = Column(String)
    telefono = Column(String)
    fechaNacimiento = Column(Date)
    sexo = Column(Integer)
    foto = Column(BLOB)
    barbero = relationship("Barbero", back_populates="usuario")

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.userId

    def consultaGeneral(self):
        return self.query.all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Usuario.query.get(id)
    
    def validar(self, correo):
        user = Usuario.query.filter(Usuario.correo == correo).first()
        return user

    def consultarImagen(sef, id):
        return Usuario().query.get(id).foto
    


class Barbero(db.Model):
    __tablename__='Barberos' 
    barberoId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('Usuarios.userId'))
    precios = Column(String)
    especialidad = Column(String)
    horario = Column(String)
    barberiaId = Column(Integer, ForeignKey('Barberia.barberiaId'))
    usuario = relationship("Usuario", back_populates="barbero") 
    barberia = relationship("Barberia", back_populates="barberos")

    def consultaGeneral(self):
        return self.query.all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Barbero().query.get(id)
    
    def consultaPorUsuario(self, user_id):
        return self.query.filter_by(userId=user_id).first()
    
class Barberia(db.Model):
    __tablename__='Barberia' 
    barberiaId = Column(Integer, primary_key=True)
    ubicacion = Column(String)
    nombre = Column(String)
    calificacion = Column(Integer)
    servicios = Column(String)
    barberos = relationship("Barbero", back_populates="barberia") 
    
    def consultaGeneral(self):
        return self.query.all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Barberia().query.get(id)

    
class Publicacion(db.Model):
    __tablename__='Publicaciones' 
    publicacionId = Column(Integer, primary_key=True)
    barberoId = Column(Integer, ForeignKey('Barberos.barberoId'))
    titulo = Column(String)
    contenido = Column(String)
    fecha = Column(Date)
    hora = Column(Time)
    foto = Column(BLOB)
    comentarios = relationship('Comentario', backref='Publicaciones', lazy='select')
    barbero = relationship("Barbero") 

    def consultaGeneral(self):
        return self.query.all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Publicacion().query.get(id)
    
    def consultarImagen(self, id):
        return Publicacion().query.get(id).foto
    


class Comentario(db.Model):
    __tablename__='Comentarios' 
    comentarioId = Column(Integer, primary_key=True)
    publicacionId = Column(Integer, ForeignKey('Publicaciones.publicacionId'))
    userId = Column(Integer, ForeignKey('Usuarios.userId'))
    contenido = Column(String)
    fecha = Column(Date)
    hora = Column(Time)
    usuario = relationship("Usuario") 
    
    def consultaGeneral(self):
        return self.query.all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Comentario().query.get(id)


class Producto(db.Model):
    __tablename__='Productos' 
    productoId = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    precio = Column(Float)
    stock = Column(Integer)
    foto = Column(BLOB)
    
    def consultaGeneral(self):
        return self.query.all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return Producto().query.get(id)
        
    def consultarImagen(self, id):
        return Producto().query.get(id).foto

    

class Carrito(db.Model):
    __tablename__='Carrito' 
    carritoId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('Usuarios.userId'))
    productoId = Column(Integer, ForeignKey('Productos.productoId'))
    cantidad = Column(Integer)
    producto = relationship("Producto")
        
    def consultaGeneral(self):
        return self.query.all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return CartItem().query.get(id)


class HistorialCompra(db.Model):
    __tablename__='HistorialCompra' 
    historialId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('Usuarios.userId'))
    productoId = db.Column(db.Integer, db.ForeignKey('Productos.productoId'))
    cantidad = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)
    producto = relationship("Producto")
        
    def consultaGeneral(self):
        return self.query.all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return HistorialCompra().query.get(id)

        