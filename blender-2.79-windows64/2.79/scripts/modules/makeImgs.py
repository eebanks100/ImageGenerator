import subprocess
import os
#import math

outfilepath = "./outputFiles/outputBGpos/"
outfilepathc = "./outputFiles/outputGTpos/"
outfilepathn = "./outputFiles/outputBGneg/"
outfilepathcn = "./outputFiles/outputGTneg/"

totalFilesposBG = len(os.listdir(outfilepath))
totalFilesposGT = len(os.listdir(outfilepathc))
totalFilesnegBG = len(os.listdir(outfilepathn))
totalFilesnegGT = len(os.listdir(outfilepathcn))

folders = [outfilepath, outfilepathc, outfilepathn, outfilepathcn]

def wipeData(cmd):
	for folder in folders:
		files = os.listdir(folder)  # get list of file names in the folder
		for file in files:
			filePath = os.path.join(folder, file)  # get full path of the file
			if os.path.isfile(filePath):  # check if the file is a regular file
				os.remove(filePath)  # remove the file

def imgGen(imgNum, cmd, width, height, posBGimgs, posGTimgs, negBGimgs, negGTimgs, headsize, tilt, mosaic, brightness, blur):
	blenderLocation = r'".\blender-2.79-windows64\blender.exe"'
	blenderScript = r'./imageGen.py'
	#NumImgsNeeded = totalFilesposGT + (imgNum/4)
# Elisha - passing imgNum to imageGen no longer opening and closing blender which slows down image generation
	#subprocess.call(f'{blenderLocation} --background -P {blenderScript} -- {imgNum} {width} {height} {posBGimgs} {posGTimgs} {negBGimgs} {negGTimgs} {headsize} {tilt} {mosaic} {brightness} {blur}', shell=True)	
	subprocess.call([f'./blender-2.79-windows64/blender.exe --background -P ./imageGen.py', '--', f'{imgNum}', f'{width}', f'{height}', f'{posBGimgs}', f'{posGTimgs}', f'{negBGimgs}', f'{negGTimgs}', f'{headsize}', f'{tilt}', f'{mosaic}', f'{brightness}', f'{blur}'])

	
	# i = 0
	# while totalFilesposGT < NumImgsNeeded and i < imgNum:
	# 	subprocess.call(f'{blenderLocation} --background -P {blenderScript} -- {imgNum} {width} {height} {posBGimgs} {posGTimgs} {negBGimgs} {negGTimgs} {headsize} {tilt} {mosaic} {brightness} {blur}', shell=True)
	# 	totalFilesposGT = len(os.listdir(outfilepathc))
	# 	i += 1

	#totalFiles = sum([len(os.listdir(folder)) for folder in folders])
	#file_names1 = os.listdir(p1)

# Elisha - num was for old removal of extra images generated
	# num = imgNum
	#imgNum = math.floor((imgNum - totalFiles) / 4) + 1

	# print(imgNum)
	# for i in range(0, int(imgNum)):
	# 	subprocess.call(f'{blenderLocation} --background -P {blenderScript} -- {width} {height} {posBGimgs} {posGTimgs} {negBGimgs} {negGTimgs} {headsize} {tilt} {mosaic} {brightness} {blur}', shell=True)





# Elisha - no longer need cleaner.py, rename.py, or the additional code that removes duplicate images during generation

# after imageGen.py has finished generating all the images, run the cleaner
	# subprocess.run(['python', 'cleaner.py'])

	# for folder in folders:
	# 	fileList = os.listdir(folder)
	# 	if len(fileList) > num:
	# 		for i in range(num, len(fileList)):
	# 			if fileList[i].__contains__('pos') or fileList[i].__contains__('neg'):
	# 				continue
	# 			else:
	# 				filePath = os.path.join(folder, fileList[i])
	# 				os.remove(filePath)


	# for folder in folders:
	# 	fileList = os.listdir(folder)
	# 	if len(fileList) > num:
	# 		for i in range(num, len(fileList)):
	# 			filePath = os.path.join(folder, fileList[i])
	# 			os.remove(filePath)

	# blenderScript = r'rename.py'
	# subprocess.run(['python', 'rename.py'])


# Elisha - old logic, would crash when changing checkboxes for image type

	# file_names1 = os.listdir(p1)		#this is logic for deleting the corresponding images if we want to for example check an image from 1 folder 
	# file_names2 = os.listdir(p2)		#to see if it is black, and then delete the corresponding images in the other folders
	# file_names3 = os.listdir(p3)
	# file_names4 = os.listdir(p4)

	# if len(file_names1) > num:
	# 	for i in range(0, len(file_names1) - num):
	# 		if i < len(file_names1):
	# 			os.remove(p1 + file_names1[i])
	# 		if i < len(file_names2):
	# 			os.remove(p2 + file_names2[i])
	# 		if i < len(file_names3):
	# 			os.remove(p3 + file_names3[i])
	# 		if i < len(file_names4):
	# 			os.remove(p4 + file_names4[i])

	#subprocess.call(f'{blenderScript}', shell=True)