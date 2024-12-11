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

being able to comfortably switch between working enviorments where seed is left ALMOST untouched (depends, will explain)

There are two ways to achieve this: 1) is independent chart for every enviorment (more complicated) and 2) is one values.yaml file only for each evniorment and enabling/disabling diffrent templates.

I chose the first meaning you need to need to change seed path to application which is environment/you choose which

by changing the seed path in the GitOps repository you pick which environment to start.
each environment has a diffrent resources and values. 
