from presidio_analyzer import AnalyzerEngineProvider
from backports import configparser

conf_file="./config_files/configSpacy.yaml"

provider = AnalyzerEngineProvider(
    analyzer_engine_conf_file=conf_file
    )

analyzer=provider.create_engine()
class Presidio:
    def examine(texto: str)->str:
        analyzer_results_es = analyzer.analyze(text=texto,language="es")
        entidades_detectadas = []
        for result in analyzer_results_es:
            entity_text = texto[result.start:result.end]  # Extraer el texto detectado
            print(f"Entidad: {result.entity_type}, Texto: '{entity_text}', Score: {result.score}")
            if result.score >= 0.8:
                entidades_detectadas.append(entity_text)
            
        print("PII que se tendran en cuenta: ")
        print(entidades_detectadas)
        PIItokens=", ".join(entidades_detectadas)
        print("\n\n")
        return PIItokens

test_memory=False
testTo="test2"
num_iterations = 50
exit_folder="salidaTestSLMShortMessage.txt"

configfile_name = "./config_files/test.ini"
configFile = configparser.ConfigParser()
with open(configfile_name, encoding='utf-8') as configfilename:
    configFile.read_file(configfilename)
i=0

if __name__=="__main__":
    while True:
        if i==50:
            exit
        texto=configFile.get(testTo,f"prompt{i+1}")
        print(f"Texto: {texto}")
        Presidio.examine(texto)
        i=i+1