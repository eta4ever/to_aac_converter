"""
Simple "to aac" converter
"""
import os
from subprocess import *

# GUI module import
from tkinter import *
from tkinter.ttk import * # better gui
from tkinter import filedialog

# global vars for folders, program root default
inputRoot = os.getcwd()
outputRoot = os.getcwd()

# AAC encoder keys
aacParams = '--cbr 512 --profile lc'

# external tools paths %prog/tools/
ffmpegPath = os.path.join(os.getcwd(), 'tools', 'ffmpeg.exe')
fhgaacencPath = os.path.join(os.getcwd(), 'tools', 'fhgaacenc.exe')

# filetypes processing
processFileTypes = ['.flac', '.ape', '.m4a', '.wv']

# processing files lossless -> AAC from inputDirectory
# temporary files and results are in outputDirectory
def ProcessFolder(inputDirectory, outputDirectory):

    # subprocess launch as separate function
    def Launch(cmd):

        #PIPE = subprocess.PIPE
        p = Popen(cmd, shell=True)
        p.wait()

    # filelist generation
    dirFileList = os.listdir(inputDirectory)

    # 0 - filename, 1 - extension
    procFileList = list(filter (lambda fileName: 
        os.path.splitext(fileName)[1] in processFileTypes, dirFileList))


    # transcode  to WAV (ffmpeg) and encode to AAC (fhgaacenc)
    for procFile in procFileList:

        # get filename w/o extension
        procFileNoExt = os.path.splitext(procFile)[0]

        # generate ffmpeg command
        inputFilePath = os.path.join(inputDirectory, procFile)
        outputFilePath = os.path.join(outputDirectory, procFileNoExt + '.wav')
        cmdKey = '-i ' + '"' + inputFilePath + '" "' + outputFilePath + '"'
        cmd = ffmpegPath + ' ' + cmdKey 

        # transcode to wav - launch
        Launch(cmd)

        # generate fhgaacenc command
        inputFilePath = outputFilePath # ffmpeg out is fhgaacenc input
        outputFilePath = os.path.join(outputDirectory, procFileNoExt + '.m4a')
        cmdKey = aacParams + ' "' + inputFilePath + '" "' + outputFilePath + '"'    
        cmd = fhgaacencPath + ' ' + cmdKey

        # encode to aac - launch
        Launch(cmd)

        # remove .wav
        os.remove(inputFilePath)

# folder selection dialog
def SelectFolder (event, typeOfDir):

    # options
    dialogOptions = {}
    dialogOptions['mustexist'] = True
    dialogOptions['parent'] = root
    dialogOptions['initialdir'] = inputRoot

    # launch dialog
    selectedDir = filedialog.askdirectory(**dialogOptions)

    # where to work
    global inputRoot, outputRoot
    
    if typeOfDir == 'in':
        inputRoot = selectedDir
    elif 'out':
        outputRoot = selectedDir

# process function
def Process (event):
    
    # directory tree walking
    for basePath, watchingDir, filesInDir in os.walk(inputRoot):
        
        # subfolder files watching
        for fileInDir in filesInDir:
            
            # process subfolder if file with "right" extension exists
            if os.path.splitext(fileInDir)[1] in processFileTypes:

                # relative subfolder path generation
                dirStruct = os.path.relpath(basePath, inputRoot)

                # create dir structure in output folder
                outputDirectory = os.path.join(outputRoot, dirStruct) 
                os.makedirs(outputDirectory)

                # process folder
                ProcessFolder(basePath, outputDirectory)

                # don't continue to watch files in subfolder
                break

root = Tk()

# frame creation
test_frame = Frame(root, 
                    width = 500, 
                    height = 200)

# frame alignment
test_frame.pack(side = 'left')

# button for input selection
buttonInputDir = Button(test_frame, text = 'Input dir')
buttonInputDir.place(x = 10, y = 75, width = 100, height = 50)
buttonInputDir.bind("<Button-1>", lambda event: SelectFolder(event,'in')) # 

# button for output selection
buttonOutputDir = Button(test_frame, text = 'Output dir')
buttonOutputDir.place(x = 120, y = 75, width = 100, height = 50)
buttonOutputDir.bind("<Button-1>", lambda event: SelectFolder(event,'out')) # 

# Launch button
buttonProcess = Button(test_frame, text = 'Process')
buttonProcess.place(x = 230, y = 75, width = 100, height = 50)
buttonProcess.bind("<Button-1>", Process) # 


root.mainloop() # window

