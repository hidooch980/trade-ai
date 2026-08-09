class InnovationLab:

    def __init__(self):
        self.projects={}
        self.experiments=[]


    def create_project(self,name,goal):

        self.projects[name]={
            "goal":goal,
            "status":"RESEARCH"
        }

        return self.projects[name]


    def run_experiment(self,project,result):

        experiment={
            "project":project,
            "result":result
        }

        self.experiments.append(experiment)

        return experiment


    def improve(self,project):

        if project in self.projects:
            self.projects[project]["status"]="IMPROVED"

        return self.projects.get(project)


    def status(self):

        return {
            "projects":len(self.projects),
            "experiments":len(self.experiments),
            "lab":"ACTIVE"
        }


innovation_lab=InnovationLab()
