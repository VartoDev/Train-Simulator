from ursina import Ursina, Entity, color, Vec3, time
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import mouse, Animation, curve
from ursina import AmbientLight, DirectionalLight, held_keys, Audio, Text
from ursina.shaders import lit_with_shadows_shader
from ursina import clamp
from ursina import window, random, math
from ursina import camera, entity
from ursina.shader import Shader
from ursina.shaders.screenspace_shaders.pixelation_shader import pixelation_shader
from ursina.shaders.screenspace_shaders.camera_vertical_blur import camera_vertical_blur_shader
from ursina import raycast, sys
from ursina.shaders import lit_with_shadows_shader
from ursina import PointLight
from ursina import destroy, invoke 
from direct.interval.IntervalGlobal import LerpFunc

contrast_shader = Shader(
    name='screen_contrast',
    language=Shader.GLSL,
    vertex='''
#version 120
uniform mat4 p3d_ModelViewProjectionMatrix;
attribute vec4 p3d_Vertex;
attribute vec2 p3d_MultiTexCoord0;
varying vec2 uv;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    uv = p3d_MultiTexCoord0;
}
''',
    fragment='''
#version 120
uniform sampler2D tex;
uniform float contrast;
varying vec2 uv;

void main() {
    vec4 c = texture2D(tex, uv);
    vec3 rgb = (c.rgb - vec3(0.5)) * contrast + vec3(0.5);
    gl_FragColor = vec4(rgb, c.a);
}
'''
)


#App starten
Station_Life = Ursina()

window.render_resolution = (320, 180)
window.size = (1280, 720)

camera.shader = contrast_shader
camera.set_shader_input('contrast', 1.5)














#---------------------------------------------
#------------Sounds-------------------

Walking_Sound = Audio('Sounds_Zug/Walking.wav', loop=True, autoplay=False)
City_Sound = Audio('Music_Zug/City.mp3', loop=True, autoplay=False)
Power_Sound = Audio('Sounds_Zug/Electric.mp3', loop=True, autoplay=False)
Hum_Sound = Audio('Sounds_Zug/Hum.mp3', loop=True, autoplay=False)
Bullet = Audio('Sounds_Zug/Bullet.mp3', loop=False, autoplay=False)
Fast = Audio('Sounds_Zug/Fast.mp3', loop=False, autoplay=False)
Vending_Sound = Audio('Sounds_Zug/Vending.mp3', loop= False, autoplay= False)
Zug_verlässt = Audio('Sounds_Zug/Zug_leavt.mp3', loop=False, autoplay= True)
Zug_kommt =  Audio('Sounds_Zug/Zug_kommt.mp3', loop= False, autoplay= False)
Zug_kommt_acc =  Audio('Sounds_Zug/ICE.mp3', loop= False, autoplay= False)
Damper = Audio('Sounds_Zug/Damper.mp3', loop= False, autoplay= False)

City_Sound.play()
Power_Sound.play()
Hum_Sound.play()


#---------------------------------------------
#-----------Text-------------------

Text_pos = Text(text='Position: ', position=(0, 0), scale=1, color=color.white)
Text_für_Vending = Text(text='',position=(0, 0), scale=1.2, color=color.white, font= 'arial',  origin=(0, 0))

#---------------------------------------------

#---------------------------------------------
#-----------Licht-------------------

#sun = DirectionalLight() 
#sun.look_at(Vec3(1, -1, 1)) 

#sun2 = DirectionalLight() 
#sun2.look_at(Vec3(1, -1, 1)) 

#sun4 = DirectionalLight() 
#sun4.look_at(Vec3(-7, -1, 1)) 

#sun3 = DirectionalLight() 
#sun3.look_at(Vec3(1, -1, -1))


lamp = PointLight()
lamp.position = Vec3(-3, 3, -5)
lamp.color = color.rgb(255, 180, 100)

amp = PointLight()
amp.position = Vec3(-3, 3, -5)
amp.color = color.rgb(255, 180, 100)








Zug_licht = PointLight()
Zug_licht.color = color.rgb(125, 75, 33)


Zug_licht2 = PointLight()
Zug_licht2.color = color.rgb(100, 75, 33)

Zug_licht3 = PointLight()
Zug_licht3.color = color.rgb(255, 180, 100)


#---------------------------------------------
def input(key):
    if key == 't' :
        player.position = Vec3(player.position.x, player.position.y+1, player.position.z)
        player.color = color.green
        window.render_mode = 'wireframe'

        Shinkansen.wireframe = False
        

    if key == 'r' :
        window.render_mode = 'default'
        


    if key == 'escape':
        sys.exit()

    if key == 'e' and Vending_Interact == True:
       print("Hallo")
    
    if key == 'e' and Die_fahrt_kann_beginnen:
       global Die_Fahrt_hat_begonnen
       black_out()
       invoke(black_weg, delay=9)
       
       Text_für_Vending.text = ""
       Die_Fahrt_hat_begonnen = True
       
       invoke(Zug_Spawn, delay=8)
       invoke(fahrt_beginn, delay=8)
       Zug3.position = Vec3(10000,1111, 6767)
       
      
#---------------------------------------------
#-----------First Person Controller-------------------
#First Person Controller erstellen
player = FirstPersonController(model='cube', color=color.orange, scale=0.03, position=Vec3(0, 0, 0))
player.position = Vec3(3, 1.8, -10)
#----------------------------------------------
#-----------Texturen----------------


black_screen = Entity(
    parent=camera.ui,
    model='quad',
    texture='Photos_Zug/Schwarz.jpeg',
    scale=2,
    color=color.rgba(0, 0, 0, 0)
)





#---------------------------------------------
#------------Variablen-------------------
mouse.locked = False
player.cursor.visible = False
Train_Passing = False
Die_fahrt_kann_beginnen = False
sound_played = False
animation_gestartet = False
Train_can_drive = False
sound_played_for_train_coming = False
Vending_Interact = False
sound_played_for_vending = False
animation_gestartet_for_other_train = False
Main_Zug_kann_kommen = False
animation_gestartet_for_main_train = False
Die_Fahrt_hat_begonnen = False
       
In_bahnhof = True
Dove_Interact = False
Im_Zug = False
current_mouse_x = mouse.position.x
current_mouse_y = mouse.position.y
player.gravity = 0
player.speed = 2.8
sensitivity = 150
City_Sound.volume = 1
Walking_Sound.volume = 1000
sekunde = 0
Power_Sound.volume = 0.3
Hum_Sound.volume = 0.3
is_walking = False
breathing = math.sin(sekunde * 2) * 0.5
#---------------------------------------------

#---------------------------------------------
#-----------Models-------------------


Bahnhof = Entity(model='Models_Zug/abandoned_underground_train_station.glb', scale=1, position=Vec3(0, 0, 0), collider='', shader=lit_with_shadows_shader )
Zug = Entity(model='Models_Zug/Zug.glb', scale=1, position=Vec3(-7, 1.2, -0.02), collider='cube', rotation= Vec3(0, 270, 0), shader=lit_with_shadows_shader)

Zug3 = Entity(model='Models_Zug/Zug.glb', scale=1, position=Vec3(-200, 1.2, -6), collider='cube', rotation= Vec3(0, 270, 0), shader=None)

Shinkansen = Entity(model='Models_Zug/bullet_train.glb', scale=0.67, position=Vec3(-100, 0.045, -6.2), collider='cube', rotation=Vec3(0, 180, 0), render_mode = 'filled', shader=lit_with_shadows_shader)
Tree = Entity(model='Models_Zug/stylized_tree.glb', scale=10, position=Vec3(4, 0.3, -3.7),  rotation=Vec3(0, 0, 0), collider='', shader=lit_with_shadows_shader)
Tree2 = Entity(model='Models_Zug/Shelter.glb', scale=1, position=Vec3(8, 0.3, -3),  rotation=Vec3(0, 90, 0), shadows= True)
Tree3 = Entity(model='Models_Zug/stylized_tree.glb', scale=10, position=Vec3(-3, 0.3, -3.7),  rotation=Vec3(0, 0, 0),shadows= True)
Tree4 = Entity(model='Models_Zug/stylized_tree.glb', scale=10, position=Vec3(-3, 0.3, -9),  rotation=Vec3(0, 0, 0), shadows= True)
Tree5 = Entity(model='Models_Zug/stylized_tree.glb', scale=10, position=Vec3(-3, 0.3, 3.32),  rotation=Vec3(0, 0, 0),shadows= True )
Tree6 = Entity(model='Models_Zug/stylized_tree.glb', scale=10, position=Vec3(12, 0.3, 3.32),  rotation=Vec3(0, 0, 0),shadows= True )
Tree6 = Entity(model='Models_Zug/stylized_tree.glb', scale=10, position=Vec3(4, 0.3, 3.32),  rotation=Vec3(0, 0, 0),shadows= True )
Tree7 = Entity(model='Models_Zug/stylized_tree.glb', scale=6, position=Vec3(-13, 4.2, -6),  rotation=Vec3(0, 0, 0), shadows= True )



Vending = Entity(model='Models_Zug/minecraft_vending_machine.glb', scale=1, position=Vec3(-2.8, 0.47, -12),  rotation=Vec3(0, -180, 0),  collider='mesh', shader=lit_with_shadows_shader)
latern1 = Entity(model='Models_Zug/lamp.glb', scale=100000, position=Vec3(0, 0.3, -7.3),  rotation=Vec3(90, 90, 0),  collider='')
depature = Entity(model='Models_Zug/airport_departure_sign.glb', scale=1, position=Vec3(-12.2, 2.89, -6.2),  rotation=Vec3(0, 0, 0), shader=lit_with_shadows_shader)
depature2 = Entity(model='Models_Zug/airport_departure_sign.glb', scale=1, position=Vec3(-12.2, 2.89, 0.8),  rotation=Vec3(0, 0, 0), shader=lit_with_shadows_shader)
dove = Entity(model='Models_Zug/dove_poster.glb', scale=0.025, position=Vec3(-1.7, 1.7, -15.2),  rotation=Vec3(0, 0, 0), shader=lit_with_shadows_shader)

#Pink_Tree = Entity(model='Models_Zug/Birch_Tree.glb', scale=10, position=Vec3(-2, 0.47, -12),  rotation=Vec3(0, -180, 0))



#------------Definitionen--------------


def Zug_Spawn():
   Zug2 = Entity(model='Models_Zug/vr_train_wagon.glb', 
    scale=1, position=Vec3(1, -1, -6), collider='cube', rotation= Vec3(0, 270, 0))


   return Zug_Spawn

def fahrt_beginn():
   global Im_Zug
   global In_bahnhof
   player.position = Vec3(4.1 , 2.5 , -6.5)
   lamp5 = PointLight()
   lamp5.position = Vec3(player.x, player.y, player.z)
   lamp5.color = color.rgb(255, 180, 100)

   lamp6 = PointLight()
   lamp6.position = Vec3(player.x, player.y, player.z)
   lamp6.color = color.rgb(255, 180, 100)

   lamp7 = PointLight()
   lamp7.position = Vec3(player.x, player.y, player.z)
   lamp7.color = color.rgb(255, 180, 100)

   lamp = PointLight()
   lamp.position = Vec3(1000, 3, -5)
   lamp.color = color.rgb(255, 180, 100)

   amp = PointLight()
   amp.position = Vec3(1000, 3, -5)
   amp.color = color.rgb(255, 180, 100)
   

   Im_Zug = True
   In_bahnhof = False
   player.speed = 1
   City_Sound.volume = 0.1
   
def black_out():
   def fade_in(alpha):
      black_screen.color = color.rgb(0, 0, 0, alpha)


   fade_in_intervall = LerpFunc(
      fade_in,
      fromData=0, 
      toData=1, 
      duration=5
   )

   fade_in_intervall.start()


def black_weg():
   def fade_out(alpha):
       black_screen.color = color.rgb(0, 0, 0, alpha)

   fade_in_intervall = LerpFunc(
         fade_out,
         fromData=1, 
         toData=0, 
         duration=5
      )
   
   fade_in_intervall.start()
      
      

#---------------------------------------------

def update():
    global is_walking
    global sekunde
    global Train_Passing
    global sound_played
    global animation_gestartet
    global sensitivity
    global current_mouse_x
    global current_mouse_y
    global camera
    global In_bahnhof
    global breathing
    global Im_Zug 
    global Vending_Interact
    global Dove_Interact
    global sound_played_for_vending
    global Train_can_drive
    global animation_gestartet_for_other_train
    global Main_Zug_kann_kommen 
    global animation_gestartet_for_main_train
    global sound_played_for_train_coming
    global Die_fahrt_kann_beginnen
    global Die_Fahrt_hat_begonnen
    #---------------------------------------------
    #------------Mouse-Look-------------------
    
    last_mouse_x = current_mouse_x
    last_mouse_y = current_mouse_y

    current_mouse_x = mouse.position.x
    current_mouse_y = mouse.position.y

    delta_x = current_mouse_x - last_mouse_x
    delta_y = current_mouse_y - last_mouse_y

    player.rotation_y += delta_x * sensitivity
    player.rotation_x -= delta_y * sensitivity

    player.rotation_x = clamp(
        player.rotation_x,
        -90,
        90
    )




    #----------------------------------------------



    #------------Gravitation_bzw._Mag-Begrenzung-------------

    if In_bahnhof == True and player.position.y < 1.8:
        player.position = Vec3(player.position.x, 1.8, player.position.z)


    if In_bahnhof == True and player.position.y > 1.8:
        player.set_position(Vec3(player.position.x, 1.8, player.position.z))

    if In_bahnhof == True and player.position.z > -7.3:
       player.position = Vec3(player.position.x, player.position.y , -7.3)

    if Im_Zug == True and player.position.y > 2.47:
        player.set_position(Vec3(player.position.x, 2.47, player.position.z))
       
    if Im_Zug == True and player.position.y < 2.47:
            player.set_position(Vec3(player.position.x, 2.47, player.position.z))
     
    #---------------------------------------------------------

    #---------------------------------------------------------
    #----------Gameplay----------------
    if is_walking == True:
      sens = 1.2
      rotation_rest = False
    else:
      sens = 0.5
      rotation_rest = True
    breathing = math.sin(sekunde * 2) * sens
    player.camera_pivot.rotation_x = breathing


    #if rotation_rest == True:
      #player.camera_pivot.rotation_y = breathing
      #player.camera_pivot.rotation_z = breathing
    #---------------------------------------------------------

    #---------------------------------------------------------
    #----------Hitbox----------------

    hit = raycast(
    camera.world_position,
    camera.forward,
    distance=3,
    ignore=[player]
    )

    if hit.hit and hit.entity == Vending:
      Text_für_Vending.text = "Press [E] to interact"
      Vending_Interact = True
    else:
       Text_für_Vending.text = ""
       Vending_Interact = False
      #Du kannst den Vending benutzen

    if Vending_Interact == True and sound_played_for_vending == False:
       sound_played_for_vending = True
       Vending_Sound.play()
       
    elif Vending_Interact == False and sound_played_for_vending == True:
       sound_played_for_vending = False
    
       
       
    hitZug = raycast(
        camera.world_position,
        camera.forward,
        distance=3,
        ignore=[player]
        )

    
    if hitZug.hit and hit.entity == dove:
       Text_für_Vending.text = "YOU: Beautiful..."
    






    #---------------------------------------------------------
    
    



    #---------------------------------------------------------
    #-----------Updates-------------------------

    pos = Vec3(player.position.x, player.position.y, player.position.z)

    #mouse.x = 0
    #mouse.y = 0

    #mouse.position = (mouse.x, mouse.y)
    

    
    Text_pos.text = f'Position: {pos}'
    sekunde += time.dt
    print(sekunde)


    Zug_licht.position = Zug3.position + Vec3(30, 4, -5)

    Zug_licht2.position = Zug3.position + Vec3(20, 4, -5)

    Zug_licht3.position = Zug3.position + Vec3(0, 4, -5)

    
    moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']

    if moving and not is_walking:
        Walking_Sound.play()
        is_walking = True
    elif not moving and is_walking:
        Walking_Sound.stop(destroy=False)
        is_walking = False
    
       
    #---------------------------------------------------------
    #---------------------------------------------------------
    #-----------Zug_Events---------------------
    # use >= for float accumulation (exact equality rarely matches)
    if sekunde >= 5:
        Train_Passing = True

    if sekunde >= 6 and sound_played == False:
        Bullet.play()
        sound_played = True
              
              
        Fast.play()


    if Train_Passing == True and not animation_gestartet:
      Shinkansen.animate('position', Vec3(460, 0.045, -6.2), duration=10, curve=curve.linear)
      animation_gestartet = True


    if sekunde >=30:
       Train_can_drive = True
    if sekunde == 15:
        Damper.play()
       

    if Train_can_drive and not animation_gestartet_for_other_train:
       animation_gestartet_for_other_train = True
       Zug.animate('x', -100, duration=25, curve=curve.in_expo)

    if sekunde >=53:
       Zug_verlässt.volume = 0.8
    if sekunde >=53.5:
        Zug_verlässt.volume = 0.7
    if sekunde >=54:
        Zug_verlässt.volume = 0.5
    if sekunde >=54.5:
        Zug_verlässt.volume = 0.38
           
    #------------------------------------------------------
    #-------------------Main-Zug-Events------------     


    if sekunde >=40:
       Main_Zug_kann_kommen = True

    if sekunde >= 43 and not sound_played_for_train_coming:
       sound_played_for_train_coming = True
       Zug_kommt.play()
       Zug_kommt_acc.play()
       Zug_kommt_acc.volume = 100
       
       
    if Main_Zug_kann_kommen == True and animation_gestartet_for_main_train == False:
       animation_gestartet_for_main_train = True
       Zug3.animate('x', -4, duration=35, curve=curve.out_expo)

     
    if sekunde >=1 and Die_Fahrt_hat_begonnen == False:
    

       Text_für_Vending.text = "Press [E] to start your ride"
       Die_fahrt_kann_beginnen = True
      
      


    #--Zug einsteigen--I

    
    


    #--Zug einsteigen--I
    #--------------------------------------------------





    #---------------------------------------------------------   




Station_Life.run()