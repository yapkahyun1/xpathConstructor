function getElementAttributes(element) {
  const result = {
    tag: element.tagName.toLowerCase()
  };

  for (const attr of element.attributes) {
    result[attr.name] = attr.value;
  }


  return result;
}
