class ChoosePerson():

    def __init__(self):
        """ Write something if we need to remember things like the last person followed or something like that """
        pass

    def choose(self, people):
        if len(people) > 0:
            return max(people, key=lambda person: person['confidence_name'])
