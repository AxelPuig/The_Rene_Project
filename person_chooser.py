class PersonChooser():

    def __init__(self):
        """ Write something if we need to remember things like the last person followed or something like that """
        self.person = None

    def choose(self, people):
        if people:
            if self.person is not None:
                x1,y1,x2,y2 = self.person['box']
                x,y = (x1+x2)/2,(y1+y2)/2
            else:
                self.person = max(people, key=lambda person: person['confidence_name'])
        else:
            self.person = None
        return self.person