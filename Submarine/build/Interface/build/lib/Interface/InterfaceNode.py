#!/usr/bin/env python3

import rclpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from rclpy.node import Node
from cv_bridge import CvBridge
import cv2
import tkinter as tk
import numpy as np
from pynput import keyboard








class Publicador(Node):

    def __init__(self):
        super().__init__('robot_teleop')
        self.publisher_ = self.create_publisher(Twist, 'robot_cmdVel', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.movement = Twist()
        self.presionado=False
        self.bridge=CvBridge()
        # Create a subscription for camera data
        self.camera_subscription = self.create_subscription(
            Image, 'camera_topic', self.camera_callback, 10)

        #por defecto la velocidades son 1 
        self.angular_value = 1.0
        self.linear_value = 1.0

        # Crear ventana de tkinter para la interfaz de movimiento
        self.root = tk.Tk()
        self.root.title("Submarine Interface")
        self.root.geometry("1000x600") 
        #mportar imagen de fondo
        #ruta_imagen = os.path.abspath("imagen_de_fondo.jpg")
        #image = Image.open(ruta_imagen)
        #image = image.resize((600, 600), Image.ANTIALIAS) # Redimensionar la imagen
        #bg_image = ImageTk.PhotoImage(image)
        # Crear un Label con la imagen de fondo
        #bg_label = tk.Label(self.root, image=bg_image)
        #bg_label.place(x=0, y=0, relwidth=1, relheight=1)

       

        # ... (inicio del código se mantiene igual)

        # Crear marcos para los botones de movimiento y establecer la imagen de fondo
        self.defaultbg = self.root.cget('bg')
        movement_frame = tk.Frame(self.root, bg=self.defaultbg, width=100, height=130, borderwidth=0, relief="groove")
        movement_frame.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=10)
        movement_frame.grid_propagate(False)
        movement_frame.grid_columnconfigure(0, weight=1)
        movement_frame.grid_columnconfigure(1, weight=1)
        movement_frame.grid_columnconfigure(2, weight=1)
        movement_frame.grid_rowconfigure(0, weight=1)
        movement_frame.grid_rowconfigure(1, weight=1)
        movement_frame.grid_rowconfigure(2, weight=1)
        movement_frame.grid_propagate(False)

        # ... (resto del código)



        #bg_label = tk.Label(movement_frame, image=bg_image)
        #bg_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        #crear camras 
        self.camera_frame = tk.Frame(self.root, bg=self.defaultbg, width=300, height=300, bd=2, relief="raised")
        self.camera_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.camera_frame.grid_columnconfigure(0, weight=100)
        self.camera_frame.grid_columnconfigure(1, weight=100)
        self.camera_frame.grid_columnconfigure(2, weight=100)
        self.camera_frame.grid_rowconfigure(0, weight=300)
        self.camera1 = tk.Label(self.camera_frame, text="Cámara 1", bg='grey')
        self.camera1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        # Inicializar captura de video
        self.cap = cv2.VideoCapture(0)
        self.update_camera_feed(self.camera1)
        #
        self.camera2 = tk.Label(self.camera_frame, text="Cámara 2", bg='grey')
        self.camera2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.cv2_image = None
        self.camera3 = tk.Label(self.camera_frame, text="Cámara 3", bg='grey')
        self.camera3.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

       





        # Crear botones de movimiento y hacerlos transparentes
        
        self.w_button = tk.Button(movement_frame, text="W", width=1, height=1, command=lambda:self.forward(self,self.w_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.a_button = tk.Button(movement_frame, text="A", width=1, height=1, command=lambda:self.left(self,self.a_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.s_button = tk.Button(movement_frame, text="S", width=1, height=1, command=lambda:self.backward(self,self.s_button), highlightthickness=0,bg='#191970', fg='white', font=('Arial', 16))
        self.d_button = tk.Button(movement_frame, text="D", width=1, height=1, command=lambda:self.right(self,self.d_button), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.q_button = tk.Button(movement_frame, text="Q", width=1, height=1, command=lambda:self.up_left(), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.e_button = tk.Button(movement_frame, text="E", width=1, height=1, command=lambda:self.up_right(), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))
        self.z_button = tk.Button(movement_frame, text="Z", width=1, height=1, command=lambda:self.down_left(), highlightthickness=0,bg='#191970', fg='white', font=('Arial', 16))
        self.c_button = tk.Button(movement_frame, text="C", width=1, height=1, command=lambda:self.down_right(), highlightthickness=0, bg='#191970', fg='white', font=('Arial', 16))

        # ... (El resto de tu código se mantiene igual)

        self.q_button.grid(row=2, column=0, padx=0, pady=0)
        self.e_button.grid(row=2, column=2, padx=0, pady=0)
        self.z_button.grid(row=4, column=0, padx=0, pady=0)
        self.c_button.grid(row=4, column=2, padx=0, pady=0)

        self.w_button.grid(row=2, column=1, padx=0, pady=0)
        self.a_button.grid(row=3, column=0, padx=0, pady=0)
        self.s_button.grid(row=3, column=1, padx=0, pady=0)
        self.d_button.grid(row=3, column=2, padx=0, pady=0)

        # ... (El resto de tu código se mantiene igual)

                             


        # Asociar teclas del teclado con los botones de movimiento

        self.root.bind('<KeyRelease-w>', lambda event: self.w_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-a>', lambda event: self.a_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-s>', lambda event: self.s_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-d>', lambda event: self.d_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-q>', lambda event: self.q_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-e>', lambda event: self.e_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-z>', lambda event: self.z_button.config(relief=tk.RAISED))
        self.root.bind('<KeyRelease-c>', lambda event: self.c_button.config(relief=tk.RAISED))


        # Iniciar listener de teclado
        self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.key_listener.start()
        self.root.mainloop()

        
    def forward(self):
        button=self.w_button
        self.movement.linear.x = self.linear_value
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')
    def camera_callback(self, msg):
        try:
            # Convert the ROS2 Image message to OpenCV format
            cv2_image = self.bridge.imgmsg_to_cv2(msg)

            if cv2_image is not None:
                self.cv2_image = cv2_image

            # Display the image in your tkinter interface
            if self.cv2_image is not None:
                img = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.config(image=imgtk)

        except Exception as e:
            self.get_logger().error(f"Error processing camera data: {e}")

    def backward(self):
        button=self.s_button
        self.movement.linear.x = -(self.linear_value)
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def left(self):
        button=self.a_button
        self.movement.linear.y = self.linear_value
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')

    def right(self):
        button=self.d_button
        self.movement.linear.y =  -self.linear_value
        self.publisher_.publish(self.movement)
        button.configure(bg='#FFA500')
    def unforward(self):
        button=self.w_button
        self.movement.linear.x = 0.0
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def unbackward(self):
        button=self.s_button
        self.movement.linear.x = 0.0
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def unleft(self):
        button=self.a_button
        self.movement.linear.y  = 0.0
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')

    def unright(self):
        button=self.d_button
        self.movement.linear.y  = 0.0
        self.publisher_.publish(self.movement)
        button.configure(bg='#191970')
    def up_left(self):
        self.movement.linear.x = self.linear_value
        self.movement.linear.y = self.linear_value
        self.publisher_.publish(self.movement)
        self.q_button.configure(bg='#FFA500')

    def up_right(self):
        self.movement.linear.x = self.linear_value
        self.movement.linear.y = -self.linear_value
        self.publisher_.publish(self.movement)
        self.e_button.configure(bg='#FFA500')

    def down_left(self):
        self.movement.linear.x = -self.linear_value
        self.movement.linear.y = self.linear_value
        self.publisher_.publish(self.movement)
        self.z_button.configure(bg='#FFA500')

    def down_right(self):
        self.movement.linear.x = -self.linear_value
        self.movement.linear.y = -self.linear_value
        self.publisher_.publish(self.movement)
        self.c_button.configure(bg='#FFA500')



    def custom_cmd(self, cmd):
        self.get_logger().info('Custom command received: "%s"' % cmd)
        # Aquí puedes implementar lo que quieras que haga el robot cuando reciba un comando personalizado

    def on_press(self, key):

        try:
            # Mapear teclas de flechas a comandos de movimiento
            if key.char == 'w' and (not self.presionado):
                self.presionado=True
                self.forward()
            if key.char == 's'and (not self.presionado):
                self.presionado=True
                self.backward()

            if key.char == 'a'and (not self.presionado):
                self.presionado=True
                self.left()
            if key.char == 'd'and (not self.presionado):
                self.presionado=True
                self.right()

            if key.char == 'q' and (not self.presionado):
                self.presionado=True
                self.up_left()
            if key.char == 'e' and (not self.presionado):
                self.presionado=True
                self.up_right()
            if key.char == 'z' and (not self.presionado):
                self.presionado=True
                self.down_left()
            if key.char == 'c' and (not self.presionado):
                self.presionado=True
                self.down_right()
            else:
                # Si se presiona cualquier otra tecla, tomar el comando personalizado de la entrada de texto
                cmd = self.custom_cmd_entry.get()
                self.custom_cmd(cmd)
        except AttributeError:
            # Ignorar teclas de modificación (Shift, Ctrl, Alt, etc.)
            pass

    def on_release(self, key):
        # Detener el movimiento al soltar cualquier tecla de movimiento
        try:
            if key.char == 'w'and (self.presionado):
                self.presionado=False
                self.unforward()
            if key.char == 's'and (self.presionado):
                self.presionado=False
                self.unbackward()
            if key.char == 'a'and ( self.presionado):
                self.presionado=False
                self.unleft()
            if key.char == 'd'and ( self.presionado):
                self.presionado=False
                self.unright()
            if key.char == 'q' and (self.presionado):
                self.presionado=False
                self.q_button.configure(bg='#191970')
            if key.char == 'e' and (self.presionado):
                self.presionado=False
                self.e_button.configure(bg='#191970')
            if key.char == 'z' and (self.presionado):
                self.presionado=False
                self.z_button.configure(bg='#191970')
            if key.char == 'c' and (self.presionado):
                self.presionado=False
                self.c_button.configure(bg='#191970')
        except AttributeError:
            # Ignorar teclas de modificación (Shift, Ctrl, Alt, etc.)
            pass

    def timer_callback(self):
        print(self.linear_speed_entry)
        print(self.angular_speed_entry)
        self.i += 1
    def update_camera_feed(self, camera_label):
        # Capturar el siguiente frame de video
        ret, frame = self.cap.read()

        if ret:
            # Redimensionar el frame a 100x300
            frame = cv2.resize(frame, (500, 400))

            # Convertir el frame de cv2 (BGR) a RGB para usar con tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convertir la imagen de cv2 a una imagen de PIL para mostrarla en tkinter
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # Actualizar el label con la nueva imagen
            camera_label.imgtk = imgtk
            camera_label.config(image=imgtk)

            # Llamar a esta función nuevamente para obtener el siguiente frame
            self.root.after(10, lambda: self.update_camera_feed(camera_label))

        

        


    def destroy(self):
            self.cap.release()  # Liberar la cámara
            super().destroy()


def main(args=None):
    rclpy.init(args=args)     
    publicador = Publicador()

    rclpy.spin(publicador)

    publicador.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
    print("¡El programa se ha ejecutado correctamente!")