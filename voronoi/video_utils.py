#!/bin/env python

# Extract frames from video
# python ./video_utils.py -action=extract video.mp4 frames

# Join

import argparse
import cv2
import glob
import numpy as np
import os


def extract_frames(video, frames_path):
    vidcap = cv2.VideoCapture(video)
    success,image = vidcap.read()
    count = 0

    if not os.path.isdir(frames_path):
        os.mkdir(frames_path)

    while success:
        cv2.imwrite("{}/{}.png".format(frames_path,count), image)     # save frame as PNG file
        success,image = vidcap.read()
        print ('Read a new frame: ', count)
        count += 1

def join_frames(frames_path, output, fps):
    if not os.path.isdir(frames_path):
        print("'{}' frames path doesn't exist".format(frames_path))
        return
    frames = glob.glob('{}/*.png'.format(frames_path))
    print(frames)
    img = cv2.imread(frames[0])
    height, width, layers = img.shape
    size = (width,height)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    out = cv2.VideoWriter(output, fourcc, fps * 1.0, size)

    for count in range(0,len(frames)):
        print("Joining frame: {}".format(count))
        filename = "{}/anim_{}.png".format(frames_path,count)
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        out.write(img)

    out.release()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-action", default="extract", help="extract or join video frames")
    parser.add_argument("-fps", default=30, help="frames per second (integer)")
    parser.add_argument("video", default="video.mp4", help="input or output video path")
    parser.add_argument("frames_path", default="frames", help="frames path path")

    args = parser.parse_args()
    if args.action == 'extract':
        extract_frames(args.video, args.frames_path)
    elif args.action == 'join':
        join_frames(args.frames_path, args.video, int(args.fps))
    else:
        parser.print_help()