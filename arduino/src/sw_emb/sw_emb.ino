#include <SPI.h>
#include <UIPEthernet.h>
#include <ArduinoJson.h>

// MAC address (pode ser qualquer valor único)
static byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// IP fixo (ou deixe como DHCP se preferir)
// IPAddress ip(192, 168, 15, 177);  // Endereço do Arduino na rede

// IP do servidor Flask
IPAddress server(192, 168, 15, 8);

// Endpoint da API Flask
const char* endpoint = "/estado_bombas";

// Porta HTTP
const int port = 80;

// Pinos das bombas
const int bombas[4] = { 4, 5, 6, 7 };
int estado_bombas[4] = { 0, 0, 0, 0 }; // Estado atual das bombas

// Ethernet client
EthernetClient client;

void conectarEthernet()
{
  Serial.println("Inicializando Ethernet com DHCP...");
  if (Ethernet.begin(mac) == 0)
  {
    Serial.println("Failed to configure Ethernet using DHCP");
    // no point in carrying on, so do nothing forevermore:
    while (true) {
      delay(1);
    }
  }

  // Aguarda conexão física com o cabo de rede
  delay(1000);
  Serial.println("Conectado à rede!");
  Serial.print("IP obtido via DHCP: ");
  Serial.println(Ethernet.localIP());
}

void atualizarBombas()
{
  if (client.connect(server, port))
  {
    Serial.println(" conectado.");

    // Enviando requisição GET
    client.println("GET /estado_bombas HTTP/1.1");
    client.print("Host: ");
    client.println(server);
    client.println("Connection: close");
    client.println(); // fim dos cabeçalhos
  }
  else
  {
    Serial.println("Falha na conexão.");
    return;
  }
   // Aguarda resposta e ignora cabeçalhos
  bool headersEnded = false;
  String payload = "";

  while (client.connected())
  {
    String line = client.readStringUntil('\n');
    if (!headersEnded)
    {
      if (line == "\r")
      {
        headersEnded = true;
      }
    }
    else
    {
      payload += line + "\n";
    }
  }

  client.stop(); // Encerra conexão

  // DEBUG: mostra o JSON recebido
  // Serial.println("Resposta JSON bruta:");
  // Serial.println(payload);

  // Faz parsing manual dos dados para a variável estado_bombas
  for (int i = 0; i < 4; i++)
  {
    estado_bombas[i] = parseSensor(payload, "\"" + String(i + 1) + "\":");
    digitalWrite(bombas[i], estado_bombas[i] == 1 ? HIGH : LOW);
    Serial.println("Estado da bomba " + String(i + 1) + ": " + (estado_bombas[i] == 1 ? "Ligada" : "Desligada"));
  }
}

// Função auxiliar para extrair valor de um campo JSON simples
int parseSensor(String json, String key) {
  int start = json.indexOf(key);
  if (start == -1) return -1; // chave não encontrada

  start += key.length(); // pula até após a chave
  while (json[start] == ' ') start++; // ignora espaços
  int end = json.indexOf(',', start);
  if (end == -1) end = json.indexOf('}', start);
  if (end == -1) return -1;

  return json.substring(start, end).toInt();
}


void setup()
{
  Serial.begin(115200);
  for (int i = 0; i < 4; i++)
  {
    pinMode(bombas[i], OUTPUT);
    digitalWrite(bombas[i], LOW); // Inicialmente desligadas
  }
  conectarEthernet();
}

void loop()
{
  atualizarBombas();
  delay(1000); // Atualiza a cada 1 segundos
}
