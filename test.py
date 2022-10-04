# pylint: disable=C0103

ID_COUNTER = 1

designsDB = []
versionsDB = []
propertiesDB = []
elementsDB = []
versionedElementPropertiesDB = []


class Design:
    width = 500
    height = 600

    def __init__(self, elements):
        global ID_COUNTER
        ID_COUNTER += 1

        self.id = ID_COUNTER
        self.elements = elements


class Element:
    def __init__(self, kind, properties):
        global ID_COUNTER
        ID_COUNTER += 1

        self.id = ID_COUNTER
        self.kind = kind
        self.properties = properties


class Version:
    def __init__(self, name, properties):
        global ID_COUNTER
        ID_COUNTER += 1

        self.id = ID_COUNTER
        self.name = name
        self.properties = properties


class Property:
    def __init__(self, unit, value):
        global ID_COUNTER
        ID_COUNTER += 1

        self.id = ID_COUNTER
        self.unit = unit
        self.value = value

class VersionedElementPropertyMap:
    def __init__(self, elementId, propertyId):
        global ID_COUNTER
        ID_COUNTER += 1

        self.id = ID_COUNTER
        self.elementId = elementId
        self.propertyId = propertyId

def idMapper(n):
    return n.id

def addVersion(name, properties):
    newVersion = Version(name, map(idMapper, properties))
    versionsDB.append(newVersion)

def addVersionPropertyMapping(elementId, propertyId):
    versionedElementPropertiesDB.append(VersionedElementPropertyMap(elementId, propertyId))

def findInArray(array, id):
    return list(filter(lambda obj: obj.id == id, array))[0]

# Default Version ANY
# Design with 1 image
imageUrlProp = Property('url', 'www.placeholder.com/DEFAULT')
imageBorderProp = Property('border', 'blue')
imageElement1 = Element('image', [imageUrlProp.id, imageBorderProp.id])
englishDesign1 = Design([imageElement1.id])


# Swedish Version
swedishImageUrlProp = Property('url', 'www.placeholder.com/SE')
swedishVersion = Version('Swedish', [swedishImageUrlProp.id])
addVersionPropertyMapping(imageElement1.id, swedishImageUrlProp.id)
addVersion('Swedish', [swedishImageUrlProp])


# store
propertiesDB.append(imageUrlProp)
propertiesDB.append(imageBorderProp)
propertiesDB.append(swedishImageUrlProp)

designsDB.append(englishDesign1)
elementsDB.append(imageElement1)

# reconstruct

finalDesign = {}

# 1. Query Design
foundDesign = findInArray(designsDB, englishDesign1.id)
# 2. Query all elements from design
foundElements = []
for elementId in foundDesign.elements:
    foundElements.append(findInArray(elementsDB, elementId))
# 3. Query all element properties from design
foundElementProperties = []
for element in foundElements:
    for elPropertyId in element.properties:
        foundElementProperties.append(findInArray(propertiesDB, elPropertyId))

# 4. Query Version
foundVersion = findInArray(versionsDB, swedishVersion.id)

# 5. Get versioned element mapping


print(foundElementProperties[0].value)



