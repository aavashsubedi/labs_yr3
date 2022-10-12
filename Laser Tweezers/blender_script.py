# Blender tracking export to CSV
# Python script originally taken from:
# http://scummos.blogspot.cz/2012/11/blender-exporting-camera-tracking.html
# https://gist.github.com/anonymous/31c915d611f0a84e5d33
# Last edited by David Wei, University of Manchester, August 2016
import bpy
import csv
D = bpy.data


frameNums = True # include frame numbers in the csv file
relativeCoords = False # marker coords will be relative to the dimensions of the clip
filepath = "filename here"
markers = {}


for clip in D.movieclips:
    print('Clip {} found'.format(clip.name))
    if relativeCoords:
        width = 1
        height = 1
    else:
        width = clip.size[0]
        height = clip.size[1]
    for ob in clip.tracking.objects:
        print('Object {} found'.format(ob.name))
        for track in ob.tracks:
            fn = '{}_{}_tr_{}'.format(clip.name.split('.')[0], ob.name, track.name)
            markers[fn] = []
            print('track {} found'.format(track.name))
            for framenum in range(clip.frame_duration):
                markerAtFrame = track.markers.find_frame(framenum)
                if markerAtFrame:
                    coords = list(markerAtFrame.co.xy)
                    coords = [coords[0] * width, coords[1] * height]
                    markers[fn].append(coords)
                    
                    
for key, value in markers.items():
    
    print(key)
    filename = "{}{}{}".format(filepath, key, ".csv")
    open_data = open(filename, 'w', newline='')
    with open_data as writer:
        writer = csv.writer(writer, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        if frameNums:
# writer.writerow([key, "x", "y"])
            for i, data in enumerate(value):
                writer.writerow([i] + data)
        else:
# writer.writerow(["x", "y"])
            for data in value:
                writer.writerow(data)