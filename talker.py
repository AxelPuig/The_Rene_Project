import app.rasp_speaking.talk as talk


class Talker:
    def __init__(self):
        self.hello_said = []
        self.hello_in_process = {}
        self.nobody_rate = 0
        self.time_since_last_action = 0

    def start(self):
        talk.rene_parle("Salut a vous les copains ! Je me prépare.")

    def ready(self):
        talk.rene_parle("Je suis prêt !")

    def talk(self, people, action, person, verbose=False):

        for person in people:
            if person['confidence_name'] >= 0.95:
                if person['name'] not in self.hello_said:  # Si bonjour non dit pour cette personne
                    if person['name'] not in self.hello_in_process:
                        self.hello_in_process[person['name']] = [1,
                                                            0]  # [1 pour le nombre de fois reconnu, 0 à 2 pour les nombre de boucles parcourues depuis la dernière reconnaissance de data[name], au plus 2
                    elif self.hello_in_process[person['name']][0] == 1:
                        talk.rene_parle('Bonjour ' + person['name'])
                        self.hello_said.append(person['name'])
                    else:
                        self.hello_in_process[person['name']] = [1, 0]
        for i in self.hello_in_process:
            if i not in self.hello_said and self.hello_in_process[i][0] != 0:  # pour éviter du travail inutile.
                if self.hello_in_process[i][1] <= 2:
                    self.hello_in_process[i][1] += 1  # indique qu'une boucle de plus a été parcourue
                else:
                    self.hello_in_process[i] = [0,
                                           0]  # réinitialise si pas de 2ème reconnaissance en moins de 3 boucles parcourues.

        if len(people) == 0:
            self.nobody_rate += 1

        if self.nobody_rate >= 5:
            self.nobody_rate = 0
            talk.read_file("app/rasp_speaking/nobody")

        if verbose:
            print(self.hello_said)
            print(self.hello_in_process)

        if action == 1 and self.time_since_last_action > 1:
            talk.read_file("app/rasp_speaking/hey")
            self.time_since_last_action = 0

        elif action == 2 and self.time_since_last_action > 1:
            talk.rene_parle("Ok, je vous ai pris en photo !")
            self.time_since_last_action = 0

        else:
            self.time_since_last_action += 1