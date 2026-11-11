import xml.etree.ElementTree as et
import urllib.request
import urllib.error


def parse_pom_xml(xml_content: str) -> list:
    try:
        root = et.fromstring(xml_content)
    except et.ParseError:
        raise Exception("Ошибка парсинга XML: неверный формат файла")

    deps = []
    for dep in root.findall(".//dependency"):
        artifact = dep.find("artifactId")
        version = dep.find("version")
        if artifact is not None and version is not None:
            deps.append(f"{artifact.text}:{version.text}")
    return deps


def get_dependencies(repo_url: str, test_mode: bool) -> list:
    if test_mode:
        with open("configs/mock_pom.xml", "r", encoding="utf-8") as f:
            return parse_pom_xml(f.read())

    url = repo_url
    if not url.endswith(".xml") and not url.endswith(".pom"):
        if not url.endswith("/"):
            url += "/"
        url += "pom.xml"

    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
            return parse_pom_xml(content)
    except urllib.error.URLError:
        raise Exception(f"Не удалось скачать pom.xml: {url}")