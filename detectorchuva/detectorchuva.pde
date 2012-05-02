#define SAMPLES 10
//Numero de gotas maximo estimado a partir do seguinte racioncinio:
/*Uma chuva violenta chega a indice de 50 mm (5 cm) pluviometricos, portanto para
uma area com raio de 4.25 cm (aprox. 57 cm2) o volume sera de cerca de 285 cm3
o que precisaria de 2519.9 gotas de raio medio de 3mm de raio c/ volume de 0.113 cm3.
Arredondando chegamos a 26200 gotas por hora a cada 57 cm2 numa chuva intensa.
*/
#define MAXDPH 25200

float area_membrana_cm2 = 57; //Membrana circular c/ 4.25 cm de raio
float volume_gota_ml = 0.1131; //gota media c/ 3mm de raio

const int ledPin = 13;

//Shift Register pins
const int latchPin = 8;
const int clockPin = 12;
const int dataPin = 11;

//Display Cathodes
const int dispPin0 = 3;
const int dispPin1 = 4;
const int dispPin2 = 5;
const int dispPin3 = 6;

int dph = 0, sensorValue;
float mm_de_chuva;

int last[SAMPLES + 10];
unsigned long lasttime = 0;
unsigned long i;

void setup()
{
  	Serial.begin(9600);
	pinMode(latchPin, OUTPUT);
	pinMode(dataPin, OUTPUT);
	pinMode(clockPin, OUTPUT);
	pinMode(dispPin0, OUTPUT);
	pinMode(dispPin1, OUTPUT);
	pinMode(dispPin2, OUTPUT);
	pinMode(dispPin3, OUTPUT);
        memset(last, 0, sizeof(last));
}

void loop()
{
	digitalWrite(ledPin, LOW);
	sensorValue = analogRead(A5);
	last[i % SAMPLES] = sensorValue;
        int sum = 0;
        for(int j = 1; j < SAMPLES; j++){
          sum += last[(i - 10) % SAMPLES] - last[(i - j - 10) % SAMPLES];
        }

        //if(sum > 100) Serial.println(sum);
        //Verify if is a heart beat
        //if(delta * delta > 30) Serial.println(delta);
	if (3600000.0 / MAXDPH < millis() - lasttime && sum > 150) {
                //Turn on the led
		digitalWrite(ledPin, HIGH);
                unsigned long altualTime = millis();
                int delayMs = altualTime - lasttime;
                //Calculate the frequency in drops per hour / frequency in dph = 1.0 / delay in ms * 3600000
		dph = 3600000.0 / delayMs;
                //Estimativa da altura que um frasco se encheria durante uma hora com a chuva permanecendo nesta intensidade
                mm_de_chuva = (sum - 100) / 1000.0 * dph * volume_gota_ml / area_membrana_cm2 * 10;
                Serial.print(mm_de_chuva);
                Serial.println(" mm.");
		lasttime = altualTime;
	}
	++i;
}
