from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.formrecognizer import AzureKeyCredential
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

# Configurações de API
form_recognizer_endpoint = "https://<seu-form-recognizer-endpoint>.cognitiveservices.azure.com/"
form_recognizer_key = "<sua-chave-do-form-recognizer>"

computer_vision_endpoint = "https://<seu-computer-vision-endpoint>.cognitiveservices.azure.com/"
computer_vision_key = "<sua-chave-do-computer-vision>"

# Inicialização dos clientes
form_recognizer_client = DocumentAnalysisClient(
    endpoint=form_recognizer_endpoint,
    credential=AzureKeyCredential(form_recognizer_key)
)

computer_vision_client = ComputerVisionClient(
    endpoint=computer_vision_endpoint,
    credentials=CognitiveServicesCredentials(computer_vision_key)
)

# Função para analisar documentos com Form Recognizer
def analyze_document(file_path):
    with open(file_path, "rb") as document:
        poller = form_recognizer_client.begin_analyze_document("prebuilt-document", document)
        result = poller.result()

    print("=== Dados Extraídos ===")
    for kv_pair in result.key_value_pairs:
        if kv_pair.key and kv_pair.value:
            print(f"{kv_pair.key.content}: {kv_pair.value.content}")

# Função para detectar anomalias visuais no documento com Computer Vision
def analyze_image(file_path):
    with open(file_path, "rb") as image:
        analysis = computer_vision_client.analyze_image_in_stream(
            image,
            visual_features=["ImageType", "Objects", "Description"]
        )

    print("\n=== Análise Visual ===")
    print(f"Tipo de Imagem: {'Clip Art' if analysis.image_type.clip_art_type else 'Foto'}")
    if analysis.description.captions:
        print(f"Descrição: {analysis.description.captions[0].text}")

# Caminho do arquivo para análise
document_path = "exemplo_documento.pdf"
image_path = "exemplo_imagem.png"

# Chamada das funções
if os.path.exists(document_path):
    analyze_document(document_path)

if os.path.exists(image_path):
    analyze_image(image_path)
