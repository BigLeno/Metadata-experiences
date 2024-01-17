import xml.etree.ElementTree as ET

# Leia o arquivo XML
try:
    tree = ET.parse('Data\\um.nfo')
    root = tree.getroot()

    # Agora você pode acessar os elementos do XML
    # Por exemplo, para obter o texto do primeiro elemento 'version'
    version_element = root.find('version')
    if version_element is not None:
        version = version_element.text
        print(version)
    else:
        print("Elemento 'version' não encontrado no arquivo XML.")
except ET.ParseError as e:
    print(f"Não foi possível ler o arquivo. Erro: {e}")
    exit(-1)