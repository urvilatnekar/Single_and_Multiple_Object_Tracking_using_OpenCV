from ML_Pipeline import SingleObjectTracking, MultiObjectTracking


class EngineClass:
    """
    This class defines the Engine to run both SOT and MOT.
    The constructor of the class takes two parameters
    """
    def __init__(self, input_video, tracker_index=7):
        # param 1: input video path
        self.input_video = input_video
        # param 2: tracker type
        self.tracker_index = tracker_index

    def main(self, type_="multi_object"):
        # the main function calls the SOT or MOT based on the type of parameter passed
        # if type_ passed is "single_object", SOT will be called, else MOT will be called
        if type_ == "single_object":
            singleObjTrack = SingleObjectTracking.SingleObjectTrackingClass(self.input_video, tracker_index=7)
            singleObjTrack.single_object_tracking_main()
        else:
            objTrack = MultiObjectTracking.MultiObjectTrackingClass(self.input_video, tracker_index=7)
            objTrack.multi_object_tracking_main()


if __name__ == '__main__':
    # input path defines the path of the input file for the object tracking
    # tracker_index is the index for element from the list: ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    input_file = '../InputFiles/car_driving.mp4'
    tracker_list = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    # we have selected the CSRT tracker(index=7)
    tracker_type_index = 7
    eng_obj = EngineClass(input_file, tracker_index=tracker_type_index)
    eng_obj.main()
