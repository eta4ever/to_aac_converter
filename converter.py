"""
Simple "to aac" converter
"""
import os
from subprocess import *

# GUI module import
from tkinter import *
from tkinter.ttk import * # better gui
from tkinter import filedialog

# global constants for folders, program root default
INPUTROOT = os.getcwd()
OUTPUTROOT = os.getcwd()

# AAC encoder keys
AACPARAMS = '--cbr 512 --profile lc'

# external tools paths %prog/tools/
FFMPEGPATH = os.path.join(os.getcwd(), 'tools', 'ffmpeg.exe')
FHGAACENCPATH = os.path.join(os.getcwd(), 'tools', 'fhgaacenc.exe')

# filetypes processing
PROCESSFILETYPES = ['.flac', '.ape', '.m4a', '.wv']

def ProcessFolder(inputDirectory, outputDirectory):
    """
    processing files lossless -> AAC from inputDirectory.
    temporary files and results are in outputDirectory
    """
    
    def Launch(cmd):
        """
        subprocess launch as separate function
        """

        #PIPE = subprocess.PIPE
        p = Popen(cmd, shell=True)
        p.wait()

    # filelist generation
    dirFileList = os.listdir(inputDirectory)

    # 0 - filename, 1 - extension
    procFileList = list(filter(lambda fileName: 
        os.path.splitext(fileName)[1] in PROCESSFILETYPES, dirFileList))


    # transcode  to WAV (ffmpeg) and encode to AAC(FHGAACENC)
    for procFile in procFileList:

        # get filename w/o extension
        procFileNoExt = os.path.splitext(procFile)[0]

        # generate ffmpeg command
        inputFilePath = os.path.join(inputDirectory, procFile)
        outputFilePath = os.path.join(outputDirectory, procFileNoExt + '.wav')
        cmdKey = '-i ' + '"' + inputFilePath + '" "' + outputFilePath + '"'
        cmd = FFMPEGPATH + ' ' + cmdKey 

        # transcode to wav - launch
        Launch(cmd)

        # generate FHGAACENC command
        inputFilePath = outputFilePath # ffmpeg out is FHGAACENC input
        outputFilePath = os.path.join(outputDirectory, procFileNoExt + '.m4a')
        cmdKey = AACPARAMS + ' "' + inputFilePath + '" "' + outputFilePath + '"'    
        cmd = FHGAACENCPATH + ' ' + cmdKey

        # encode to aac - launch
        Launch(cmd)

        # remove .wav
        os.remove(inputFilePath)

# folder selection dialog
def SelectFolder(event, typeOfDir):

    # options
    dialogOptions = {}
    dialogOptions['mustexist'] = True
    dialogOptions['parent'] = root
    dialogOptions['initialdir'] = INPUTROOT

    # launch dialog
    selectedDir = filedialog.askdirectory(**dialogOptions)

    if typeOfDir == 'in':
        inputDirectory = selectedDir
    elif 'out':
        outputDirectory = selectedDir

# process function
def Process(event, inputDirectory, outputDirectory):
    
    # directory tree walking
    for basePath, watchingDir, filesInDir in os.walk(inputDirectory):
        
        # subfolder files watching
        for fileInDir in filesInDir:
            
            # process subfolder if file with "right" extension exists
            if os.path.splitext(fileInDir)[1] in PROCESSFILETYPES:

                # relative subfolder path generation
                dirStruct = os.path.relpath(basePath, inputDirectory)

                # create dir structure in output folder
                outputPath = os.path.join(outputDirectory, dirStruct) 
                os.makedirs(outputPath)

                # process folder
                ProcessFolder(basePath, outputPath)

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
buttonInputDir.bind("<Button-1>", lambda event: SelectFolder(event,'in'))  

# button for output selection
buttonOutputDir = Button(test_frame, text = 'Output dir')
buttonOutputDir.place(x = 120, y = 75, width = 100, height = 50)
buttonOutputDir.bind("<Button-1>", lambda event: SelectFolder(event,'out'))  

# Launch button
buttonProcess = Button(test_frame, text = 'Process')
buttonProcess.place(x = 230, y = 75, width = 100, height = 50)
buttonProcess.bind("<Button-1>", lambda event: Process(event,)) # 


root.mainloop() # window

