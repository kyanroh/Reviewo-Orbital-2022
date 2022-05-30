import pandas as pd

class MLModel:
    def __init__(self, DOCUMENT_PATH):
        self.reviews = pd.read_excel(DOCUMENT_PATH)


    def filter(self):
        return "Filtered"


    def conductCSA(self):
        return "CSA Conducted"


    def compileTopFiveWords(self):
        return {
                "Positive" : 
                    ["Excellent", "Best choice", "Very good", "Helpful", "High-grade"], 
                "Negative" : 
                    ["Expensive", "Not worth", "Not good", "Terrible", "Disgusting"]
                }