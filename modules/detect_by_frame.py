import numpy as np
import supervision as sv
# from tqdm import tqdm
from modules import dataframe
from stqdm import stqdm

def detect_video(VIDEO_PATH, TARGET_PATH, model,CONFIDENCE):
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()


    video_info = sv.VideoInfo.from_video_path(VIDEO_PATH)

    text_scale = sv.calculate_optimal_text_scale(video_info.resolution_wh)

    tracker = sv.ByteTrack()

    frame_generator = sv.get_video_frames_generator(VIDEO_PATH)

    start_point = sv.Point(0, video_info.height*(3/4))
    end_point = sv.Point(video_info.width, video_info.height*(3/4))

    line_zone = sv.LineZone(start=start_point, end=end_point)


    line_annotator = sv.LineZoneAnnotator(color=sv.Color.GREEN,
                                        text_scale=text_scale,
                                        custom_in_text="OUT",
                                        custom_out_text="IN")



    datas = 'Total Harga'
    t_price=0

    text_anchor = sv.Point(x=50, y=50)


    smoother = sv.DetectionsSmoother()

    with sv.VideoSink(target_path=TARGET_PATH, video_info=video_info) as sink:
        for frame in stqdm(frame_generator, total=video_info.total_frames):
                # run inference on the frame
                result = model(frame)[0]


                # convert the detections to a supervision detections object.
                detections = sv.Detections.from_ultralytics(result)
                detections = detections[detections.confidence > CONFIDENCE]



                # update detections with tracker id's
                detections = tracker.update_with_detections(detections)
                detections = smoother.update_with_detections(detections)

                # update with smmoter


                labels = [
                    f"{class_id} {confidence:.2f}"
                    for class_id, confidence
                    in zip(dataframe.get_name_by_class(detections.class_id), detections.confidence)]


                b_annotated_frame = bounding_box_annotator.annotate(
                    scene=frame.copy(), detections=detections)
                l_annotated_frame = label_annotator.annotate(
                    scene=b_annotated_frame.copy(), detections=detections, labels=labels)


                crossed_in, crossed_out = line_zone.trigger(detections)
                if np.any(crossed_in) or np.any(crossed_out):
                    detections_crossed_out = detections[crossed_out]
                    for cls_id in detections_crossed_out.class_id:
                        t_price=dataframe.total_Price(cls_id, t_price)
                        datas = f'Rp {str(t_price)}'

                l_annotated_frame = sv.draw_text(scene=l_annotated_frame.copy(), text=datas, text_anchor=text_anchor, text_thickness=2, text_color=sv.Color.WHITE)

                annotated_frame = line_annotator.annotate(frame=l_annotated_frame.copy(), line_counter=line_zone)

                # save the annotated frame to the video sink.
                sink.write_frame(frame=annotated_frame)