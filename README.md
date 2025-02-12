This package is able to do full body motion analysis with data from Xsens DOT and Vicon Blue Trident sensors. You can choose to analyse the results in the console, or to upload your results to MoveShelf to organise, analyse and share your results. 


**1.	Requirements**

1.1	Python 3.7 and OpenSim 4.1. Install the opensim python package as described here: https://simtk-confluence.stanford.edu/display/OpenSim/Scripting+in+Python#ScriptinginPython-SettingupyourPythonscriptingenvironment 

**2.	Folders and files**
The default setup of the file system is as follows:

- MoveShelf_IMU_analyser	> main folder, place it anywhere on computer.
	- Geometry				                > folder supportive to OpenSim model.
	- IMUData				                > data folder.
		- 20201104_1_example trial	    > example folder containing data for one trial.
		- setup.txt			              > has to be copied into every trial folder. 
	- MoveShelf_IMU_operator.py	    > interactive script to execute analysis.
	- api.py				                  > MoveShelf’s API, adjusted to this application.
	- mvshlf-api-key.json	              > You have to import your own api-key from your MoveShelf account.
	- OpenSense_Main.py			        > main function.		
	- OpenSim_model.osim		          > OpenSim model. You can add your own.
	- OS_CalibrateModel.py 
	- OS_createAngles_json.py
	- OS_csv_to_txt.py
	- OS_findFirst_t.py
	- OS_IMUDataConversion.py
	- OS_IMUmappings.py
	- OS_Interpolation_slerp_Vicon.py	  > support functions.
	- OS_Interpolation_slerp_Xsens.py
	- OS_investigateJoints.py
	- OS_InvKin.py
	- OS_plotJointangles.py
	- OS_plotMatrix.py
	- OS_plotQuaternions.py
	- OS_plotQuaternions_v2.py
	- OS_reset_heading.py
	- OS_sync_tridents.py

	Note: If you would like to use an OpenSim model (.osim) other than the one provided, then changes may have to be implemented in OS_investigateJoints.py and 	OS_createAngle_json.py.


2.1.	Main folder:
- Additional files will be created in this folder upon processing trials. If these already exist, they will be overwritten:
	- “err.txt” 
  Output of “OS_CalibrateModel.py”. Contains error messages if encountered.

  - “out.txt”
  Output of “OS_CalibrateModel.py”. Contains orientation offsets (matrices) of the IMUs relative to the according body segment of the OpenSim model.

  - “myIMUmappings.xml”
  Output of “OpenSense_Main.py”, input to “OS_IMUDataConversion.py”. Describes which IMU was attached to which body segment.

  - “calibrated_<OpenSim model>.osim”
  Output of “OS_CalibrateModel.py”, input to “OS_InvKin.py”. This file contains the calibrated OpenSim model. A copy of this file is also stored in the trial folder.
	
2.2.	Geometry
Contains files necessary to construct “<OpenSim model>.osim”

2.3.	IMUData
Contains all trial folders and “setup_format.txt”. 
- The naming of the trial folders should be following format: “yyyymmdd_<trial number><optional description>”, e.g. “20201104_1 knee extension”.
- “setup.txt” is a file that has to be copied to any trial folder before processing! This file is a fill-in file, requesting info about the measurement.


**3.	Measurement Manual (Vicon Blue Trident and Xsens DOT)**
These are the steps needed to do a measurement:

3.1	Digital setup.
Create a folder for the trial under IMUData and insert a copy of setup.txt. Fill in what the operating system is of your mobile device, together with the sampling rate of the sensors and which sensor will be placed on which body segment. The naming of the body segments should be the same as in your OpenSim model, otherwise they will not bet recognized.

3.2	A. Start trial: DOTs.
- Align IMUs. Put all IMUs that will be used on a flat surface in the exact same orientation. IMU z-axis should face upward. This step is needed for the script to perform a heading reset. In this operation the IMU world frames are aligned with the IMU local frames. Since all IMUs are facing the same direction, they now share a global frame.
- Start the measurement in the mobile app. Settings:
	- In “Dashboard” select sensors.
	- In “Measure & Collect” select “Real-time Streaming” and confirm sensors.
	- Press “START”
	- Under “Select Transmit Data”: select “Sensor Fusion Data”
			- Select “Orientation” and “Quaternions”
			- Make sure “Synchronization” and “Data Logging” are on.
			- Upon pressing “Apply” the measurement starts.

B. Start trial: Blue Tridents.
- Align IMUs. Put all IMUs that will be used on a flat surface in the exact same orientation. IMU z-axis should face upward. This step is needed for the script to perform a heading reset. In this operation the IMU world frames are aligned with the IMU local frames. Since all IMUs are facing the same direction, they now share a global frame.
- Start the measurement in the mobile app. Settings: 
	- Create a session and start a new trial.
		- Global Angles: On
		- Capture Viceo: Optional
		- Press “Start Capture”
	- Select sensors.
	- Upon pressing “Start Capture” again, the measurement starts.

- Perform sensor calibration as described by Vicon :
- Wave the sensor in a figure-of-eight for at least 10 seconds, ensuring that it rotates through all three axes during the motion.
- Put the sensor on a flat surface and spin it through two full rotations.
- Wait at least five seconds until the data has stabilized.
	- Make sure you end the calibration in the aligned orientation.

3.3	Attach IMUs to the subject.

3.4	Perform calibration pose.
- Assume the same position as the OpenSim model you are going to use.
- Make sure you are facing the same direction in the IMU world frame as the OpenSim model does in the OpenSim world frame. 
The provided OpenSim model looks along the positive x-axis, so your subject should look along the positive x-axis of the IMU world frame too.
	  -  Note the time point of assuming the calibration pose as t_calib in “setup.txt”.

3.5	Perform motion.
Perform the motion you want to measure. Note the beginning and end time in “setup.txt” in t_range. 

3.6	Stop measurement.
Stop the measurement in the mobile application. The data files are stored on the phone itself.

**4.	Processing**

4.1	Import the sensor output files (.csv) to the trial folder.

4.2	Open “_MoveShelf_IMU_operator.py” and fill in your preferences.

4.3	Upon running, the script asks to which project you would like to upload the trial to. Here it will create a new clip named after the trial folder.

4.4	You can add a video of the kinematics by recording the motion manually in OpenSim and upload the video using the second section of the script. 

