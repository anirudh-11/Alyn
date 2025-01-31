""" Deskews file after getting skew angle """
import optparse
import numpy as np
import matplotlib.pyplot as plt

from skew_detect import SkewDetect
from skimage import io
from skimage.transform import rotate
import glob
import os


class Deskew:

    def __init__(self, input_file, display_image, output_file, r_angle):

        self.input_file = input_file
        self.display_image = display_image
        self.output_file = output_file
        self.r_angle = r_angle
        self.skew_obj = SkewDetect(self.input_file)

    def deskew(self, input_file = None):

        if(input_file):
          img = io.imread(input_file)
        else:
          img = io.imread(self.input_file)

        res = self.skew_obj.process_single_file()
        angle = res['Estimated Angle']

        if angle >= 0 and angle <= 90:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -45 and angle < 0:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -90 and angle < -45:
            rot_angle = 90 + angle + self.r_angle

        rotated = rotate(img, rot_angle, resize=True)

        if self.display_image:
            self.display(rotated)

        if self.output_file:
            self.saveTemp(rotated*255)
        return(res, rotated*255)

    def saveImage(self, img):
        path = self.skew_obj.check_path(self.output_file)
        os.remove("temp.jpg")
        io.imsave(path, img.astype(np.uint8))

    def saveTemp(self, img):
      path = "temp.jpg"
      io.imsave(path, img.astype(np.uint8))


    def display(self, img):

        plt.imshow(img)
        plt.show()

    def run(self):

        if self.input_file:
            res_p, rotated = self.deskew()
            res_c, rotated = self.deskew(input_file = "temp.jpg")
            count = 1
            while(res_p["Estimated Angle"] != res_c["Estimated Angle"]):
              res_p = res_c
              res_c, rotated = self.deskew(input_file = "temp.jpg")
              count += 1
              print(count)
            self.saveImage(rotated)
if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option(
        '-i',
        '--input',
        default=None,
        dest='input_file',
        help='Input file name')
    parser.add_option(
        '-d', '--display',
        default=None,
        dest='display_image',
        help="display the rotated image")
    parser.add_option(
        '-o', '--output',
        default=None,
        dest='output_file',
        help='Output file name')
    parser.add_option(
        '-r', '--rotate',
        default=0,
        dest='r_angle',
        help='Rotate the image to desired axis',
        type=int)
    parser.add_option(
        '-f', '--file',
        default= None,
        dest='file',
        help='Given Input and Output is Directory or not')
    options, args = parser.parse_args()
    if(options.file == "Yes"):
      path = glob.glob(options.input_file + "/*.jpg")
      path.extend(glob.glob(options.input_file + "/*.jpeg"))
      path.extend(glob.glob(options.input_file + "/*.png"))
      for inp_file in path:
        f_name = inp_file.split("/")[-1]
        out_file = os.path.join(options.output_file, f_name)
        deskew_obj = Deskew(
          inp_file,
          options.display_image,
          out_file,
          options.r_angle)
        deskew_obj.run()
    else:
      deskew_obj = Deskew(
          options.input_file,
          options.display_image,
          options.output_file,
          options.r_angle)

      deskew_obj.run()
