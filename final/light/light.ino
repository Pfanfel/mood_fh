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
  NONE = 0, ANGRY, DISGUSTED, FEARFUL, HAPPY, NEUTRAL, SAD, SURPRISED
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
static bool animationOn = false;

/**
 * Angabe, ob ANimation gewechselt wurde
 */
static volatile bool switched = false;

static uint16_t frame = 0;

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
 * Farbwerte fuer die Palette setzen
 */
DEFINE_GRADIENT_PALETTE( Angry_gp ) {
  0, 210, 11, 24,
  22, 255, 0,  0,
  51, 163, 6,  6,
  85, 121, 9, 9,
  135, 255,  61, 12,
  198,  255,  84, 0,
  255,  245,  229, 70
};

/**
 * Farbpalette fuer die Animation von Disgusted
 */
CRGBPalette16 disgustedPal = Sunset_gp;

/**
 * Farbpalette fuer die Animation von Angry
 */
CRGBPalette16 angryPal = Angry_gp;

/**
 * Farbpalette fuer die Animation von Fearful
 */
CRGBPalette16 fearfulPal = ForestColors_p;

/**
 * Wartet solange, bis die Zeit abgelaufen ist, oder die Animation beendet wird
 */
static void wait(uint8_t currDelay){
  unsigned long startMillis = millis();
  while ((millis() - startMillis < currDelay) && (!switched)) {
  }
  switched = false;
}

/*----------------------------Animation und Farbangaben---------------------------------*/

/**
 * Animiert die LEDs wellenfoermig.
 */
static void drawWave() {
  FastLED.clear();
  uint8_t value = 0;
  static const uint32_t MAX_VAL = 65536;
  
  /* LEDs durchlaufen und farbwert ermitteln */
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    /* Neuen Farbwert ermitteln */
    value = (sin16(frame + ((MAX_VAL / NUM_LEDS) * i)) + (MAX_VAL / 2)) / 256;
    
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
  static const uint16_t ANIMATE_SPEED = 100; 
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawWave();
  }
  else {
    /* LEDs auf angegebenen Farbwert setzen */
    fill_solid(leds, NUM_LEDS, CRGB(138, 30, 0));
  }
  FastLED.show();
  frame += ANIMATE_SPEED;
}

/**
 * Animiert die LEDs wie einen bunten Kometen mit Richtungswechsel.
 */
static void drawComet() {
  static const uint8_t FADE_AMOUNT = 128;
  static const uint8_t COMET_SIZE = 30;
  static const uint8_t DELTA_HUE = 4;

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
  wait(20);
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
  wait(d);
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
  /* Angabe der BPM zu denen die LEDs pulsieren */
  static const uint8_t BPM = 62;
  uint8_t beat = beatsin8(BPM, 64, 255);
  /* LEDs durchlaufen und Farbwert anpassen */
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    leds[i] = ColorFromPalette(angryPal, (i * 2), beat - (i * 10));
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

/**
 * Animiert die LEDs mit einem weichen Farbverlauf in den Farben eines Sonnenuntergangs.
 */
static void drawSunset() {
  static uint8_t disgustedPalIdx = 0;
  /* Aendert den Farbewert der LEDs zu der Farbe, die ueber den passenden Index der Palette erreicht wird */
  fill_palette(leds, NUM_LEDS, disgustedPalIdx, 255 / NUM_LEDS, disgustedPal, 255, LINEARBLEND);

  EVERY_N_MILLISECONDS(10) {
    /* Farbwert veraendern, in dem der Indes der Palette weiter gesetzt wird */
    disgustedPalIdx++;
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
 * Animiert die LEDs mit einer Hintergrundfarbe und zufaellig bewegten LEDs.
 */
static void drawBeatWave() {
  uint8_t outer = beatsin8(30, 0, NUM_LEDS-1);
  uint8_t outer1 = beatsin8(40, 0, NUM_LEDS-1);
  uint8_t outer2 = beatsin8(50, 0, NUM_LEDS-1);
  uint8_t outer3 = beatsin8(60, 0, NUM_LEDS-1);
  uint8_t outer4 = beatsin8(70, 0, NUM_LEDS-1);
     
  uint8_t wave1 = beatsin8(9, 0, 255);

  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = ColorFromPalette(fearfulPal, i+wave1, 255, LINEARBLEND); 
  }
  
  leds[outer] = CRGB::Aqua;
  leds[outer1] = CRGB::Aqua;
  leds[outer2] = CRGB::Aqua;
  leds[outer3] = CRGB::Aqua;
  leds[outer4] = CRGB::Aqua;
  
  nscale8(leds, NUM_LEDS, 200); 
} 


/**
 * Setzt die LEDs auf die angebenen Animation/Farbwerte fuer die Emotion Fearful
 */
static void illuminateFearful() {
  /* Pruefen, ob die LEDs animiert werden sollen */
  if (animationOn) {
    drawBeatWave();
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
    animationOn = false;
    switched = true;
  }
  /* Pruefen, ob die Animation angeschaltet wurde */
  else if (temp == 'T') {
    animationOn = true;
  }
  /* Umwandeln des gelesenen Zeichens in eine Zahl */
  else {
    temp = temp - '0';
  }

  /* Pruefen, ob die gespeicherte Zahl einer Emotion entspricht */
  if ((emotion != temp) && (temp >= 0) && (temp < 8)) {
    emotion = (Emotion) temp;
    switched = true;
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
