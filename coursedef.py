# define a Course object to store information about a course
class Course:
    def __init__(self, codes, title, description, prereqs, coreqs):
        self.codes = codes
        self.title = title
        self.description = description
        self.prereqs = prereqs
        self.coreqs = coreqs
