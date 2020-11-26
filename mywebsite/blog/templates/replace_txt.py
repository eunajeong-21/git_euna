import os
import re


def findPatterns(str):
    pattern = r'(([\'|"])(css|js|demo-images|fonts|images)\/.*\.(css|js|png|jpg|gif)([\'|"]))'

    p = re.compile(pattern)
    results = p.findall(str)

    return results


def transformLink(link):
    curQuote = None
    quote1 = "'"
    quote2 = '"'

    if link.startswith(quote1):
        _link = link.strip(quote1)
        curQuote = quote1
    else:
        _link = link.strip(quote2)
        curQuote = quote2

    ##    if not _link.startswith("/"):
    ##        _link = f"/{_link}"

    if curQuote == quote1:
        newLink = f'{{% static "{_link}" %}}'
        newLink = quote1 + newLink + quote1
    else:
        newLink = f"{{% static '{_link}' %}}"
        newLink = quote2 + newLink + quote2
    return newLink


currentPath = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(currentPath):
    for file in files:
        filePath = os.path.join(root, file)
        if not filePath.endswith(".html"):
            continue

        print(filePath)
        with open(filePath, 'r', encoding='utf8') as file:
            filedata = file.read()

        results = findPatterns(filedata)
        print(results)
        for result in results:
            transformed = transformLink(result[0])
            print(f"from : {result[0]} -> {transformed}")
            filedata = filedata.replace(result[0], transformed)

      
        with open(filePath, 'w', encoding='utf8') as file:
            file.write(filedata)
