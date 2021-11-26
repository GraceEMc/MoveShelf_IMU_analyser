device = 'apple'			# phone operating system 'apple' or 'android'?
freq = 225 			# sampling frequency of IMUs [Hz]
t_calib = 130 			# time point in measurement when calibration pose is performed, [s]
t_range = [150,180]			# time range to process/visualize, [s]

# For Vicon Blue Tridents:
delay = 70			# time point at which IMUs are aligned after sensor calibration.

# list body segments to corresponding imus. in imu order (increasing number): ['imu_01', 'imu_02', 'imu_03' ...
IMUs = ['tibia_r','femur_r'] 





