import os
from visistingcard import VisitingCard
from extractor import DataExtractor

PATH = os.path.join(os.getcwd(), 'utils', 'driver', 'geckodriver')
URL = "https://deerwalk.edu.np/DWIT/faculty.php"

def main() -> None:
    extractor = DataExtractor(PATH, URL)
    length = extractor.extract_links()
    
    for i in range(length):
        data = extractor.get_profile_data(i)
        card = VisitingCard(*data)
        card.create(extractor.links[i])
        card.save()

    extractor.browser.close()




if __name__ == "__main__":
    main()