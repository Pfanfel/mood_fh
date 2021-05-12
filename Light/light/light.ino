#include <FastLED.h>

/* Anzahl der Leds */
#define NUM_LEDS    96

/* Angabe der Helligkeit */
#define BRIGHTNESS  255

/* Angabe des LED-Strips */
#define LED_TYPE    WS2801

/* Angabe der Farbwerte */
#define COLOR_ORDER RGB

/* Pin-Belegung zur "Ansteuerung" des LED-Strips */
/* (Master In Slave Out (MOSI) */
#define DATA_PIN 11

/* Serial Clock (SCK) */
#define CLOCK_PIN 13

/**
   Beeinhaltet die einzelnen Emotionen
*/
typedef enum {
  NONE = 0, NEUTRAL, HAPPY, SAD, ANGRY, DISGUSTED, FEARFUL, SURPRISED
} Emotion;

/**
 * Angabe der aktuellen Emotion
 */
static Emotion emotion = NONE;

/** 
 * Beinhaltet die Farbwerte dr einzelnen LEDs des Strips
 */
CRGB leds[NUM_LEDS];

/**
 * Angabe, ob Animatation angezeigt werden soll
 */
static uint8_t animationOn = 0;

uint16_t frame = 0;      //I think I might be able to move this variable to the void loop() scope and save some CPU
uint16_t animateSpeed = 100;            //Number of frames to increment per loop
uint8_t paletteIndex = 0;

/**
 * Farbwerte fuer die Palette setzen
 */
DEFINE_GRADIENT_PALETTE( Sunset_gp ) {
  0, 120,  0,  0,
  22, 179, 22,  0,
  51, 255, 104,  0,
  85, 167, 22, 18,
  135, 100,  0, 103,
  198,  16,  0, 130,
  255,   0,  0, 160
};

/**
 * Farbpalette fuer die Animation von Disgusted
 */
CRGBPalette16 disgustedPal = Sunset_gp;

/*----------------------------Animation und Farbangaben---------------------------------*/

/**
 * Animiert die LEDs wellenfoermig.
 */
static void drawWave() {
  FastLED.clear();
  uint8_t value = 0;
  
  /* LEDs durchlaufen und farbwert ermitteln */
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    /* Neuen Farbwert ermitteln */
    value = (sin16(frame + ((65536 / NUM_LEDS) * i)) + (65536 / 2)) / 256;
    
    /* Aktuelle LED auf Farbwert setzen, wenn dieser gueltig ist */
    if (value >= 0) {
      leds[i] += CHSV(25, 255, value);
    }
  }
}

/**
 * Setzt die LEDs auf die angebenen Animation/Farbwerte fuer die Emotion Neutral
 */
static void illuminateNeutral() {
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawWave();
  }
  else {
    /* LEDs auf angegebenen Farbwert setzen */
    fill_solid(leds, NUM_LEDS, CRGB(138, 30, 0));
  }
  FastLED.show();
  frame += animateSpeed;
}

/**
 * Animiert die LEDs wie einen bunten Kometen mit Richtungswechsel.
 */
static void drawComet() {
  #define FADE_AMOUNT 128
  #define COMET_SIZE 30
  #define DELTA_HUE 4

  static uint8_t hue = HUE_RED;
  static int dir = 1;
  static int pos = 0;

  /* Farbwert wird weiter gesetzt */
  hue += DELTA_HUE;
  /* Position wird weiter gesetzt */
  pos += dir;

  /* Pruefen, ob der Komet seine Richtung aendern soll */
  if (pos == (NUM_LEDS - COMET_SIZE) || pos == 0) {
    dir *= -1;
  }

  /* Farbwert der LEDs setzen */
  for (uint8_t i = 0; i < COMET_SIZE; i++) {
    leds[pos + i].setHue(hue);
  }

  /* Farbwert der LEDs zufaellig abdunkeln */
  for (uint8_t j = 0; j < NUM_LEDS; j++) {
    if (random(10) > 5) {
      leds[j] = leds[j].fadeToBlackBy(FADE_AMOUNT);
    }
  }
  delay(20);
}

/**
 * Setzt die LEDs auf die angebenen Animation/Farbwerte fuer die Emotion Happy
 */
static void illuminateHappy() {
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawComet();
  }
  else {
    /* LEDs auf angegebenen Farbwert setzen */
    fill_solid(leds, NUM_LEDS, CRGB(224, 80, 0));

  }
  FastLED.show();
}

/**
 * Animiert ein zufaelliges Funkeln der LEDs.
 * 
 * @param color Farbe der Funken
 * @param d delay Angabe
 * @param fadeAmount Angabe, um wieviel die leds abdunkeln
 */
static void drawTwinkles(CHSV color, uint8_t d, uint8_t fadeAmount) {
  /* Alle LEDs abdunkeln */
  fadeToBlackBy( leds, NUM_LEDS, fadeAmount);
  /* Zufaellige Position ermitteln */
  uint8_t pos = random16(NUM_LEDS);
  /* Farbwert der LED an der ermittelten Position setzen */
  leds[pos] += color;
  delay(d);
}

/**
 * Setzt die LEDs auf die angebenen Animation/Farbwerte fuer die Emotion Sad
 */
static void illuminateSad() {
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawTwinkles(CHSV(130 + random8(90), 200, 255), 30, 7);
  }
  else {
    /* LEDs auf angegebenen Farbwert setzen */
    fill_solid(leds, NUM_LEDS, CRGB(80, 0, 224));
  }
  FastLED.show();
}

/**
 * Animiert die LEDs als pulsierenden Ring, der sich vor und zurueck bewegt.
 */
static void drawForwardBackward() {
  // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
  #define BeatsPerMinute 62
  uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    leds[i] = ColorFromPalette(LavaColors_p, (i * 2), beat - (i * 10));
  }
}

/**
 * Setzt die LEDs auf die angebenen Animation/Farbwerte fuer die Emotion Angry
 */
static void illuminateAngry() {
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawForwardBackward();
  }
  else {
    /* LEDs auf angegebenen Farbwert setzen */
    fill_solid(leds, NUM_LEDS, CRGB(224, 0, 0));
  }
  FastLED.show();
}

static void drawSunset() {
  fill_palette(leds, NUM_LEDS, paletteIndex, 255 / NUM_LEDS, disgustedPal, 255, LINEARBLEND);

  EVERY_N_MILLISECONDS(10) {
    paletteIndex++;
  }
}

/**
 * Setzt die LEDs auf die angebenen Animation/Farbwerte fuer die Emotion Disgusted
 */
static void illuminateDisgusted() {
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawSunset();
  }
  else {
    /* LEDs auf angegebenen Farbwert setzen */
    fill_solid(leds, NUM_LEDS, CRGB(180, 0, 50));
  }
  FastLED.show();
}

/**
 * Animiert die LEDs explosionsartig.
 */
static void drawFirework() {

  /* max. Anzahl der Funken */
  #define NUM_SPARKS 48

  #define MAX_POS ((NUM_LEDS - 1) * 128)

  int sparkPos[NUM_SPARKS] ;
  int sparkVel[NUM_SPARKS] ;
  int sparkHeat[NUM_SPARKS];
  
  EVERY_N_MILLIS(30) {
    // Shoot
      if (random(1100) < 10) {

    int flarePos = random(20, NUM_LEDS - 20);
    
    // initialize sparks
    for (int x = 0; x < NUM_SPARKS; x++) {
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
    for (int x = 0; x < NUM_SPARKS; x++) {
    sparkPos[x] = sparkPos[x] + (sparkVel[x] >> 5); // adjust speed of sparks here
    sparkPos[x] = constrain(sparkPos[x], 0, MAX_POS);
    sparkHeat[x] = scale16(sparkHeat[x], 64000); // adjust speed of cooldown here

   CRGB color = ColorFromPalette(ForestColors_p, scale16(sparkHeat[x], 6600));

    leds[sparkPos[x] >> 7] += color;
  }
  }

  delay(5);
  fadeToBlackBy(leds, NUM_LEDS, 80);
}

/**
 * Setzt die LEDs auf die angebenen Animation/Farbwerte fuer die Emotion Fearful
 */
static void illuminateFearful() {
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawFirework();
  }
  else {
    /* LEDs auf angegebenen Farbwert setzen */
    fill_solid(leds, NUM_LEDS, CRGB(0, 150, 20));
  }
  FastLED.show();
}

/**
 * Setzt die LEDs auf die angebenen Animation/Farbwerte fuer die Emotion Surprised
 */
static void illuminateSurprised() {
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawTwinkles(CHSV(0,0,BRIGHTNESS), 20, 15);
  }
  else {
    /* LEDs auf angegebenen Farbwert setzen */
    fill_solid(leds, NUM_LEDS, CRGB(50, 50, 120));
  }
  FastLED.show();
}

/* ----------------------------------------------------------------------------- */

/**
 * Initialisiert die LEDs.
 */
void setup() {
  Serial.begin(9600);
  FastLED.addLeds<LED_TYPE, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
}

/**
 * Main-Loop
 * Sorgt dafuer, dass die LEDs veraendert werden koennen.
 */
void loop() {
  /* Lesen der Daten vom PI */
  char temp = Serial.read();

  /* Pruefen, ob die Animation ausgeschaltet wurde */
  if (temp == 'F') {
    animationOn = 0;
  }
  /* Pruefen, ob die Animation angeschaltet wurde */
  else if (temp == 'T') {
    animationOn = 1;
  }
  /* Umwandeln des gelesenen Zeichens in eine Zahl */
  else {
    temp = temp - '0';
  }

  /* Pruefen, ob die gespeicherte Zahl einer Emotion entspricht */
  if ((emotion != temp) && (temp >= 0) && (temp < 8)) {
    emotion = temp;
  }

  /* Je nach Emotion, Farbe oder Animation der LEDs anpassen */
  switch (emotion) {
    /* Keine Emotion -> LEDs aus */
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
