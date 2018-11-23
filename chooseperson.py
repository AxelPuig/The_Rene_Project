class ChoosePerson():

    def __init__(self):
        """ Write something if we need to remember things like the last person followed or something like that """
        self.person = None

    def choose(self, people):
        if people:
            if self.person is not None:
                distances = []
                for other_person in people:
                    box = other_person["box"]
                    distances.append(self.distance(box))
                index = distances.index(min(distances))
                self.person = people[index]
            else:
                self.person = max(people, key=lambda person: person['confidence_name'])
        else:
            self.person = None
        return self.person

    def distance(self, box):
        x1_a, y1_a, x2_a, y2_a = self.person["box"]
        x1_b, y1_b, x2_b, y2_b = box
        return (x1_a - x1_b)**2 + (x2_a - x2_b)**2 + (y1_a - y1_b)**2 + (y2_a - y2_b)**2
