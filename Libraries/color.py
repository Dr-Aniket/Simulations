
def color(number : int):
    ''' Color on a Circular Scale ''' 
    if int(number) == -1:
        return (255,255,255)        
    number = abs(int(number))
    if number >= 400:
        number = number - ( 300 * ((number-100)//300))
    r = 0
    g = 0
    b = 0
    if number <= 100:
        percent = number/100
        r = int(percent * 255)
    elif number > 100 and number <= 200:
        number = number - 100
        percent = number/100
        g = int(percent * 255)
        r = 255 - g

    elif number >200 and number <= 300:
        number = number - 200
        percent = number/100
        b = int(percent * 255)
        g = 255 - b
    elif number > 300 and number <= 400:
        number = number - 300
        percent = number/100
        r = int(percent * 255)
        b = 255 - r
    else:
        r = g = b = 255
    return (r,g,b)

