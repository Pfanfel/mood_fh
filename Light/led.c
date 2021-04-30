#include <FastLED.h>

// TODO Pins anpassen
#define LED_PIN     5
#define NUM_LEDS    96
#define BRIGHTNESS  255
#define LED_TYPE    WS2801
#define COLOR_ORDER RGB
CRGB leds[NUM_LEDS];

#define UPDATES_PER_SECOND 100

/**
 * Angabe, ob Animatation angezeigt werden soll
 */
static int animationOn = 1;

/**
 * Beeinhaltet die einzelnen Emotionen
 */
typedef enum {
    NEUTRAL, HAPPY, SAD, ANGRY, DISGUSTED, FEARFUL, SURPRISED
} Emotion;


static void DrawComet()
{
    const byte fadeAmt = 128;
    const int cometSize = 5;
    const int deltaHue  = 4;

    static byte hue = HUE_RED;
    static int iDirection = 1;
    static int iPos = 0;

    hue += deltaHue;

    iPos += iDirection;
    if (iPos == (NUM_LEDS - cometSize) || iPos == 0)
        iDirection *= -1;
    
    for (int i = 0; i < cometSize; i++)
        leds[iPos + i].setHue(hue);
    
    // Randomly fade the LEDs
    for (int j = 0; j < NUM_LEDS; j++)
        if (random(10) > 5)
            leds[j] = leds[j].fadeToBlackBy(fadeAmt);  

    delay(30);
}

void DrawTwinkle3()
{
    
    leds[random(NUM_LEDS)] = TwinkleColors[random(0, NUM_COLORS)];
        // Randomly fade the LEDs
    for (int j = 0; j < NUM_LEDS; j++)
            leds[j] = leds[j].fadeToBlackBy(64);
    delay(100);       
}



static void illuminateNeutral() {
    if (animationOn) {
        DrawComet();
    }
    else {
        fill_solid(leds, NUM_LEDS, CRGB:RED);
    }
}

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );
  FastLED.setBrightness(  BRIGHTNESS );

}

void loop() {
    if (Serial.available()) {}
        /* TODO korrektes Einlesen */
        Emotion emotion = (Serial.read() - '0');
        Serial.println("Emotion received");
        
        /*
            in Python dann:
            import serial
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            while 1: 
                if(ser.in_waiting >0):
                    line = ser.readline()
                    print(line) 
         */
        animationOn = Serial.read();
        //delay(2000);
    }
    /*---------------------------------*/
    switch(emotion) {
        case NEUTRAL:
            illuminateNeutral();
            break;
        case HAPPY:
            illuminateHappy();
            break;
        case SAD:
            illuminateSad();
            break;
        case ANGRY:
            illuminateAngry();
            break;
        case DISGUSTED:
            illuminateDisgusted();
            break;
        case FEARFUL:
            illuminateFearful();
            break;
        case SURPRISED:
            illuminateSurprised();
            break;
    }
}