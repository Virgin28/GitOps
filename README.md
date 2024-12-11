Hey all

This repo contains a task that was resolved

Seed >> Gitops Chart >> argo application >> real chart

from botton to top:
1. realchart contains an untouched nginx helm chart (default chart that is created with helm create...)
2. Argo Apllication in environment/dev/templates that launches the chart above into ArgoCD
3. Gitops Chart is in fact the repo itself. in enviorment/dev there is a helm chart that launches an argo application - that launches the argo application above 
4. Seed application that wraps everything
Seed >> Gitops Chart >> argo application >> real chart

a) seed Application is in fact an argo application that its source is this repo
b) it launches the GitopsChart at enviorment/dev
c) GitOpsChart at enviorment/dev launches an Argo Application
d) the ArgoApplication launches the realchart (helm chart)
that installs nginx on the ArgoCD client.


The idea behind it:
being able to comfortably switch between working enviorments, seed is left untouched
the GitOps chart is the one who's changing where you can pick which enviorment to start (lets say we have another chart except for dev with diffrent
resources and values, you can also make the chart to be located at enviorments if resources are always the same on only put values.yaml under the required enviorment such as dev/values.yaml only or prod/values.yaml. my idea was that every enviorment can have a diffrent set of components so it will be better only to change the seed enviorment/(enviorment name). it makes you write more value files but every enviorment will be more universal
and independet) 