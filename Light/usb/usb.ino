#include <FastLED.h>

#define NUM_LEDS    96
#define BRIGHTNESS  255
#define LED_TYPE    WS2801
#define COLOR_ORDER RGB

// For led chips like WS2812, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define DATA_PIN 11
#define CLOCK_PIN 13

CRGB leds[NUM_LEDS];

/**
 * Angabe, ob Animatation angezeigt werden soll
 */
static int animationOn = 0;

/**
 * Beeinhaltet die einzelnen Emotionen
 */
typedef enum {
    NONE = 0, NEUTRAL, HAPPY, SAD, ANGRY, DISGUSTED, FEARFUL, SURPRISED
} Emotion;

static Emotion emotion = NONE;

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
    
    leds[random(NUM_LEDS)] = CRGB::Red;
        // Randomly fade the LEDs
    for (int j = 0; j < NUM_LEDS; j++)
            leds[j] = leds[j].fadeToBlackBy(64);
    delay(100);       
}

void setup() {
  Serial.begin(9600);
// put your setup code here, to run once:
FastLED.addLeds<LED_TYPE, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );

FastLED.setBrightness(  BRIGHTNESS );

}

static void illuminateNeutral() {
    if (animationOn) {
        DrawComet();
    }
    else {
        fill_solid(leds, NUM_LEDS, CRGB(138, 30, 0));
    }
    FastLED.show();
}

static void illuminateHappy() {
    if (animationOn) {
        DrawComet();
    }
    else {
        fill_solid(leds, NUM_LEDS, CRGB(224, 80, 0));
    }
    FastLED.show();
}

static void illuminateSad() {
    if (animationOn) {
        DrawComet();
    }
    else {
        fill_solid(leds, NUM_LEDS, CRGB(80, 0, 224));
    }
    FastLED.show();
}

static void illuminateAngry() {
    if (animationOn) {
        DrawComet();
    }
    else {
        fill_solid(leds, NUM_LEDS, CRGB(224, 0, 0));
    }
    FastLED.show();
}

static void illuminateDisgusted() {
    if (animationOn) {
        DrawComet();
    }
    else {
        fill_solid(leds, NUM_LEDS, CRGB(180, 0, 50));
    }
    FastLED.show();
}

static void illuminateFearful() {
    if (animationOn) {
        DrawComet();
    }
    else {
        fill_solid(leds, NUM_LEDS, CRGB(0, 150, 20));
    }
    FastLED.show();
}

static void illuminateSurprised() {
    if (animationOn) {
        DrawComet();
    }
    else {
        fill_solid(leds, NUM_LEDS, CRGB(50, 50, 120));
    }
    FastLED.show();
}

void loop() {
  //if (Serial.available()) {
        /* TODO korrektes Einlesen */
        char temp = Serial.read();
        if (temp == 'F') {
          animationOn = 0;
        }
        else if (temp == 'T') {
          animationOn = 1;
        }
        else {
          temp = temp - '0';
        }
        Serial.println(temp);
    if ((emotion != temp) && (temp >= 0) && (temp < 8)) {
      
      emotion = temp;
    
    }
    switch(emotion) {
      case NONE:
            FastLED.clear();
            FastLED.show();
            break;
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
        default:
            break;
    }

}
