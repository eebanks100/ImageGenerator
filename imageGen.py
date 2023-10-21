import bpy
import sys
import os
import random
from math import radians
import time  # doby debug
#import logging as logger

# Elisha - Render using GPU (really slow and output doesnt come out correctly)
# bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
# bpy.context.user_preferences.addons['cycles'].preferences.devices[0].use = True
# bpy.context.user_preferences.addons['cycles'].preferences.feature_set = 'EXPERIMENTAL'
# bpy.context.scene.cycles.device = 'GPU'
# bpy.context.scene.render.engine = 'CYCLES'
# bpy.context.scene.render.tile_x = 150
# bpy.context.scene.render.tile_y = 150
# bpy.context.scene.render.use_simplify = True

# Specify paths and files
path = os.getcwd() # Get the current working directory
infilepath = path + "/foregroundObjects/"
outfilepath = path + "/outputFiles/outputBGpos/"
outfilepathc = path + "/outputFiles/outputGTpos/" # give each output their own folder
outfilepathn = path + "/outputFiles/outputBGneg/"
outfilepathcn = path + "/outputFiles/outputGTneg/"
logpath = path + "/imglog/"             # doby for logging the data of the imgs gen for future recreation of contoured versions to train ai
contDir = path + "/planeImages/contRE"              # set directory to contour images
blackbg = contDir + "/black.jpg"
whitebg = contDir + "/white.jpg"
objs = bpy.data.objects

# Elisha - all the user input from GUI
argv = sys.argv 
argv = argv[argv.index("--") + 1:]      # Elisha - command-line arguments list, '--' as separator to separate command-line arguments
totalRuns = int(argv[0])
renderRes_x = int(argv[1])
renderRes_y = int(argv[2])
posBGimgs = bool(argv[3] == 'True')
posGTimgs = bool(argv[4] == 'True')
negBGimgs = bool(argv[5] == 'True')
negGTimgs = bool(argv[6] == 'True')
randomScale = bool(argv[7] == 'True')
tiltImage = bool(argv[8] == 'True')
randomMosaic = bool(argv[9] == 'True')
brightnessVariation = bool(argv[10] == 'True')
blurVariation = bool(argv[11] == 'True')

blenderLocation = r'".\blender-2.79-windows64\blender.exe"'
blenderScript = r'./imageGen.py'


#################################################################################################################################################################

# Elisha - run the image generator based on the number of images the user input from GUI
imgBatch = 20
for i in range(totalRuns):
# Elisha - clear meshes/objects after a batch of images have been generated: https://blender.stackexchange.com/questions/102025/how-to-prevent-memory-leakage-in-blender
    if (i+1) % imgBatch == 0:
        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)

        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)

        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)

        for block in bpy.data.objects:
            if block.users == 0:
                bpy.data.objects.remove(block)

        # for block in bpy.data.curves:
        #     if block.users == 0:
        #         bpy.data.curves.remove(block)
        # for block in bpy.data.lamps:
        #     if block.users == 0:
        #         bpy.data.lattices.remove(block)

        # for block in bpy.data.cameras:
        #     if block.users == 0:
        #         bpy.data.cameras.remove(block)
        # Clear cache
        #bpy.ops.wm.memory_statistics(clean_cache=True)
        #bpy.ops.wm.previews_batch_clear(clean_cache=True)

# Elisha - keep track of the total files in each output folder to adjust for different num of imgs in each folder
    totalFilesposBG = len(os.listdir(outfilepath))
    totalFilesposGT = len(os.listdir(outfilepathc))
    totalFilesnegBG = len(os.listdir(outfilepathn))
    totalFilesnegGT = len(os.listdir(outfilepathcn))

    # Elisha - head size variation
    global scaleFactor
    if randomScale:
        scaleFactor = random.uniform(0.0002, 0.0005)
    else:
        scaleFactor = 0.0004

    # Elisha - brightness variation
    if brightnessVariation:
        brightness = random.uniform(0.5, 1.5)

    # Elisha - blur variation
    if blurVariation:
        blur = random.uniform(0.0, 5.0)

    def listFiles(dir, ext):
        fileList = []

        # for file in os.listdir(currentDir):
        for file in os.listdir(dir):
            if file[-len(ext):] == ext:
                fileList.append(file)
        return fileList
    
    def getvars():
        x = random.randrange(-250, 250, 40)
        y = random.randrange(-150, 150, 30)
        rx = random.randrange(-40, 41,1)
        ry = random.randrange(0,181,10)
        rz = random.randrange(-5, 6,1)
        numList = [x, y, rx, ry, rz]
        
        return numList

    def camoimages(x,y,RX,RY,RZ, infile, start=0):
    # arguments that are passed are used to position head and rotate/tilt it
        X=x
        Y=y
        rx = RX
        ry=RY
        rz=RZ

        f = open(path + '/imglog.txt', 'a')

        imgNum = start
        print(imgNum)
        f.write("img" + str(imgNum) + " ")
        whichBG = random.randint(0, 1)
        if whichBG == 0:
            backgrTexPath = path + "/planeImages/bgFruit/"
            foregroundTextures = path + "/planeImages/fgFruit/"
            bgCrop = path + "/planeImages/bgFruit/cropFruit/"
            fgCrop = path + "/planeImages/fgFruit/cropFruit/"

            f.write("fruit ")
        else:
            backgrTexPath = path + "/planeImages/bgTrees/"
            foregroundTextures = path + "/planeImages/fgTrees/"
            bgCrop = path + "/planeImages/bgTrees/cropTree/"
            fgCrop = path + "/planeImages/fgTrees/cropTree/"

            f.write("tree ")

#################################################################################################################################################################

        # Select a random background
        
        # Elisha - when user checkmarks mosaic on GUI, will use bg images in cropFruit and cropTree folders
        backgroundsList = listFiles(dir=backgrTexPath, ext='.jpg')
        bgCropList = listFiles(dir=bgCrop, ext='.jpg')
        if randomMosaic:
            #allBackgrounds = backgroundsList + bgCropList
            randFile = random.randint(0, len(bgCropList)-1)
            backgrTexName = bgCropList[randFile]  # Randomly select a background texture
        else:
            randFile = random.randint(0, len(backgroundsList)-1)
            backgrTexName = backgroundsList[randFile]  # Randomly select a background texture

        f.write("bg" + str(randFile) + " ")

#################################################################################################################################################################

    # Select a random foreground(object) texture
    # Elisha - when user checkmarks mosaic on GUI, will use fg images in cropFruit and cropTree folders
        objTexName = backgrTexName  # set equal to make sure we definitely fall into the while loop and randomly select a foreground
        foregroundsList = listFiles(dir=foregroundTextures, ext='.jpg')
        fgroundsList = listFiles(dir=fgCrop, ext='.jpg')
        if randomMosaic:
            while objTexName == backgrTexName:
                randFile = random.randint(0, len(fgroundsList)-1)
                objTexName = fgroundsList[randFile]  # randomly select a foreground texture that is NOT named the same as the background (i.e. not the same image)
        else:
            while objTexName == backgrTexName:
                randFile = random.randint(0, len(foregroundsList)-1)
                objTexName = foregroundsList[randFile]  # randomly select a foreground texture that is NOT named the same as the background (i.e. not the same image)

        f.write("fg" + str(randFile) + " ")
        outfiletype = ".jpg"

        f.write("X" + str(X) + " ")
        f.write("Y" + str(Y) + " ")
#################################################################################################################################################################
        # Remove all existing objects in the scene
        scene = bpy.context.scene
        for ob in scene.objects:
            ob.select = True
        bpy.ops.object.delete()

#################################################################################################################################################################
        # Import face .obj file
        full_path_to_file = (infilepath + infile)

        bpy.ops.import_scene.obj(filepath=full_path_to_file, \
                                filter_glob="*.obj",
                                use_edges=True, \
                                use_smooth_groups=True, \
                                use_split_objects=False, \
                                use_split_groups=False,
                                use_groups_as_vgroups=False, \
                                use_image_search=False, \
                                split_mode='ON', \
                                global_clamp_size=0.0, \
                                axis_forward='-Z', \
                                axis_up='Y')

        bpy.data.objects[0].name = 'FaceObject'
        # print(bpy.data.objects[0].name)
        face_obj = bpy.data.objects["FaceObject"]
        face_obj.location = (0.0, Y / renderRes_y, -X / renderRes_y)
        face_obj.scale = (scaleFactor, scaleFactor, scaleFactor)

        f.write("sf" + str(scaleFactor) + " ")

#################################################################################################################################################################

        # Now the Background imagePlane
        # Elisha - background imagePlane will use cropped images if mosaic is checked
        bpy.ops.wm.addon_enable(module='io_import_images_as_planes')
        if randomMosaic:
            bpy.ops.import_image.to_plane(files=[{"name": backgrTexName}], directory=bgCrop, filter_image=True, filter_movie=True)
        else:
            bpy.ops.import_image.to_plane(files=[{"name": backgrTexName}], directory=backgrTexPath, filter_image=True, filter_movie=True)
        bpy.data.objects[1].name = 'BackgrImagePlane'
        backimage_obj = bpy.data.objects["BackgrImagePlane"]
        backimage_obj.location = (-2.0, 0.0, 0.0)

        # Elisha - adjust brightness
        if brightnessVariation:
            bpy.context.scene.view_settings.gamma = brightness
            
        # Elisha - adjust blur
        if blurVariation:
            bpy.context.scene.use_nodes = True
            tree = bpy.context.scene.node_tree
            blur_node = tree.nodes.new(type='CompositorNodeBlur')
            blur_node.size_x = blur
            blur_node.size_y = blur
            render_layer_node = tree.nodes['Render Layers']
            composite_node = tree.nodes['Composite']
            tree.links.new(render_layer_node.outputs['Image'], blur_node.inputs['Image'])
            tree.links.new(blur_node.outputs['Image'], composite_node.inputs['Image'])

        # Elisha - Tilt the image plane by a random angle between -5 and 5 degrees
        if tiltImage:
            tilt_angle = random.uniform(-25, 25)
            backimage_obj.rotation_euler = (0, 90, radians(tilt_angle))
        else:
            backimage_obj.rotation_euler = (radians(0), radians(90), radians(0))

        bpy.context.object.active_material.use_shadeless = True

#################################################################################################################################################################

        # Now the camera
        cam = bpy.data.cameras.new("Camera")
        cam_ob = bpy.data.objects.new("Camera", cam)
        bpy.context.scene.camera = cam_ob
        bpy.context.scene.objects.link(cam_ob)
        bpy.context.scene.objects.active = bpy.context.scene.objects["Camera"]
        obj_camera = bpy.data.objects['Camera']  # bpy.types.Camera
        obj_camera.data.type = 'ORTHO'
        obj_camera.location.x = 4.0
        obj_camera.location.y = 0.0
        obj_camera.location.z = 0.0
        obj_camera.rotation_euler = (radians(0), radians(90), radians(0))  # !!!!!!!!!!!!!!!!

#################################################################################################################################################################

        # Create couple of new lamps.  (Using single lamp will create shadows
        # For additional info on lamps, see http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Other_data_types
        lamp1_data = bpy.data.lamps.new(name="Lamp1", type='POINT')
        lamp2_data = bpy.data.lamps.new(name="Lamp2", type='POINT')

        # Create new lamp objects with our lamp datablock
        lamp_obj1 = bpy.data.objects.new(name="Lamp1", object_data=lamp1_data)
        lamp_obj2 = bpy.data.objects.new(name="Lamp2", object_data=lamp2_data)

        # Link lamp objects to the scene so it'll appear in this scene
        scene.objects.link(lamp_obj1)
        scene.objects.link(lamp_obj2)

        # Place lamps in specified locations
        lamp_obj1.location = (0.0, 0.0, 0.0)
        lamp_obj2.location = (0.0, 0.0, 0.0)
        lamp_obj1.data.energy = 3
        lamp_obj2.data.energy = 3

#################################################################################################################################################################

        # Render the scene
        bpy.ops.object.select_all(action='DESELECT')
        face_obj.select = True
        bpy.context.scene.objects.active = face_obj
        bpy.context.object.rotation_mode = 'YZX'
        pi = 3.14159265
        face_obj.rotation_euler[0] = rx * (pi / 180.0)
        face_obj.rotation_euler[1] = ry * (pi / 180.0)
        face_obj.rotation_euler[2] = rz * (pi / 180.0)

        f.write("rx" + str(rx) + " ")
        f.write("ry" + str(ry) + " \n")

        # Set the render params
        pi = 3.14159265
        scene = bpy.data.scenes["Scene"]
        # Set render resolution
        scene.render.resolution_x = renderRes_x
        scene.render.resolution_y = renderRes_y
        scene.render.resolution_percentage = 100
        fov = 90.0
        scene.camera.data.angle = fov * (pi / 180.0)

        # Elisha - in order to not generate images with black borders on edges, camera is zoomed in if tilt is enabled
        if tiltImage:
            scene.camera.data.ortho_scale = 0.95
        else:
            scene.camera.data.ortho_scale = 1.333

        bpy.ops.object.select_all(action='DESELECT')
        face_obj.select = True
        bpy.context.scene.objects.active = face_obj

        # Add a new texture to material
        for i in range(0, 10, 1):
            bpy.ops.object.material_slot_remove()
        mat = bpy.data.materials.new(name="Material")
        bpy.ops.object.material_slot_add()
        bpy.context.object.data.materials[0] = mat
        bpy.context.object.active_material.specular_intensity = 0
        Tex = bpy.data.textures.new("ObjectTexture", type='IMAGE')
        if randomMosaic:
            Img = bpy.data.images.load(fgCrop + "\\" + objTexName)
        else:
            Img = bpy.data.images.load(foregroundTextures + "\\" + objTexName)
        Tex.image = Img
        bpy.context.object.active_material.specular_intensity = 0
        # uncomment next line for activate shadeless option to object material
        bpy.context.object.active_material.use_shadeless = True
        mtex = bpy.context.object.active_material.texture_slots.add()
        mtex.texture = Tex
        mtex.texture_coords = 'WINDOW'
        mtex.use_map_color_diffuse = True
        mtex.diffuse_color_factor = 1.0
        mtex.blend_type = 'MULTIPLY'
        mtex.offset = (random.randint(0, 10001), random.randint(0, 10000),0)

#################################################################################################################################################################

        # filepath = "somepathtoimage"
        if randomMosaic:
            filepath = bgCrop + "\\" + backgrTexName
        else:
            filepath = backgrTexPath + "\\" + backgrTexName
        for a in bpy.context.screen.areas:
            if a.type == 'VIEW_3D':
                break

        if (outfiletype == ".bmp"):
            scene.render.image_settings.file_format = 'BMP'
        elif (outfiletype == ".jpg"):
            # The following code snippet was copied from https://gooseberry.blender.org/simple-python-tips-for-artists/
            # Output to JPEG 100% (for easy test render saving):
            scene.render.image_settings.file_format = 'JPEG'
            scene.render.image_settings.quality = 100
            #scene.render.image_settings.color_depth = '8'
        else:
            scene.render.image_settings.file_format = 'PNG'
            scene.render.image_settings.quality = 100
            #scene.render.image_settings.color_depth = '8'

        face_obj.rotation_euler[1] = ry * (pi / 180.0)
        # Using myFilePath to store the file string so it is not duplicated
        # myFileName = ("(" + str(counter) + ")" + objTexName[:-4] + "_" + infile[:-15] + "_" + backgrTexName[:-4] + outfiletype)		doby

    # Elisha - will generate positive background images if checkmarked from GUI
        if posBGimgs:
        # Elisha - imgNum is set so that it will increment based on the number of images already in the specific folder
            imgNum = totalFilesposBG
            myFileName = "pos" + str(imgNum)
            myLogEntry = (myFileName + ", " + backgrTexName + ", " + infile + ", " + objTexName + ", " + str(
                X) + ", " + str(Y) + ", " + str(rx) + ", " + str(ry) + ", rz" + "\n")  # doby ", " + str(rz)
            myFilePath = (outfilepath + myFileName)
            if not os.path.exists(myFilePath):  # Avoid overwriting
                print(myFilePath)
                if not os.path.exists(path + "/meta.txt"):
                    f = open(path + "/meta.txt", "a")
                    f.write(
                        "FileName, background_texture_name, object_file_name, object_texture_name, X-coord, Y-coord, rotation about X (rx), ry, rz \n\n")  # write a header if meta.txt is new
                else:
                    f = open(path + "/meta.txt", "a")
                f.write(myLogEntry)
                f.close()
                bpy.data.scenes['Scene'].render.filepath = myFilePath
                bpy.ops.render.render(write_still=True)
            else:
                print("Render already exists! Moving to next image...")

    # remove the head and render another image to create the negative
    # Elisha - will generate positive negative background images if checkmarked from GUI
        if negBGimgs:
        # Elisha - imgNum is set so that it will increment based on the number of images already in the specific folder
            imgNum = totalFilesnegBG
            bpy.ops.object.select_all(action='DESELECT')
            face_obj.select = True
            objs.remove(objs["FaceObject"], do_unlink=True)
            bpy.ops.object.select_all(action='DESELECT')

            myFileName = ("neg" + str(imgNum))
            myFilePath = (outfilepathn + myFileName)
            if not os.path.exists(myFilePath):
                bpy.data.scenes['Scene'].render.filepath = myFilePath
                bpy.ops.render.render(write_still=True)
            else:
                print("Render already exists! Moving to next image...")
        bpy.ops.object.delete()
        #f.close()

    # returns images with black backgrounds and white head for training purposes
    def contourimages(x,y,RX,RY,RZ, infile,start = 0):
        X = x
        Y = y
        rx = RX
        ry = RY
        rz = RZ
        world = bpy.context.scene.world
        world.ambient_color = (0, 0, 0)
        world.horizon_color[0] = 0
        world.horizon_color[1] = 0
        world.horizon_color[2] = 0
        world.zenith_color[0] = 0
        world.zenith_color[1] = 0
        world.zenith_color[2] = 0
        
#################################################################################################################################################################
        backgrTexName = blackbg  # Randomly select a background texture
        imgNum = start #+ len(listFiles(dir=outfilepathc, ext='.jpg'))
        # Select a random foreground(object) texture
        objTexName = whitebg
        outfiletype = '.jpg'

#################################################################################################################################################################

        # Remove all existing objects in the scene
        scene = bpy.context.scene
        for ob in scene.objects:
            ob.select = True
        bpy.ops.object.delete()

#################################################################################################################################################################

        # Import face .obj file
        full_path_to_file = (infilepath + infile)

        bpy.ops.import_scene.obj(filepath=full_path_to_file, \
                                filter_glob="*.obj",
                                use_edges=True, \
                                use_smooth_groups=True, \
                                use_split_objects=False, \
                                use_split_groups=False,
                                use_groups_as_vgroups=False, \
                                use_image_search=False, \
                                split_mode='ON', \
                                global_clamp_size=0.0, \
                                axis_forward='-Z', \
                                axis_up='Y')

        bpy.data.objects[0].name = 'FaceObject'
        face_obj = bpy.data.objects["FaceObject"]
        face_obj.location = (0.0, Y / renderRes_y, -X / renderRes_y)
        face_obj.scale = (scaleFactor, scaleFactor, scaleFactor)

#################################################################################################################################################################

        # Now the camera
        cam = bpy.data.cameras.new("Camera")
        cam_ob = bpy.data.objects.new("Camera", cam)
        bpy.context.scene.camera = cam_ob
        bpy.context.scene.objects.link(cam_ob)
        bpy.context.scene.objects.active = bpy.context.scene.objects["Camera"]

        obj_camera = bpy.data.objects['Camera']  # bpy.types.Camera
        obj_camera.data.type = 'ORTHO'
        obj_camera.location.x = 4.0
        obj_camera.location.y = 0.0
        obj_camera.location.z = 0.0
        obj_camera.rotation_euler = (radians(0), radians(90), radians(0))  # !!!!!!!!!!!!!!!!

#################################################################################################################################################################

        # Create couple of new lamps.  (Using single lamp will create shadows
        # For additional info on lamps, see http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Other_data_types
        lamp1_data = bpy.data.lamps.new(name="Lamp1", type='POINT')
        lamp2_data = bpy.data.lamps.new(name="Lamp2", type='POINT')
        # Create new lamp objects with our lamp datablock
        lamp_obj1 = bpy.data.objects.new(name="Lamp1", object_data=lamp1_data)
        lamp_obj2 = bpy.data.objects.new(name="Lamp2", object_data=lamp2_data)
        # Link lamp objects to the scene so it'll appear in this scene
        scene.objects.link(lamp_obj1)
        scene.objects.link(lamp_obj2)
        # Place lamps in specified locations
        lamp_obj1.location = (6.0, 3.0, 0.0)
        lamp_obj2.location = (6.0, -3.0, 0.0)
        lamp_obj1.data.energy = 3
        lamp_obj2.data.energy = 3

#################################################################################################################################################################

        # Render the scene
        bpy.ops.object.select_all(action='DESELECT')
        face_obj.select = True
        bpy.context.scene.objects.active = face_obj
        bpy.context.object.rotation_mode = 'YZX'
        pi = 3.14159265
        face_obj.rotation_euler[0] = rx * (pi / 180.0)
        face_obj.rotation_euler[1] = ry * (pi / 180.0)
        face_obj.rotation_euler[2] = rz * (pi / 180.0)

        # Set the render params
        pi = 3.14159265
        scene = bpy.data.scenes["Scene"]
        # Set render resolution
        scene.render.resolution_x = renderRes_x
        scene.render.resolution_y = renderRes_y
        scene.render.resolution_percentage = 100
        fov = 90.0
        scene.camera.data.angle = fov * (pi / 180.0)

    # Elisha - adjust scene camera to remove black borders dur to tilting the image
        if tiltImage:
            scene.camera.data.ortho_scale = 0.95
        else:
            scene.camera.data.ortho_scale = 1.333

        bpy.ops.object.select_all(action='DESELECT')
        face_obj.select = True
        bpy.context.scene.objects.active = face_obj

        # Add a new texture to material
        for i in range(0, 10, 1):
            bpy.ops.object.material_slot_remove()
        mat = bpy.data.materials.new(name="Material")
        bpy.ops.object.material_slot_add()
        bpy.context.object.data.materials[0] = mat
        bpy.context.object.active_material.specular_intensity = 0
        Tex = bpy.data.textures.new("ObjectTexture", type='IMAGE')
        Img = bpy.data.images.load(whitebg)
        Tex.image = Img
        bpy.context.object.active_material.specular_intensity = 0
        bpy.context.object.active_material.use_shadeless = True
        mtex = bpy.context.object.active_material.texture_slots.add()
        mtex.texture = Tex
        mtex.texture_coords = 'WINDOW'
        mtex.use_map_color_diffuse = True
        mtex.diffuse_color_factor = 1.0
        mtex.blend_type = 'MULTIPLY'

#################################################################################################################################################################

        for a in bpy.context.screen.areas:
            if a.type == 'VIEW_3D':
                break

        if (outfiletype == ".bmp"):
            scene.render.image_settings.file_format = 'BMP'
        elif (outfiletype == ".jpg"):
            # The following code snippet was copied from https://gooseberry.blender.org/simple-python-tips-for-artists/
            # Output to JPEG 100% (for easy test render saving):
            scene.render.image_settings.file_format = 'JPEG'
            scene.render.image_settings.quality = 100
            #scene.render.image_settings.color_depth = '8'
        else:
            scene.render.image_settings.file_format = 'PNG'
            scene.render.image_settings.quality = 100
            #scene.render.image_settings.color_depth = '8'

    # Elisha - will generate positive ground truth images if checkmarked from GUI
        if posGTimgs:
        # Elisha - imgNum is set so that it will increment based on the number of images already in the specific folder
            imgNum = totalFilesposGT
            face_obj.rotation_euler[1] = ry * (pi / 180.0)
            myFileName = ("posCont" + str(imgNum))
            myFilePath = (outfilepathc + myFileName)
            if not os.path.exists(myFilePath):  # Avoid overwriting
                bpy.data.scenes['Scene'].render.filepath = myFilePath
                bpy.ops.render.render(write_still=True)
            else:
                print("Render already exists! Moving to next image...")

    # Elisha - will generate negative ground truth images if checkmarked from GUI
        if negGTimgs:
        # Elisha - imgNum is set so that it will increment based on the number of images already in the specific folder
            imgNum = totalFilesnegGT
            bpy.ops.object.select_all(action='DESELECT')
            face_obj.select = True
            objs.remove(objs["FaceObject"], do_unlink=True)
            bpy.ops.object.select_all(action='DESELECT')

            myFileName = ("negCont" + str(imgNum))
            myFilePath = (outfilepathcn + myFileName)
            if not os.path.exists(myFilePath):
                bpy.data.scenes['Scene'].render.filepath = myFilePath
                bpy.ops.render.render(write_still=True)
            else:
                print("Render already exists! Moving to next image...")

        bpy.ops.object.delete()

    def generate_image(imgNum, infilepath, start = 0, min=0):
        while min < imgNum:
            for infile in listFiles(dir = infilepath, ext = '.obj'):
                if min < imgNum:
                    vals = getvars()
                    x = vals[0]
                    y = vals[1]
                    rx = vals[2]
                    ry = vals[3]
                    rz = vals[4]
                    contourimages(x,y,rx,ry,rz, infile, start)
                    camoimages(x,y,rx,ry,rz, infile, start)
                    start += 1
                    min += 1

# Elisha - negative_enabled is redundant
    # if negBGimgs or negGTimgs:
    #    negative_enabled = True
    # else:
    #     negative_enabled = False

    #maxx = input("Enter max ")
    # maxx = 5
    imgNum = 1
    outfilepath = path + "/outputFiles/outputBGpos/"
    outfilepathc = path + "/outputFiles/outputGTpos/"
    outfilepathn = path + "/outputFiles/outputBGneg/"
    outfilepathcn = path + "/outputFiles/outputGTneg/"

    folders = [outfilepath, outfilepathc, outfilepathn, outfilepathcn]
    totalFiles = max([len(os.listdir(folder)) for folder in folders])
    start = totalFiles

    #start = input('which index to start from: ')
    #start = len(file_names1) + 10000


    print(start)
    generate_image(int(imgNum), infilepath, int(start))
    # generate_image(int(imgNum), infilepath, negative_enabled, int(start))

