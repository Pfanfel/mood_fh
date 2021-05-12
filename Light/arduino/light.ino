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


#define NUM_SPARKS 40 // max number

CRGB leds[NUM_LEDS];


/**
   Angabe, ob Animatation angezeigt werden soll
*/
static int animationOn = 0;

uint16_t frame = 0;      //I think I might be able to move this variable to the void loop() scope and save some CPU
uint16_t animateSpeed = 100;            //Number of frames to increment per loop
uint8_t  animation = 10;    //Active animation
uint8_t brightness = 50;

uint8_t paletteIndex = 0;

CRGBPalette16  lavaPalette = CRGBPalette16(
                               CRGB::DarkRed,  CRGB::Maroon,   CRGB::DarkRed,  CRGB::Maroon,
                               CRGB::DarkRed,  CRGB::Maroon,   CRGB::DarkRed,  CRGB::DarkRed,
                               CRGB::DarkRed,  CRGB::DarkRed,  CRGB::Red,      CRGB::Orange,
                               CRGB::White,    CRGB::Orange,   CRGB::Red,      CRGB::DarkRed
                             );

DEFINE_GRADIENT_PALETTE( Sunset_Real_gp ) {
  0, 120,  0,  0,
  22, 179, 22,  0,
  51, 255, 104,  0,
  85, 167, 22, 18,
  135, 100,  0, 103,
  198,  16,  0, 130,
  255,   0,  0, 160
};

CRGBPalette16 myPal = Sunset_Real_gp;
const int maxPos = (NUM_LEDS - 1) * 128;

/**
   Beeinhaltet die einzelnen Emotionen
*/
typedef enum {
  NONE = 0, NEUTRAL, HAPPY, SAD, ANGRY, DISGUSTED, FEARFUL, SURPRISED
} Emotion;

static Emotion emotion = NONE;

static void drawFirework() {

int sparkPos[NUM_SPARKS] ;
int sparkVel[NUM_SPARKS] ;
int sparkHeat[NUM_SPARKS];
byte nSparks = 30;
  
  EVERY_N_MILLIS(30) {
    // Shoot
      if (random(1100) < 10) {

    int flarePos = random(20, NUM_LEDS - 20);
    
    // initialize sparks
    for (int x = 0; x < nSparks; x++) {
      sparkPos[x] = flarePos << 7;
      sparkVel[x] = random16(0, 5120) - 2560; // velocitie original -1 o 1 now -255 to + 255
      word sph = abs(sparkVel[x]) << 2;
      if (sph > 2550) sph = 2550; // set heat before scaling velocity to keep them warm heat is 0-500 but then clamped to 255
      sparkHeat[x] = sph ;
    }
    sparkHeat[0] = 5000; // this will be our known spark
  }
  }
  EVERY_N_MILLIS(15) {
    // Spark
    for (int x = 0; x < nSparks; x++) {
    sparkPos[x] = sparkPos[x] + (sparkVel[x] >> 5); // adjust speed of sparks here
    sparkPos[x] = constrain(sparkPos[x], 0, maxPos);
    sparkHeat[x] = scale16(sparkHeat[x], 64000); // adjust speed of cooldown here

   CRGB color;
   color = ColorFromPalette(ForestColors_p, scale16(sparkHeat[x], 6600));

    leds[sparkPos[x] >> 7] += color;
  }
  }

  delay(5);
  fadeToBlackBy(leds, NUM_LEDS, 80);
}

static void drawForwardBackward() {
  // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
  uint8_t BeatsPerMinute = 62;
  uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
  for ( int i = 0; i < NUM_LEDS; i++) { //9948
    leds[i] = ColorFromPalette(lavaPalette, (i * 2), beat - (i * 10));
  }
}

static void drawSunset() {
  fill_palette(leds, NUM_LEDS, paletteIndex, 255 / NUM_LEDS, myPal, 255, LINEARBLEND);

  EVERY_N_MILLISECONDS(10) {
    paletteIndex++;
  }
}

static void drawWave() {
  FastLED.clear();
  uint8_t value;
  for (uint8_t i = 0; i < NUM_LEDS; i++)
  {
    value = (sin16(frame + ((65536 / NUM_LEDS) * i)) + (65536 / 2)) / 256;
    if (value >= 0) {
      leds[i] += CHSV(25, 255, value);
    }
  }
}


static void drawTwinkles() {
  // random colored speckles that blink in and fade smoothly
  fadeToBlackBy( leds, NUM_LEDS, 7);
  int pos = random16(NUM_LEDS);
  leds[pos] += CHSV( 130 + random8(90), 200, 255);
  delay(30);
}

static void drawGlitter() {
  // built-in FastLED rainbow, plus some random sparkly glitter

  fadeToBlackBy( leds, NUM_LEDS, 15);
  int pos = random16(NUM_LEDS);
  leds[pos] += CRGB::White;
  delay(20);
}

static void drawComet()
{
  const byte fadeAmt = 128;
  const int cometSize = 30;
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

  delay(20);
}

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  FastLED.addLeds<LED_TYPE, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );

  FastLED.setBrightness(  BRIGHTNESS );

}

static void illuminateNeutral() {
  if (animationOn) {
    drawWave();
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB(138, 30, 0));
  }
  FastLED.show();
  frame += animateSpeed;
}

static void illuminateHappy() {
  if (animationOn) {
    drawComet();
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB(224, 80, 0));

  }
  FastLED.show();
}

static void illuminateSad() {
  if (animationOn) {
    drawTwinkles();
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB(80, 0, 224));
  }
  FastLED.show();
}

static void illuminateAngry() {
  if (animationOn) {
    drawForwardBackward();
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB(224, 0, 0));
  }
  FastLED.show();
}

static void illuminateDisgusted() {
  if (animationOn) {
    drawSunset();
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB(180, 0, 50));
  }
  FastLED.show();
}

static void illuminateFearful() {
  if (animationOn) {
    drawFirework();
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB(0, 150, 20));
  }
  FastLED.show();
}

static void illuminateSurprised() {
  if (animationOn) {
    drawGlitter();
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB(50, 50, 120));
  }
  FastLED.show();
}

void loop() {
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

  if ((emotion != temp) && (temp >= 0) && (temp < 8)) {

    emotion = temp;

  }
  switch (emotion) {
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
