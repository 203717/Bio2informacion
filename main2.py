import tkinter as tk
import mysql.connector
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import paho.mqtt.client as mqtt

# Configuración de la conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'registromantenimiento'
}

# Crear la conexión
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

usuario_actual = None



class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.geometry("1084x700")  # Cambiar el tamaño de la ventana
        self._frame = None
        self.crear_interfaz()

    def crear_interfaz(self):
        imagen_fondo = Image.open("D:/descargas/proyectos-trabajo/nuevo/img/login.png")
        imagen_fondo = imagen_fondo.resize((1084, 700))
        self.foto_fondo = ImageTk.PhotoImage(imagen_fondo)


        label_fondo = tk.Label(self, image=self.foto_fondo)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        self.entry_usuario = tk.Entry(self, font=('Arial', 16))
        self.entry_usuario.place(x=410, y=270)


        self.entry_contrasena = tk.Entry(self, show="*", font=('Arial', 16))
        self.entry_contrasena.place(x=410, y=390)


        estilo_boton = {
            'font': ('Arial', 20, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 11,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }

    
        self.label_resultado = tk.Label(self, text="")
        self.label_resultado.place(x=470, y=420)

        self.button_login = tk.Button(self, text="Iniciar Sesión", command=self.login, **estilo_boton)
        self.button_login.place(x=330, y=470)

        boton = tk.Button(self, text="Registro", **estilo_boton, command=self.abrir_ventana_registro)
        boton.place(x=540, y=470)

    def login(self):
        global usuario_actual  # Indicar que se usará la variable global en esta función
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        cursor.execute('SELECT * FROM usuarios WHERE usuario=%s AND contrase=%s', (usuario, contrasena))
        user = cursor.fetchone()

        if user:
            tipo_usuario = user[3]  # El índice 3 corresponde al campo 'tipo'
            self.label_resultado.config(text="Inicio de sesión exitoso")
            usuario_actual = usuario  # Almacenar el usuario actual en la variable global

            if tipo_usuario == 1:
                self.abrir_ventana_admin()  # Sin necesidad de pasar el usuario
            elif tipo_usuario == 2:
                self.abrir_ventana_usuario()  # Sin necesidad de pasar el usuario
        else:
            self.label_resultado.config(text="Credenciales incorrectas")
    def abrir_ventana_admin(self):
        self.switch_frame(VentanaAdmin)
        
    def abrir_ventana_usuario(self):
        self.switch_frame(VentanaUsuario)   # Pasar el usuario a la ventana VentanaAdmin

    def abrir_ventana_registro(self):
        self.switch_frame(RegistroApp)

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self)  # Pasa el usuario a la ventana VentanaAdmin
        nuevo_frame.place(x=0, y=0, relwidth=1, relheight=1)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = nuevo_frame

class RegistroApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.crear_interfaz()


    def crear_interfaz(self):
        # Cargar la imagen de fondo de la ventana secundaria
        imagen_fondo_secundaria = Image.open("D:/descargas/proyectos-trabajo/nuevo/img/register.png")
        imagen_fondo_secundaria = imagen_fondo_secundaria.resize((1084, 700))
        self.foto_fondo_secundaria = ImageTk.PhotoImage(imagen_fondo_secundaria)

        # Mostrar la imagen de fondo en un Label
        label_fondo_secundaria = tk.Label(self, image=self.foto_fondo_secundaria)
        label_fondo_secundaria.place(x=0, y=0, relwidth=1, relheight=1)

        self.entry_usuario = tk.Entry(self, font=('Arial', 16))
        self.entry_usuario.pack()
        self.entry_usuario.place(x=410, y=200)

        self.entry_contrasena = tk.Entry(self, show="*", font=('Arial', 16))
        self.entry_contrasena.pack()
        self.entry_contrasena.place(x=410, y=310)

        self.entry_tipo = tk.StringVar()
        opciones_tipo = ["Admin", "Usuario"]
        self.combo_tipo = tk.OptionMenu(self, self.entry_tipo, *opciones_tipo)
        self.combo_tipo.config(font=('Arial', 16))
        self.combo_tipo.pack()
        self.combo_tipo.place(x=490, y=420)

        estilo_boton = {
            'font': ('Arial', 20, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 11,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }

        boton = tk.Button(self, text="Registrar", **estilo_boton, command=self.registrar)
        boton.place(x=440, y=500)
        
    def registrar(self):
        nuevo_usuario = self.entry_usuario.get()
        nueva_contrasena = self.entry_contrasena.get()
        tipo_usuario = self.entry_tipo.get()

        if tipo_usuario == "Admin":
            tipo_usuario = 1
        else:
            tipo_usuario = 2
        global usuario_actual  # Indicar que se usará la variable global en esta función
        usuario_actual = tipo_usuario 
        consulta = "INSERT INTO usuarios (usuario, contrase, tipo) VALUES (%s, %s, %s)"
        valores = (nuevo_usuario, nueva_contrasena, tipo_usuario)

        cursor.execute(consulta, valores)
        conn.commit()

        self.destroy()  # Cerrar la ventana de registro

        # Abre la ventana de administrador o usuario directamente
        if tipo_usuario == 1:
            self.abrir_ventana_admin()
        else:
            self.abrir_ventana_usuario()

    def abrir_ventana_admin(self):
        self.switch_frame(VentanaAdmin)
    
    def abrir_ventana_usuario(self):
        self.switch_frame(VentanaUsuario)

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self.master)  # Pasa 'self.master' como el argumento 'parent'
        nuevo_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.master._frame.destroy()  # Destruye el frame actual (RegistroApp)
        self.master._frame = nuevo_frame

class VentanaAdmin(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.crear_interfaz()

    def crear_interfaz(self):
        # Cargar la imagen de fondo de la ventana secundaria
        imagen_fondo_secundaria = Image.open("D:/descargas/proyectos-trabajo/nuevo/img/botons.png")
        imagen_fondo_secundaria = imagen_fondo_secundaria.resize((1084, 700))
        self.foto_fondo_secundaria = ImageTk.PhotoImage(imagen_fondo_secundaria)

        # Mostrar la imagen de fondo en un Label
        label_fondo_secundaria = tk.Label(self, image=self.foto_fondo_secundaria)
        label_fondo_secundaria.place(x=0, y=0, relwidth=1, relheight=1)

        estilo_boton1 = {
            'font': ('Arial', 20, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 16,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        estilo_boton2 = {
            'font': ('Arial', 20, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 11,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        boton = tk.Button(self, text="Ver Mantenimientos", **estilo_boton1,command=self.abrir_Mantenimiento)
        boton.place(x=380, y=250)

        boton = tk.Button(self, text="Ver Datos", **estilo_boton2,command=self.abrir_Datos)
        boton.place(x=420, y=340)

        boton = tk.Button(self, text="Usuarios", **estilo_boton2,command=self.abrir_usuarios)
        boton.place(x=420, y=430)

    def abrir_usuarios(self):
        self.switch_frame(VentanaUsers)
        
    def abrir_Mantenimiento(self):
        self.switch_frame(VentanaMantenimiento)

    def abrir_Datos(self):
        self.switch_frame(VentanaDatos)

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self.master) 
        nuevo_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self._frame = nuevo_frame

class VentanaUsuario(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.crear_interfaz()

    def crear_interfaz(self):
        # Cargar la imagen de fondo de la ventana secundaria
        imagen_fondo_secundaria = Image.open("D:/descargas/proyectos-trabajo/nuevo/img/botons.png")
        imagen_fondo_secundaria = imagen_fondo_secundaria.resize((1084, 700))
        self.foto_fondo_secundaria = ImageTk.PhotoImage(imagen_fondo_secundaria)

        # Mostrar la imagen de fondo en un Label
        label_fondo_secundaria = tk.Label(self, image=self.foto_fondo_secundaria)
        label_fondo_secundaria.place(x=0, y=0, relwidth=1, relheight=1)

        estilo_boton1 = {
            'font': ('Arial', 20, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 16,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        estilo_boton2 = {
            'font': ('Arial', 20, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 11,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        boton = tk.Button(self, text="Ver Mantenimientos", **estilo_boton1,command=self.abrir_Mantenimiento)
        boton.place(x=380, y=250)

        boton = tk.Button(self, text="Ver Datos", **estilo_boton2,command=self.abrir_Datos)
        boton.place(x=420, y=340)
        
    def abrir_Mantenimiento(self):
        self.switch_frame(VentanaMantenimiento)

    def abrir_Datos(self):
        self.switch_frame(VentanaDatos)

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self.master) 
        nuevo_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self._frame = nuevo_frame


class VentanaUsers(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.crear_interfaz()

    def crear_interfaz(self):
        global usuario_actual
        imagen_fondo_secundaria = Image.open("D:/descargas/proyectos-trabajo/nuevo/img/users.png")
        imagen_fondo_secundaria = imagen_fondo_secundaria.resize((1084, 700))
        self.foto_fondo_secundaria = ImageTk.PhotoImage(imagen_fondo_secundaria)

        label_fondo_secundaria = tk.Label(self, image=self.foto_fondo_secundaria)
        label_fondo_secundaria.place(x=0, y=0, relwidth=1, relheight=1)

        estilo_boton = {
            'font': ('Arial', 16, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 8,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        boton = tk.Button(self, text="Regresar", **estilo_boton, command=self.abrir_regresar)
        boton.place(x=50, y=50)
        

        # Consulta para obtener todos los usuarios excepto el actual
        cursor.execute('SELECT usuario, tipo FROM usuarios WHERE usuario != %s ORDER BY id ASC LIMIT 8', (usuario_actual,))
        usuarios = cursor.fetchall()

        y_position = 160  # Posición inicial vertical para las etiquetas y botones
        incrementos_y = [70, 68, 70, 70, 69, 68,70,140]  # Lista de incrementos personalizados

        


        for i, (usuario, tipo) in enumerate(usuarios):
            
            if tipo == 1:
                tipo_texto = "Administrador"
            elif tipo == 2:
                tipo_texto = "Usuario"
            else:
                tipo_texto = "Desconocido"
            estilo_label = {
                'font': ('Arial', 14),
                'bg': '#2b075f',  # O cualquier otro valor que desees para un fondo transparente
                'fg': 'white',  # Color del texto
            }
            estilo_boton = {
    'font': ('Arial', 10,'bold',),
    'fg': 'white',           # Color de las letras (blancas)
    'bg': '#2b075f',         # Color de fondo morado
    'width': 5,
    'height': 0,
    'relief': 'raised',      # Borde elevado
    'borderwidth': 2,
    'highlightbackground': 'white',
}
            label_usuario = tk.Label(self, text=f"Usuario: {usuario}", **estilo_label)
            label_usuario.place(x=350, y=y_position)

            label_usuario = tk.Label(self, text=f"Tipo: {tipo_texto}", **estilo_label)
            label_usuario.place(x=500, y=y_position)

            boton_borrar = tk.Button(self, text="Borrar",**estilo_boton, command=lambda user=usuario: self.borrar_usuario(user))
            boton_borrar.place(x=700, y=y_position)

            if i < len(incrementos_y):
                incremento_y = incrementos_y[i]
            else:
                incremento_y = 65  # Valor por defecto si se agotan los incrementos personalizados

            y_position += incremento_y

    def borrar_usuario(self, usuario):
    # Confirmar si el usuario realmente desea borrar el usuario
    
        try:
            # Realizar la lógica de eliminación del usuario de la base de datos
            cursor.execute('DELETE FROM usuarios WHERE usuario = %s', (usuario,))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario {usuario} ha sido borrado exitosamente.")
            
            # Actualizar la interfaz después de borrar el usuario
            self.actualizar_interfaz()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar el usuario: {str(e)}")

    def actualizar_interfaz(self):
        # Borra los widgets actuales en la ventana
        for widget in self.winfo_children():
            widget.destroy()

        # Crea de nuevo la interfaz con los usuarios actualizados
        self.crear_interfaz()

    def abrir_regresar(self):
        self.switch_frame(VentanaAdmin)

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self.master)
        nuevo_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self._frame = nuevo_frame

class VentanaDatos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.crear_interfaz()

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("broker_address", 1883, 60)

    def crear_interfaz(self):
        imagen_fondo_secundaria = Image.open("D:/descargas/proyectos-trabajo/nuevo/img/datos.png")
        imagen_fondo_secundaria = imagen_fondo_secundaria.resize((1084, 700))
        self.foto_fondo_secundaria = ImageTk.PhotoImage(imagen_fondo_secundaria)

        label_fondo_secundaria = tk.Label(self, image=self.foto_fondo_secundaria)
        label_fondo_secundaria.place(x=0, y=0, relwidth=1, relheight=1)

        estilo_boton = {
            'font': ('Arial', 16, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 8,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        boton_regresar = tk.Button(self, text="Regresar", **estilo_boton, command=self.abrir_regresar)
        boton_regresar.place(x=50, y=60)

        

        # Mostrar los datos iniciales de la tabla 'datos'
        self.mostrar_datos()

    def mostrar_datos(self, data):
        temperatura = data.get('temperatura', 'N/A')
        humedad = data.get('humedad', 'N/A')
        voltaje = data.get('voltaje', 'N/A')
        corriente = data.get('corriente', 'N/A')
        potencia = data.get('potencia', 'N/A')
        frecuencia = data.get('frecuencia', 'N/A')
        energia = data.get('energia', 'N/A')
        fecha_hora = data.get('fecha_hora', 'N/A')
    
    # Actualizar etiquetas con los nuevos valores
        self.label_temperatura.config(text=f"Temperatura: {temperatura} °C")
        self.label_humedad.config(text=f"Humedad: {humedad} %")
        self.label_voltaje.config(text=f"Voltaje: {voltaje} V")
        self.label_corriente.config(text=f"Corriente: {corriente} A")
        self.label_potencia.config(text=f"Potencia: {potencia} W")
        self.label_frecuencia.config(text=f"Frecuencia: {frecuencia} Hz")
        self.label_energia.config(text=f"Energía: {energia} kWh")
        self.label_fecha_hora.config(text=f"Fecha y Hora: {fecha_hora}")

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
    # Suscribirse a los temas MQTT donde el ESP32 publica los datos
        client.subscribe("sensor/dht11")
        client.subscribe("sensor/pzem004t")
        client.subscribe("sensor/rtc")

    def on_message(self, client, userdata, msg):
    # Cuando se recibe un mensaje en los temas MQTT, procesar los datos y actualizar la interfaz
        topic = msg.topic
        data = msg.payload.decode("utf-8")
        if topic == "sensor/dht11" or topic == "sensor/pzem004t" or topic == "sensor/rtc":
            self.mostrar_datos(data)



    def abrir_regresar(self):
        if usuario_actual is not None:
            cursor.execute('SELECT tipo FROM usuarios WHERE usuario = %s', (usuario_actual,))
            tipo_usuario = cursor.fetchone()[0]  # Obtener el tipo de usuario del resultado de la consulta

            if tipo_usuario == 1:
                self.switch_frame(VentanaAdmin)
            elif tipo_usuario == 2:
                self.switch_frame(VentanaUsuario)

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self.master)
        nuevo_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self._frame = nuevo_frame

class VentanaMantenimiento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.crear_interfaz()

    def crear_interfaz(self):
        imagen_fondo_secundaria = Image.open("D:/descargas/proyectos-trabajo/nuevo/img/manteni.png")
        imagen_fondo_secundaria = imagen_fondo_secundaria.resize((1084, 700))
        self.foto_fondo_secundaria = ImageTk.PhotoImage(imagen_fondo_secundaria)

        label_fondo_secundaria = tk.Label(self, image=self.foto_fondo_secundaria)
        label_fondo_secundaria.place(x=0, y=0, relwidth=1, relheight=1)

        estilo_boton = {
            'font': ('Arial', 14, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 8,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        estilo_boton2 = {
            'font': ('Arial', 14, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 15,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        boton_regresar = tk.Button(self, text="Regresar", **estilo_boton, command=self.abrir_regresar)
        boton_regresar.place(x=50, y=60)

        boton_actualizar = tk.Button(self, text="Actualizar", **estilo_boton, command=self.actualizar_datos)
        boton_actualizar.place(x=160, y=60)

        boton_regresar = tk.Button(self, text="+ Mantenimiento", **estilo_boton2, command=self.abrir_mantenimientoa)
        boton_regresar.place(x=800, y=60)

        # Mostrar los datos iniciales de la tabla 'mantenimiento'
        self.mostrar_datos()

    def mostrar_datos(self):
        # Realizar la consulta para obtener los datos de la tabla 'mantenimiento'
        cursor.execute('SELECT * FROM mantenimiento ORDER BY id DESC')
        datos = cursor.fetchall()

        # Mostrar los datos en etiquetas
        y_position = 160
        incrementos_y = [70, 68, 70, 70, 69, 68,70,140]
        for i,dato in enumerate(datos):
            estilo_label = {
                'font': ('Arial', 10),
                'bg': '#2b075f',  # O cualquier otro valor que desees para un fondo transparente
                'fg': 'white',  # Color del texto
            }
            id_mant, nombre, correo, telefono, tipo, costo, nivel, marca, area, riesgo, NS, equipo = dato
            label_dato = tk.Label(self,**estilo_label, text=f"{nombre} | {correo} |  {telefono} |  {tipo}  |  {costo} |  {nivel} | {marca} |  {area} |  {riesgo} |  {NS} |  {equipo}")
            label_dato.place(x=220, y=y_position)


            if i < len(incrementos_y):
                incremento_y = incrementos_y[i]
            else:
                incremento_y = 65  # Valor por defecto si se agotan los incrementos personalizados

            y_position += incremento_y

    def actualizar_datos(self):
        # Borra los widgets actuales en la ventana
        for widget in self.winfo_children():
            widget.destroy()

        # Recrea la interfaz desde cero
        self.crear_interfaz()

    def abrir_regresar(self):
        if usuario_actual is not None:
            cursor.execute('SELECT tipo FROM usuarios WHERE usuario = %s', (usuario_actual,))
            tipo_usuario = cursor.fetchone()[0]  # Obtener el tipo de usuario del resultado de la consulta

            if tipo_usuario == 1:
                self.switch_frame(VentanaAdmin)
            elif tipo_usuario == 2:
                self.switch_frame(VentanaUsuario)

    def abrir_mantenimientoa(self):
        self.switch_frame(RegistroMantenimiento)

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self.master)
        nuevo_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self._frame = nuevo_frame

class RegistroMantenimiento(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.crear_interfaz()

    def crear_interfaz(self):
        imagen_fondo_secundaria = Image.open("D:/descargas/proyectos-trabajo/nuevo/img/remante.png")
        imagen_fondo_secundaria = imagen_fondo_secundaria.resize((1084, 700))
        self.foto_fondo_secundaria = ImageTk.PhotoImage(imagen_fondo_secundaria)

        label_fondo_secundaria = tk.Label(self, image=self.foto_fondo_secundaria)
        label_fondo_secundaria.place(x=0, y=0, relwidth=1, relheight=1)
        estilo_boton = {
            'font': ('Arial', 14, 'bold'),  # Agregar 'bold' para hacer la letra en negrita
            'fg': '#272878',
            'bg': 'white',
            'width': 8,
            'height': 0,
            'relief': 'raised',
            'borderwidth': 2,
        }
        
        boton = tk.Button(self, text="Regresar", **estilo_boton, command=self.abrir_regresar)
        boton.place(x=50, y=50)

        estilo_label = {
            'font': ('Arial', 15),
            'fg': 'black',
            'bg': 'white',
            'width': 10,
            'height': 1,
            'relief': 'raised',
            'borderwidth': 2,
        }

        estilo_entry = {
            'font': ('Arial', 15),
            'width': 20,
        }

        label_nombre = tk.Label(self, text="Nombre:", **estilo_label)
        label_nombre.place(x=170, y=200)

        self.entry_nombre = tk.Entry(self, **estilo_entry)
        self.entry_nombre.place(x=290, y=200)

        label_correo = tk.Label(self, text="Correo:", **estilo_label)
        label_correo.place(x=170, y=250)

        self.entry_correo = tk.Entry(self, **estilo_entry)
        self.entry_correo.place(x=290, y=250)

        label_telefono = tk.Label(self, text="Teléfono:", **estilo_label)
        label_telefono.place(x=170, y=300)

        self.entry_telefono = tk.Entry(self, **estilo_entry)
        self.entry_telefono.place(x=290, y=300)

        label_tipo = tk.Label(self, text="Tipo:", **estilo_label)
        label_tipo.place(x=170, y=350)

        self.entry_tipo = tk.Entry(self, **estilo_entry)
        self.entry_tipo.place(x=290, y=350)

        label_costo = tk.Label(self, text="Costo:", **estilo_label)
        label_costo.place(x=170, y=400)

        self.entry_costo = tk.Entry(self, **estilo_entry)
        self.entry_costo.place(x=290, y=400)

        label_nivel = tk.Label(self, text="Nivel:", **estilo_label)
        label_nivel.place(x=550, y=200)

        self.entry_nivel = tk.Entry(self, **estilo_entry)
        self.entry_nivel.place(x=670, y=200)

        label_marca = tk.Label(self, text="Marca:", **estilo_label)
        label_marca.place(x=550, y=250)

        self.entry_marca = tk.Entry(self, **estilo_entry)
        self.entry_marca.place(x=670, y=250)

        label_area = tk.Label(self, text="Área:", **estilo_label)
        label_area.place(x=550, y=300)

        self.entry_area = tk.Entry(self, **estilo_entry)
        self.entry_area.place(x=670, y=300)

        label_riesgo = tk.Label(self, text="Riesgo:", **estilo_label)
        label_riesgo.place(x=550, y=350)

        self.entry_riesgo = tk.Entry(self, **estilo_entry)
        self.entry_riesgo.place(x=670, y=350)

        label_NS = tk.Label(self, text="NS:", **estilo_label)
        label_NS.place(x=550, y=400)

        self.entry_NS = tk.Entry(self, **estilo_entry)
        self.entry_NS.place(x=670, y=400)

        label_equipo = tk.Label(self, text="Equipo:", **estilo_label)
        label_equipo.place(x=390, y=450)

        self.entry_equipo = tk.Entry(self, **estilo_entry)
        self.entry_equipo.place(x=520, y=450)

        

        boton_registrar = tk.Button(self, text="Registrar", command=self.registrar, **estilo_boton)
        boton_registrar.place(x=480, y=530)

    def registrar(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        telefono = self.entry_telefono.get()
        tipo = self.entry_tipo.get()
        costo = self.entry_costo.get()
        nivel = self.entry_nivel.get()
        marca = self.entry_marca.get()
        area = self.entry_area.get()
        riesgo = self.entry_riesgo.get()
        NS = self.entry_NS.get()
        equipo = self.entry_equipo.get()

        # Realizar la inserción en la tabla 'mantenimiento'
        consulta = "INSERT INTO mantenimiento (nombre, correo, telefono, tipo, costo, nivel, marca, area, riesgo, NS, equipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (nombre, correo, telefono, tipo, costo, nivel, marca, area, riesgo, NS, equipo)

        try:
            cursor.execute(consulta, valores)
            conn.commit()
            messagebox.showinfo("Éxito", "Registro de mantenimiento exitoso.")
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el mantenimiento: {str(e)}")

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_costo.delete(0, tk.END)
        self.entry_nivel.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_area.delete(0, tk.END)
        self.entry_riesgo.delete(0, tk.END)
        self.entry_NS.delete(0, tk.END)
        self.entry_equipo.delete(0, tk.END)
    def abrir_regresar(self):
        self.switch_frame(VentanaAdmin)

    def switch_frame(self, frame_class):
        nuevo_frame = frame_class(self.master)
        nuevo_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self._frame = nuevo_frame

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
