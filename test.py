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

class VersionedElement:
    def __init__(self, elementId):
        global ID_COUNTER
        ID_COUNTER += 1

        self.id = elementId
        self.properties = []

    def addProperty(self, property):
        self.properties.append(property)
    

def idMapper(n):
    return n.id

def addVersion(name, properties):
    newVersion = Version(name, map(idMapper, properties))
    versionsDB.append(newVersion)
    return newVersion.id

def addVersionPropertyMapping(elementId, propertyId):
    versionedElementPropertiesDB.append(VersionedElementPropertyMap(elementId, propertyId))

def findInArray(array, _id):
    return list(filter(lambda obj: obj.id == _id, array))[0]

def findPropertyInArray(array, propertyId):
    return list(filter(lambda obj: obj.propertyId == propertyId, array))[0]

def printElements(elements):
    for element in elements:
        print('Element: ' + element.kind)
        for property in element.properties:
            print('Prop: ' + property.unit + ' - ' + property.value)

# Default Version ANY
# Design with 1 image
imageUrlProp = Property('url', 'www.placeholder.com/DEFAULT')
imageBorderProp = Property('border', 'blue')
imageElement1 = Element('image', [imageUrlProp.id, imageBorderProp.id])
englishDesign1 = Design([imageElement1.id])


# Swedish Version
swedishImageUrlProp = Property('url', 'www.placeholder.com/SE')
addVersionPropertyMapping(imageElement1.id, swedishImageUrlProp.id)
swedishVersionId = addVersion('Swedish', [swedishImageUrlProp])


# store
propertiesDB.append(imageUrlProp)
propertiesDB.append(imageBorderProp)
propertiesDB.append(swedishImageUrlProp)

designsDB.append(englishDesign1)
elementsDB.append(imageElement1)



# 1. Query Design
foundDesign = findInArray(designsDB, englishDesign1.id)

# 2. Query all elements from design
foundElements = []
for elementId in foundDesign.elements:
    foundElements.append(findInArray(elementsDB, elementId))

# 3. Query all element properties from design
foundElementProperties = []
for element in foundElements:
    for elementPropertyId in element.properties:
        foundElementProperties.append(findInArray(propertiesDB, elementPropertyId))

# reconstruct
print('Default Version Design:')
for element in foundElements:
    mappedElementProperties = []

    for elementPropertyId in element.properties:
        mappedElementProperties.append(findInArray(foundElementProperties, elementPropertyId))

    element.properties = mappedElementProperties

finalDesign = Design(foundElements)
printElements(finalDesign.elements)

# 4. Query Version
foundVersion = findInArray(versionsDB, swedishVersionId)

# 5. Get versioned element mapping, props and element ids
versionedElements = []
for propertyId in foundVersion.properties:
    versionMapping = findPropertyInArray(versionedElementPropertiesDB, propertyId)
    # 6. Get Versioned property
    versionProperty = findInArray(propertiesDB, propertyId)

    # create a version element if not present
    if not list(filter(lambda obj: obj.id == versionMapping.elementId, versionedElements)):
        versionElement = VersionedElement(versionMapping.elementId)
        versionedElements.append(versionElement)
    else:
        versionElement = findInArray(versionedElements, versionMapping.elementId)
    versionElement.addProperty(versionProperty)

# 7. Overwrite elements properties by type
for versionElement in versionedElements:
    originalElement = findInArray(foundElements, versionElement.id)

    # filter versioned properties out of original
    for versionElementProperty in versionElement.properties:
        originalElement.properties = list(filter(lambda obj: obj.unit != versionElementProperty.unit, originalElement.properties))
        originalElement.properties.append(versionElementProperty)

    # replace original element with newly mapped one
    foundElements = list(filter(lambda obj: obj.id != originalElement.id, foundElements))
    foundElements.append(originalElement)


print('\nSwedish Version Design:')
swedishDesign = Design(foundElements)
printElements(swedishDesign.elements)