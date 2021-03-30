
# Define the wheel function to interpolate between different hues.
def wheel(pos):
    value = (0,0,0)
    if pos < 85:
        value = (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        value = (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        value = (0, pos * 3, 255 - pos * 3)
    return value

def rainbow_cycle(leds, wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(n_leds):
            leds[i] = wheel(((i * 256 // n_leds) + j) % 256) 
        leds.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_colors(leds, wait=0.05):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(n_leds):
            leds[i] = wheel(((256 // n_leds + j)) % 256) 
        leds.show()
        if wait > 0:
            time.sleep(wait)
 
def brightness_decrease(leds, wait=0.01, step=1):
    for j in range(int(256 // step)):
        for i in range(n_leds):
            value = leds[i]
            r = int(max(0, value[0] - step))
            g = int(max(0, value[1] - step))
            b = int(max(0, value[2] - step))
            leds[i] = ( r, g, b )
        leds.show()
        if wait > 0:
            time.sleep(wait)
 
def blink_color(leds, blink_times=5, wait=0.5, color=(255,0,0)):
    for i in range(blink_times):
        # blink two times, then wait
        clear()
        for j in range(2):
            for k in range(n_leds):
                leds[k] = color
            leds.show()
            time.sleep(0.08)
            clear()
            leds.show()
            time.sleep(0.08)
        time.sleep(wait)
 
def appear_from_back(leds, color=(255, 0, 0)):
    pos = 0
    for i in range(n_leds):
        for j in reversed(range(i, n_leds)):
            clear()
            # first set all pixels at the begin
            for k in range(i):
                leds[k] = color
            # set then the pixel at position j
            leds[j] = color
            leds.show()
            time.sleep(0.02)
            
# a random color 0 -> 224
def random_color():
    return random.randrange(0, 7) * 32
   
