from multiprocessing_utils import process_segment, parallel_processing
import cv2 as cv

if __name__ == "__main__":
    # Example image split into segments
    image = cv.imread("test_image.jpg")
    segments = [image[:, i:i + 100] for i in range(0, image.shape[1], 100)]

    # Test parallel processing with inversion
    results = parallel_processing(segments, process_segment)

    # Combine results
    processed_image = cv.hconcat(results)
    cv.imshow("Processed Image", processed_image)
    cv.waitKey(0)
    cv.destroyAllWindows()
