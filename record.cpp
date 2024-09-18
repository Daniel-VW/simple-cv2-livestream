#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    std::string stream_url = "http://192.168.30.142:8443";

    cv::VideoCapture cap(stream_url);
    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open video stream." << std::endl;
        return -1;
    }

    int frame_width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    int frame_height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    cv::VideoWriter video_writer("output.mp4", cv::VideoWriter::fourcc('m', 'p', '4', 'v'), 20.0, cv::Size(frame_width, frame_height));

    if (!video_writer.isOpened()) {
        std::cerr << "Error: Could not open the video file for writing." << std::endl;
        return -1;
    }

    while (true) {
        cv::Mat frame;
        bool ret = cap.read(frame);

        if (!ret) {
            std::cerr << "Failed to grab frame." << std::endl;
            break;
        }
        video_writer.write(frame);

        cv::imshow("Live Stream", frame);

        if (cv::waitKey(1) == 'q') {
            break;
        }
    }

    cap.release();
    video_writer.release();
    cv::destroyAllWindows();

    return 0;
}
