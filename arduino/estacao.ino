#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

int sensorSoloPin = A0;
int valorSolo = 0;

void setup()
{
  Serial.begin(9600);
  dht.begin();

  Serial.println("Sistema iniciado...");
  Serial.println("------------------------");
}

void loop()
{

  valorSolo = analogRead(sensorSoloPin);

  float temperatura = dht.readTemperature();

  if (isnan(temperatura))
  {
    Serial.println("Erro ao ler o DHT11!");
  }
  else
  {
    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.println(" °C");
  }

  // ===== EXIBE SOLO =====
  Serial.print("Umidade do solo: ");
  Serial.println(valorSolo);

  if (valorSolo >= 600)
  {
    Serial.print("O solo está: ");
    Serial.print("Seco");
  }

  else if (valorSolo >= 300)
  {
    Serial.print("O solo está: ");
    Serial.print("Úmido");
  }

  else
  {
    Serial.print("O solo está: ");
    Serial.print("Molhado");
  }

  delay(2000); // necessário para o DHT11
}