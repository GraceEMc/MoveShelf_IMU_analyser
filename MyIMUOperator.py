# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:51:24 2020

@author: Joris Ravenhorst
"""
# Import the opensim libraries
import os
import glob
import time
import opensim as osim # necessary to read setup file
from numpy import pi # necessary to read setup file
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# from api import MoveshelfApi, Metadata
# api = MoveshelfApi()

# from OS_trialsetup import trialsetup
from OS_IMUmappings import IMUmappings
from OS_findFirst_t import findFirst_t
from OS_csv_to_txt import csv_to_txt
from OS_IMUDataConversion import IMUdata_conversion
from OS_CalibrateModel import calibrate_model
from OS_InvKin import inv_kinematics
from OS_createAngles_json import createAngles_json
from OS_investigateJoints import investigateJoints
from OS_plotJointangles import plotJointangles
from OS_plotQuaternions import plotQuats
import pdb


class Application:
    
    def MyIMUanalyser(self,TrialName,modelFileName,visualizeCalibration,visualizeTracking):

        sensor_to_opensim_rotation = osim.Vec3(-pi/2,0,0)	# The rotation of IMU data to the OpenSim world frame. !! Only change if subject/model is not facing x-direction in the calibration pose. 
        import pdb; 
        
        
        #------------------------------------------------------------------------------
        # %% Setup
        #   -if uploading: to which project?
        #   -Find .csv IMU data and setup.txt.
        #   -Creates 'myIMUMappings.xml' : which IMU belongs to which body segment.
        #   -Resets the heading of all IMUs to 0 yaw in initial timestep. Assuming all IMUs are aligned.
        #   -Applies heading reset to whole dataset so all IMU orientations are relative to a shared initial position.
        #   -Cuts pre-calibration data from dataset.
        #   -Creates .txt files from .csv files in useable format.
        
           
            
        #---find data and setup
        for x in os.listdir(os.path.dirname(os.path.realpath('__file__'))+'\\IMUData'):    # runs through all directories in IMUData
            if TrialName in x:
                self._trial_dir_path = os.path.dirname(os.path.realpath('__file__'))+'\\IMUData\\'+x+'\\' # search for directory with 'trial' in its name
                trial_dir_path = self._trial_dir_path
                
        
        
        #---get .csv files
                files = glob.glob(trial_dir_path+'*.csv')
                count = 0
                for x in files:
                    files[count] = files[count].replace(trial_dir_path,'')
                    count+=1
        
        pdb.set_trace()
        #---Xsens or Vicon?
        if 'DOT' in files[0]:
            sensor = 'Xsens'
            delay = 0
        if 'TS' in files[0]:
            sensor = 'Vicon'
            
            
        #---retrieve trial settings from setup file
        ldic = locals()
        exec(open(trial_dir_path + 'setup.txt','r').read(),globals(),ldic)
        
        device = ldic['device']
        freq = ldic['freq']
        t_calib = ldic['t_calib']  
        t_range = ldic['t_range']
        delay = ldic['delay']
        baseIMUName = ''
        baseIMUHeading = ''
        IMUs = ldic['IMUs']
    
        t_range = [t_range[0]-t_calib, t_range[1]-t_calib]
        
        
        #---which joints are involved?
        joints = investigateJoints(IMUs)
        
        
        #---create myIMUmappings.xml
        IMUmappings(sensor,trial_dir_path,files,IMUs)
        
        
        #---convert output data .csv files to .txt in useable format 
        #   and perform interpolation and heading reset
        t0 = [0]*len(IMUs)
        
        count = 0
        for csvfilename in files:
            t0[count] = findFirst_t(sensor, trial_dir_path, csvfilename, device)
            count += 1
        
        count = 0
        for x in files:
            print('{}'.format(IMUs[count]))
            csv_to_txt(sensor, trial_dir_path, files[count], device, t_calib, freq, delay, t_range, t0)
            count += 1
          
            
          
        #------------------------------------------------------------------------------
        # IMUDataConversion
        #   -Create .sto files of orientation, lin acceleration, magnetic north heading, angular velocity.
        #   -If no such data is provided, the file is left empty.
        trialID = IMUdata_conversion(trial_dir_path,TrialName)
        
TrialName = 'On Table-2calibrate-1'                                  # Should include date and trial number.
modelFileName = 'OpenSim_model.osim'             # The path to input model.
visualizeCalibration = False                      # Visualize calibrated model?
visualizeTracking = False                        # Visualize motion?
app = Application()
app.MyIMUanalyser(TrialName,modelFileName,visualizeCalibration,visualizeTracking)