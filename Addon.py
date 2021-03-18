import bpy
from bpy.app.handlers import persistent
from datetime import datetime as dtm
import aud

bl_info = {
    "name" : "render time estimator & alarm",
    "author" : "u/JoJoJoel2007",
    "description" : "This estimates the time a whole animation render takes, and plays a sound when a frame is done",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "category" : "Render"
}

addons = bpy.context.preferences.addons#C:/Users/joelk/Desktop/Sound.wav
@persistent
def my_handler(scene):#gets called when a frame render ends
    if addons[__name__].preferences.sound:#if the box is checked then play the sound
        sound()#play the sound
    Render_Start = dtm.strptime(bpy.types.Scene.Start, "%H:%M:%S.%f")#get when the render started
    now = dtm.strptime(dtm.now().strftime("%H:%M:%S.%f"), "%H:%M:%S.%f")#get the time
    start, current, end = bpy.data.scenes[0].frame_start, bpy.data.scenes[0].frame_current, bpy.data.scenes[0].frame_end
    if (current == start):
        print("frames done:", current-start, "\nframes remaining:", (end - current), "\naverage time per frame", (now - Render_Start), "\ntime remaining:", (now - Render_Start) * (end - current))
    else:
        print("frames done:", current-start, "\nframes remaining:", (end - current), "\naverage time per frame", (now - Render_Start), "\ntime remaining:", ((now - Render_Start)/(current-start)) * (end - current))

@persistent
def start_handler(scene):#gets called when a render starts
    bpy.types.Scene.Start = bpy.props.StringProperty(name='Render_Start')#set a hidden property to the scene as temp data
    bpy.types.Scene.Start = dtm.now().strftime("%H:%M:%S.%f")#set the property as the current date

@persistent
def complete_handler(scene):#when the animation is done
    if addons[__name__].preferences.Anim_Sound:#if the box is checked then play the sound
        if not addons[__name__].preferences.sound:#if the box is checked then play the sound
            sound()#play the sound

def sound():#play the sound
    device = aud.Device()#load the sound device
    sound = aud.Sound.file(addons[__name__].preferences.SoundFile)#load the sound file
    handle = device.play(sound)#play the sound

class Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__#name
    sound : bpy.props.BoolProperty(name="Sound", description="play a sound when a frame is done")#play a sound when a frame is done
    Anim_Sound : bpy.props.BoolProperty(name="Anim_Sound", description="play a sound when the whole render is done")#play a sound when the animation is done
    SoundFile : bpy.props.StringProperty(name="SoundFile", description="the sound this addon will play, please write the path with / and not \\")#the file to play
    def draw(self, context):#ui
        row = self.layout.row()#make a row
        row.prop(self, "sound")#play a sound when a frame is done
        row.prop(self, "Anim_Sound")#play a sound when the animation is done
        self.layout.prop(self, "SoundFile")#the file to play

def register():#set the handlers when the addon is added
    bpy.app.handlers.render_post.append(my_handler)#add the frame render handler
    bpy.app.handlers.render_complete.append(complete_handler)#add the animation render handler
    bpy.app.handlers.render_init.append(start_handler)#add the start render handler
    bpy.utils.register_class(Preferences)#add the preferences

def unregister():#remove the handlers when the addon is removed
    bpy.app.handlers.render_post.remove(my_handler)#remove the frame render handler
    bpy.app.handlers.render_complete.remove(complete_handler)#remove the animation render handler
    bpy.app.handlers.render_init.remove(start_handler)#remove the start render handler
    bpy.utils.unregister_class(Preferences)#remove the preferences