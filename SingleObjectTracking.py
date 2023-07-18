import cv2
import sys
import os

class SingleObjectTrackingClass:
    def __init__(self,input_file,tracker_index=None):
        tracker_list = ['BOOSTING','MIL','KCF','TLD','MEDIANFLOW','GOTURN','MOSSE','CSRT']
        if tracker_index is None:
            tracker_type = tracker_list[7]#If tracker index not provided by user then use CSRT
        else:
            tracker_type = tracker_list[tracker_index]
        
        if tracker_type == 'BOOSTING':
            self.tracking_algo = cv2.TrackerBoosting_create() # self.tracking_algo defines the OpenCV object tracker implementations
        elif tracker_type == 'MIL':
            self.tracking_algo = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            self.tracking_algo = cv2.TrackerKCF_create()
        elif tracker_type == 'TLD':
            self.tracking_algo = cv2.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            self.tracking_algo = cv2.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
            self.tracking_algo = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            self.tracking_algo = cv2.TrackerMOSSE_create()
        elif tracker_type == 'CSRT':
            self.tracking_algo = cv2.TrackerCSRT_create()
        self.input = input_file
        self.tracker_type = tracker_type

    def single_object_tracking_main(self):
        vid_frame = cv2.VideoCapture(self.input)
        if not vid_frame.isOpened(): #checks if the video file was opened successfully. 
            print('Error in opening the video file') #If not, it prints an error message
            sys.exit()# and exits the program.

#reads the first frame of the video
        ok,image = vid_frame.read()
        #ok indicates if the frame was read successfully
        #image contains the actual frame data.


        if not ok:# checks if the frame was read successfully
            print('Error in reading the video file')#If not, it prints an error message 
            sys.exit() #and exits the program.

#displays the first frame using the cv2.selectROI() function, which allows the user to select a rectangular region of interest (ROI) around the target object.
# The selected ROI is stored in the bbox variable.
        bbox = cv2.selectROI(image,False)

#initializes the tracking algorithm (self.tracking_algo) with the first frame (image) and the selected ROI (bbox)
        ok = self.tracking_algo.init(image,bbox)

        image_list = list()#initializes an empty list to store the tracked frames
        while True:
            ok,image=vid_frame.read()# reads the next frame from the video file.
            if not ok: #checks if the frame was read successfully
                break # breaks the loop and exits the tracking process

#updates the tracking algorithm (self.tracking_algo) with the current frame (image).
#  The algorithm estimates the new bounding box (bbox) for the tracked object in the current frame.
            ok,bbox = self.tracking_algo.update(image)

            if ok:
                point1 = (int(bbox[0]),int(bbox[1])) #define the top-left and bottom-right points. of the bounding box
                point2 = (int(bbox[0] + bbox[2]),int(bbox[1] + bbox[3]))
                cv2.rectangle(image,point1,point2,(255,255,255),2,1) #draws a rectangle around the tracked object 
            else: #if the tracking was not successful for the current frame
                cv2.putText(image,"Error in Tracking",(50,20),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)# to indicate the tracking failure.

#adds a text label to the image indicating the tracker type being used.
            cv2.putText(image,self.tracker_type,(50,20),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
            cv2.imshow("Tracked_frame",image)#displays the current frame with the bounding box and the tracker type label.
            image_list.append(image)#appends the current frame

            if cv2.waitKey(30) & 0xFF == ord('q'):#checks for the 'q' key press
                break

        vid_frame.release() #releases the video file being read, freeing up system resources.
        cv2.destroyAllWindows() # closes all the OpenCV windows that were opened during the tracking process.

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')#specifies the codec to be used for the output video file.
        each_frame = image_list[0] #selects the first frame to retrieve its dimensions used to define the output video's frame size

        output_folder = '../OutputFolder'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder,0o755)
        output_file_path = os.path.join(output_folder,"Video.mp4")

#creates a VideoWriter object to write the tracked frames to a new video file. 
#It specifies the output file path, codec, frame rate (24 frames per second in this case), and the frame size based on the dimensions of each_frame.
        new_video = cv2.VideoWriter(output_file_path, fourcc, 24, (each_frame.shape[1], each_frame.shape[0]))

        for each_frame in image_list: #iterates through each tracked frame
            new_video.write(each_frame) #writes each frame to the output video file.
        
        new_video.release() #eleases the VideoWriter object, finalizing and saving the output video file.

if __name__ == '__main__':
    input_path = 'C:/Users/Urvi Latnekar/Desktop/Data Science/ProjectPro/Object Tracking/Data/car_driving.mp4'
    objTrack = SingleObjectTrackingClass(input_path, tracker_index = 7)
    objTrack.single_object_tracking_main()


















