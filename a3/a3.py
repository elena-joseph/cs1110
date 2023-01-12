"""
Functions for Assignment A3

This file contains the functions for the assignment. You should replace the
stubs with your own implementations.

Carly Hu (ch862) and Elena Joseph (esj34)
October 8th, 2021
"""
import introcs
import math


def complement_rgb(rgb):
    """
    Returns the complement of color rgb.

    Parameter rgb: the color to complement
    Precondition: rgb is an RGB object
    """
    # THIS IS WRONG.  FIX IT
    red_comp = 255 - rgb.red
    green_comp = 255 - rgb.green
    blue_comp = 255 - rgb.blue

    return introcs.RGB(red_comp, green_comp, blue_comp)


def str5(value):
    """
    Returns value as a string, but expanded or rounded to be exactly 5
    characters.

    The decimal point counts as one of the five characters.

    Examples:
        str5(1.3546)  is  '1.355'.
        str5(21.9954) is  '22.00'.
        str5(21.994)  is  '21.99'.
        str5(130.59)  is  '130.6'.
        str5(130.54)  is  '130.5'.
        str5(1)       is  '1.000'.

    Parameter value: the number to conver to a 5 character string.
    Precondition: value is a number (int or float), 0 <= value <= 360.
    """
    # Remember that the rounding takes place at a different place depending
    # on how big value is. Look at the examples in the specification.

    value = float(value)
    if 10>value>=0:
        x=round(value,3)
    elif 100>value>=10:
        x=round(value,2)
    elif 360>value>=10:
        x=round(value,1)
    x = str(x)

    if len(x)==3:
        x = x+'00'
    elif len(x)==4:
        x= x+'0'
    else:
        x=x
    return x


def str5_cmyk(cmyk):
    """
    Returns the string representation of cmyk in the form "(C, M, Y, K)".

    In the output, each of C, M, Y, and K should be exactly 5 characters long.
    Hence the output of this function is not the same as str(cmyk)

    Example: if str(cmyk) is

          '(0.0,31.3725490196,31.3725490196,0.0)'

    then str5_cmyk(cmyk) is '(0.000, 31.37, 31.37, 0.000)'. Note the spaces
    after the commas. These must be there.

    Parameter cmyk: the color to convert to a string
    Precondition: cmyk is an CMYK object.
    """

    c = str5(cmyk.cyan)
    m = str5(cmyk.magenta)
    y = str5(cmyk.yellow)
    k = str5(cmyk.black)

    return '(' + c + ', ' + m + ', ' + y + ', ' + k + ')'


def str5_hsl(hsl):
    """
    Returns the string representation of hsl in the form "(H, S, L)".

    In the output, each of H, S, and L should be exactly 5 characters long.
    Hence the output of this function is not the same as str(hsv)

    Example: if str(hsl) is

          '(0.0,0.313725490196,0.5)'

    then str5_hsv(hsl) is '(0.000, 0.314, 0.500)'. Note the spaces after the
    commas. These must be there.

    Parameter hsl: the color to convert to a string
    Precondition: hsl is an HSL object.
    """
    h = str5(hsl.hue)
    s = str5(hsl.saturation)
    l = str5(hsl.lightness)

    return '(' + h + ', ' + s + ', ' + l + ')'


def rgb_to_cmyk(rgb):
    """
    Returns a CMYK object equivalent to rgb, with the most black possible.

    Formulae from https://www.rapidtables.com/convert/color/rgb-to-cmyk.html

    Parameter rgb: the color to convert to a CMYK object
    Precondition: rgb is an RGB object
    """
    # The RGB numbers are in the range 0..255.
    # Change the RGB numbers to the range 0..1 by dividing them by 255.0.
    r = rgb.red/255.0
    g = rgb.green/255.0
    b = rgb.blue/255.0
    k = 1-max(r, g, b)

    if k ==1:
        c = 0
        m = 0
        y = 0

    else:
        c = (1-r-k) / (1-k)
        m = (1-g-k) / (1-k)
        y = (1-b-k) / (1-k)

    c = c*100
    m = m*100
    y = y*100
    k= k*100

    return introcs.CMYK(c,m,y,k)


def cmyk_to_rgb(cmyk):
    """
    Returns an RGB object equivalent to cmyk

    Formulae from https://www.rapidtables.com/convert/color/cmyk-to-rgb.html

    Parameter cmyk: the color to convert to a RGB object
    Precondition: cmyk is an CMYK object.
    """
    # The CMYK numbers are in the range 0.0..100.0. Deal with them in the
    # same way as the RGB numbers in rgb_to_cmyk()
    c = cmyk.cyan/100
    m = cmyk.magenta/100
    y = cmyk.yellow/100
    k = cmyk.black/100

    r = (1-c)*(1-k)
    g = (1-m)*(1-k)
    b = (1-y)*(1-k)

    r = round(r * 255)
    g = round(g * 255)
    b = round(b * 255)

    return introcs.RGB(r,g,b)


def rgb_to_hsl(rgb):
    """
    Return an HSL object equivalent to rgb

    Formulae from https://en.wikipedia.org/wiki/HSL_and_HSV

    Parameter rgb: the color to convert to a HSL object
    Precondition: rgb is an RGB object
    """
    r = rgb.red/255.0
    g = rgb.green/255.0
    b = rgb.blue/255.0



    max1 = max(r, g, b)
    min1 = min(r, g, b)

    if max1==min1:
        h = 0
    elif max1 == r and (g >= b):
        h = 60.0*(g-b)/(max1-min1)
    elif max1 == r and (g < b):
        h = 60.0*(g-b/(max1-min1)) + 360.0
    elif max1 == g:
        h = 60.0*(b-r)/(max1-min1) + 120.0
    elif max1 == b:
        h = 60.0*(r-g)/(max1-min1) + 240.0

    l = (max1 + min1)/2

    if l == 0 or l == 1:
        s = 0
    else:
        s = (max1 - l)/(min(l, 1-l))

    return introcs.HSL(h,s,l)


def hsl_to_rgb(hsl):
    """
    Returns an RGB object equivalent to hsl

    Formulae from https://en.wikipedia.org/wiki/HSL_and_HSV

    Parameter hsl: the color to convert to a RGB object
    Precondition: hsl is an HSL object.
    """

    h_inital = math.floor(hsl.hue/60)
    f = hsl.hue/60-h_inital
    c = min(hsl.lightness, 1-hsl.lightness)*hsl.saturation
    p = hsl.lightness + c
    q = hsl.lightness - c
    u = hsl.lightness - (1-(2*f))*c
    v = hsl.lightness + (1-(2*f))*c

    if h_inital == 0:
        r = p
        g = u
        b = q
    elif h_inital == 1:
        r = v
        g = p
        b = q
    elif h_inital == 2:
        r = q
        g = p
        b = u
    elif h_inital == 3:
        r = q
        g = v
        b = p
    elif h_inital == 4:
        r = u
        g = q
        b = p
    elif h_inital == 5:
        r = p
        g = q
        b = v

    r = r * 255
    g = g * 255
    b = b * 255

    r = int(round(r,0))
    g = int(round(g,0))
    b = int(round(b,0))

    return introcs.RGB(r,g,b)


def contrast_value(value,contrast):
    """
    Returns value adjusted to the "sawtooth curve" for the given contrast

    At contrast = 0, the curve is the normal line y = x, so value is unaffected.
    If contrast < 0, values are pulled closer together, with all values
    collapsing to 0.5 when contrast = -1.  If contrast > 0, values are pulled
    farther apart, with all values becoming 0 or 1 when contrast = 1.

    Parameter value: the value to adjust
    Precondition: value is a float in 0..1

    Parameter contrast: the contrast amount (0 is no contrast)
    Precondition: contrast is a float in -1..1
    """

    x = value
    c = contrast

    if c==1:
        if x>= 0.5:
            y=1
        else:
            y = 0

    elif c == -1:
        y = 0.5

    else:
        if x < (0.25 + 0.25*c):
            y = ((1-c)/(1+c))*x
        elif x > (0.75 - 0.25*c):
            y = ((1-c)/(1+c))*(x - (3-c)/4) +((3+c)/4)
        else:
            y = ((1+c)/(1-c))*(x - (1+c)/4) +((1-c)/4)

    return y


def contrast_rgb(rgb,contrast):
    """
    Applies the given contrast to the RGB object rgb

    This function is a PROCEDURE.  It modifies rgb and has no return value.
    It should apply contrast_value to the red, blue, and green values.

    Parameter rgb: the color to adjust
    Precondition: rgb is an RGB object

    Parameter contrast: the contrast amount (0 is no contrast)
    Precondition: contrast is a float in -1..1
    """

    r = rgb.red/255.0
    g = rgb.green/255.0
    b = rgb.blue/255.0

    r = contrast_value(r,contrast)
    g = contrast_value(g,contrast)
    b = contrast_value(b,contrast)

    r = r * 255
    g = g * 255
    b = b * 255

    rgb.red = int(round(r,0))
    rgb.green = int(round(g,0))
    rgb.blue = int(round(b,0))
