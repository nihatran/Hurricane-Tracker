import csv
import turtle
import os


def graphical_setup():
    """Creates the Turtle and the Screen with the map background
       and coordinate system set to match latitude and longitude.

       :return: a tuple containing the Turtle and the Screen

    """
    import tkinter
    turtle.setup(965, 600)  # set size of window to size of map

    wn = turtle.Screen()

    # kludge to get the map shown as a background image,
    # since wn.bgpic does not allow you to position the image
    canvas = wn.getcanvas()
    turtle.setworldcoordinates(-90, 0, -17.66, 45)  # set the coordinate system to match lat/long

    map_bg_img = tkinter.PhotoImage(file="images/atlantic-basin.png")

    # additional kludge for positioning the background image
    # when setworldcoordinates is used
    canvas.create_image(-1175, -580, anchor=tkinter.NW, image=map_bg_img)

    t = turtle.Turtle()
    wn.register_shape("images/hurricane.gif")
    t.shape("images/hurricane.gif")

    return t, wn, map_bg_img


def track_storm(filename):
    """Animates the path of the storm.
    """
    (t, wn, map_bg_img) = graphical_setup()

    # initialize category and start
    category = ''
    start = 'yes'

    # open the file and create a dictionary for each row
    # column header is key, data in row is value
    with open(filename, 'r') as storm:
        reader = csv.DictReader(storm)

        # for each row in the file, obtain the latitude/longitude/wind and convert to float
        for row in reader:
            lat = float(row['Lat'])
            lon = float(row['Lon'])
            wind = float(row['Wind'])

            # ensure the turtle starts at the correct place
            if start == 'yes':
                t.hideturtle()
                t.penup()
                t.setx(lon)
                t.sety(lat)
                start = 'no'
            t.showturtle()

            # determining the category of the hurricane and changing pen color/width as needed
            # hurricane category from saffir-simpson hurricane scale on weather.gov
            if wind < 74:
                t.pencolor("white")
                t.width(1)
                category = ''
            elif wind >= 74 and wind <= 95:
                t.pencolor("blue")
                t.width(2)
                category = 1
            elif wind >= 96 and wind <= 110:
                t.pencolor("green")
                t.width(3)
                category = 2
            elif wind >= 111 and wind <= 129:
                t.pencolor("yellow")
                t.width(7)
                category = 3
            elif wind >= 130 and wind <= 156:
                t.pencolor("orange")
                t.width(11)
                category = 4
            elif wind >= 157:
                t.pencolor("red")
                t.width(15)
                category = 5

            # animating the hurricane and displaying the category
            t.goto(lon, lat)
            t.pendown()
            t.write(category)

    return wn, map_bg_img


def main():

    # getting the storm name from user
    user_storm = input('Enter name of storm: ')

    # getting the correct path separator based on platform and concatenating it with the 
    # data folder, where the csv files are located
    sep = os.sep
    file_location = 'data' + sep

    # determine if the given storm exists
    file_path = os.path.join(file_location)
    file_path += user_storm
    file_path += '.csv'

    # if the storm exists then call track_storm(), otherwise exit
    if os.path.exists(file_path):
        track_storm(file_path)
    else:
        print('Invalid storm name')
        exit()

    wn.exitonclick()


if __name__ == "__main__":
    t, wn, mapbg = graphical_setup()
    main()
