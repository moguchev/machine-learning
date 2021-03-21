from image_gen import generate_images, Path
import imutils
import cv2

WHITE = (255, 255, 255)
PX_SIZE = 2


def get_figure_type(contour):
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    if len(approx) == 3:
        figure = "Triangle"
    elif len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        figure = "Square" if 0.9 <= w / float(h) <= 1.1 else "Rectangle"
    elif len(approx) == 5:
        figure = "Pentagon"
    elif len(approx) == 6:
        figure = "Hexagon"
    else:
        figure = "Circle"
    return figure


def process_images(img_count):
    for i in range(img_count):
        image = cv2.imread(f"sources/test{i}.jpg")
        thresh = cv2.threshold(
            cv2.GaussianBlur(
                cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (5, 5), 0),
            60, 255, cv2.THRESH_BINARY)[1]
        # Finding contours
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        # Detecting shape of each contour
        for ctr in contours:
            moments = cv2.moments(ctr)
            cv2.drawContours(image, [ctr.astype("int")], -1, WHITE, PX_SIZE)  # контур
            figure_type = get_figure_type(ctr)
            cv2.putText(image, figure_type,
                        (int((moments["m10"] / moments["m00"] - 20)),
                         int((moments["m01"] / moments["m00"]))),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, PX_SIZE)

        Path("results").mkdir(parents=True, exist_ok=True)
        cv2.imwrite(f"results/result{i}.jpg", image)


if __name__ == '__main__':
    n = int(input("Number of images: "))
    generate_images(n)
    process_images(n)
