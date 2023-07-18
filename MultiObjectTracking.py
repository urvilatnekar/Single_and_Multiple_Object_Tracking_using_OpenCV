import cv2
import sys
import os
from random import randint

class MultiObjectTrackingClass:
    def __init__(self,input_file,tracker_index=None):
        self.tracker_list = ['BOOSTING','MIL','KCF','TLD','MEDIANFLOW','GOTURN','MOSSE','CSRT']
        self.input = input_file
        self.tracker_type = self.tracker_list[tracker_index]

    def create_tracker(self,tracker_type): 
        
        if tracker_type == self.tracker_list[0]:
            tracking_algo = cv2.TrackerBoosting_create() # self.tracking_algo defines the OpenCV object tracker implementations
        elif tracker_type == self.tracker_list[1]:
            tracking_algo = cv2.TrackerMIL_create()
        elif tracker_type == self.tracker_list[2]:
            tracking_algo = cv2.TrackerKCF_create()
        elif tracker_type == self.tracker_list[3]:
            tracking_algo = cv2.TrackerTLD_create()
        elif tracker_type == self.tracker_list[4]:
            tracking_algo = cv2.TrackerMedianFlow_create()
        elif tracker_type == self.tracker_list[5]:
            tracking_algo = cv2.TrackerGOTURN_create()
        elif tracker_type == self.tracker_list[6]:
            tracking_algo = cv2.TrackerMOSSE_create()
        elif tracker_type == self.tracker_list[7]:
            tracking_algo = cv2.TrackerCSRT_create()
        else:
            tracking_algo = None

        return tracking_algo

    def multi_object_tracking_main(self):
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

        rect_list = list()
        color_list = list()

        while True:
            bbox = cv2.selectROI(image,False)
            rect_list.append(bbox)
            color_list.append((randint(64,255),randint(64,255),randint(64,255)))
            print('press <SPACE> or <ENTER> to confirm the selection')
            print('press <q> to stop selecting and start multitracking')
            print('press <any key> to select another box')

            if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        print('Selected co-ordinates...:',rect_list)
        multi_tracker_algo = cv2.MultiTracker_create()

        for each_box in rect_list:
            multi_tracker_algo.add(self.create_tracker(self.tracker_type),image,each_box)

        image_list = list()

        while vid_frame.isOpened():
            ok,image= vid_frame.read()
            if not ok:
                break
            ok,boxes = multi_tracker_algo.update(image)

            for(i , n_box) in enumerate(boxes):
                pts1 = (int(n_box[0]),int(n_box[1]))
                pts2 = (int(n_box[0]+n_box[2]),int(n_box[1]+n_box[3]))
                cv2.rectangle(image,pts1,pts2,color_list[i],2,1)

            cv2.putText(image,self.tracker_type,(50,20),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,0),2)
            cv2.imshow('MultiTracker',image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        vid_frame.release()
        cv2.destroyAllWindows()

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
    objTrack = MultiObjectTrackingClass(input_path, tracker_index = 6)
    objTrack.multi_object_tracking_main()

