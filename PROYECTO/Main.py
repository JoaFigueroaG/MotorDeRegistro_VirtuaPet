from cgitb import text
from operator import mod
from Connect import *
from tkinter import *
from tkinter import ttk

f = ("Times bold", 14)


#VENTANA
ventana= Tk()
ventana.geometry("700x500")
ventana.title("Gestion de Reserva")
ventana['bg'] = '#a5aae0'


marco = LabelFrame(ventana)
marco.place(x=50,y=50,width=600,height=400)
marco['bg'] = '#f1d7ff'

#Dentro del marco
db=DataBase()
modificar=False

id=StringVar()
nombre=StringVar()
apellido=StringVar()
sexo=StringVar()
nombrem=StringVar()
numero=StringVar()
raza=StringVar()

#Los lables con caja de texto

lblnombre=Label(marco, text="NOMBRE").grid(column=0,row=0,padx=5,pady=5),
txtnombre=Entry(marco, textvariable=nombre)
txtnombre.grid(column=1,row=0)

lblapellido=Label(marco, text="APELLIDO").grid(column=0,row=1,padx=5,pady=5)
txtapellido=Entry(marco, textvariable=apellido)
txtapellido.grid(column=1,row=1)

lblnombrem=Label(marco, text="NOMBRE MASCOTA").grid(column=3,row=0,padx=5,pady=5)
txtnombrem=Entry(marco, textvariable=nombrem)
txtnombrem.grid(column=4,row=0)

lblsexo=Label(marco, text="SEXO MASCOTA").grid(column=3,row=1,padx=5,pady=5)
txtsexo=ttk.Combobox(marco,values=["Masculino","Femenino"], textvariable=sexo)
txtsexo.grid(column=4,row=1)
txtsexo.current(0)

lblnumero=Label(marco, text="NUMERO").grid(column=0,row=2,padx=5,pady=5)
txtnumero=Entry(marco, textvariable=numero)
txtnumero.grid(column=1,row=2)

lblraza=Label(marco, text="ESPECIE").grid(column=3,row=2,padx=5,pady=5)
txtraza=ttk.Combobox(marco,values=["Perro","Gato","Hamster","Tortuga","Conejo","Otros"], textvariable=raza)
txtraza.grid(column=4,row=2)
txtraza.current(0)

lblMensaje=Label(marco,text="Texto en verde ᵃ",fg="green")
lblMensaje.grid(column=1,row=3,columnspan=4)

#CUADRADO CON LA BDD

tvagenda=ttk.Treeview(marco, selectmode=NONE)
tvagenda.grid(column=1,row=4,columnspan=4,padx=5)
tvagenda["columns"]=("id","Nombre","Apellido","Numero","Nombre_Mascota","Sexo_Mascota","Raza_Mascota")
tvagenda.column("#0",width=0,stretch=NO)
tvagenda.column("id",width=10,anchor=CENTER)
tvagenda.column("Nombre",width=80,anchor=CENTER)
tvagenda.column("Apellido",width=80,anchor=CENTER)
tvagenda.column("Numero",width=90,anchor=CENTER)
tvagenda.column("Nombre_Mascota",width=70,anchor=CENTER)
tvagenda.column("Sexo_Mascota",width=70,anchor=CENTER)
tvagenda.column("Raza_Mascota",width=90,anchor=CENTER)


tvagenda.heading("id",text="ID",anchor=CENTER)
tvagenda.heading("Nombre",text="Nombre",anchor=CENTER)
tvagenda.heading("Apellido",text="Apellido",anchor=CENTER)
tvagenda.heading("Numero",text="Numero",anchor=CENTER)
tvagenda.heading("Nombre_Mascota",text="Nombre_M",anchor=CENTER)
tvagenda.heading("Sexo_Mascota",text="Sexo_M",anchor=CENTER)
tvagenda.heading("Raza_Mascota",text="Raza_M",anchor=CENTER)




#Botones 


btnNuevo=Button(marco,text="GUARDAR", command=lambda:nuevo())
btnNuevo.grid(column=1,row=5)

btnActualizar=Button(marco,text="SELECCIONAR", command=lambda:actualizar())
btnActualizar.grid(column=3,row=5)

btnEliminar=Button(marco,text="ELIMINAR", command=lambda:eliminar())
btnEliminar.grid(column=4,row=5)



#funciones
def seleccionar(event):
    id= tvagenda.selection()[0]
    if int(id)>0:
        nombre.set(tvagenda.item(id,"values")[1])
        apellido.set(tvagenda.item(id,"values")[2])
        numero.set(tvagenda.item(id,"values")[3])
        nombrem.set(tvagenda.item(id,"values")[4])
        sexo.set(tvagenda.item(id,"values")[5])
        raza.set(tvagenda.item(id,"values")[6])
    

tvagenda.bind("<<TreeviewSelect>>",seleccionar)

def validar():
    return len(nombre.get())>0 and len(apellido.get())>0 and  len(numero.get())>0 and  len(nombrem.get())>0
        
def modificarF():
 global modificar
 modificar=False
 tvagenda.config(selectmode=NONE)
 btnNuevo.config(text="GUARDAR")
 btnActualizar.config(text="SELECCIONAR")
 btnEliminar.config(state=DISABLED)

def modificarT():
 global modificar
 modificar=True
 tvagenda.config(selectmode=BROWSE)
 btnNuevo.config(text="NUEVO")
 btnActualizar.config(text="ACTUALIZAR")
 btnEliminar.config(state=NORMAL)

def limpiar():
    nombre.set("")
    apellido.set("")
    numero.set("")
    nombrem.set("")
#eliminar fila por fila
def vaciatabla():
    filas= tvagenda.get_children()
    for fila in filas:
        tvagenda.delete(fila)
 
#llenar tabla fila por fila
def llenatabla():
    vaciatabla()
    sql="select * from agenda"
    db.cursor.execute(sql)
    filas= db.cursor.fetchall()
    for fila in filas:
        id= fila[0]
        tvagenda.insert("",END,id,text="id", values=fila)
def eliminar():
    id= tvagenda.selection()[0]
    if int(id)>0: 
        sql="delete from agenda where ID="+id
        db.cursor.execute(sql)
        db.connection.commit()
        tvagenda.delete(id)
        lblMensaje.config(text="se elimino el registro")
        limpiar()
    else:
        lblMensaje.config(text="no se a seleccionado un registro para eliminar")
def nuevo():
    if modificar==False:
    
     if validar():
       val=(nombre.get(),apellido.get(),numero.get(),nombrem.get(),sexo.get(),raza.get())
       sql="insert into agenda (Nombre,Apellido,Numero,Nombre_Mascota,Sexo_Mascota,Raza_Mascota) values (%s,%s,%s,%s,%s,%s)"
       db.cursor.execute(sql, val)
       db.connection.commit() 
       lblMensaje.config(text="Se Guardo El Registro Correctamente",fg="green")
       llenatabla()
       limpiar()
     else:
      lblMensaje.config(text="ERROR, LOS CAMPOS NO DEBEN ESTAR VACIOS",fg="red")
    else:
       modificarF()


def actualizar():

    if modificar==True:
    
     if validar():
       id=tvagenda.selection()[0]
       val=(nombre.get(),apellido.get(),numero.get(),nombrem.get(),sexo.get(),raza.get())
       sql="update agenda set Nombre=%s,Apellido=%s,Numero=%s,Nombre_Mascota=%s,Sexo_Mascota=%s,Raza_Mascota=%s where id="+id
       db.cursor.execute(sql, val)
       db.connection.commit() 
       lblMensaje.config(text="Se Actualizo El Registro Correctamente",fg="green")
       llenatabla()
       limpiar()
     else:
      lblMensaje.config(text="ERROR, LOS CAMPOS NO DEBEN ESTAR VACIOS",fg="red")
    else:
       modificarT()


def nextPage():
    ventana.destroy()
    import Menu

Button(
 ventana,

 text="ATRAS"
 , 
  
    font=f,
    command=nextPage
    ).pack(side=BOTTOM,padx=5,pady=5
    )       

llenatabla()
ventana.mainloop()