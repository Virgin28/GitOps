# This is Start Doing.
### Simple and effortless.

if you want your Web Application to be used then, you in  the right place.<br>
this is a fun, usable app for your infrastructure.

#### The repo contains:
1. __Start Doing__ --> start-doing
2. __CI__ ------------> .github/workflows
3. __Helm Chart__ --> start-doing-chart.
4. __local-docker-compose__ --> for local run


## The App
Start Doing is an easy-going to-do list.<br>
make your __DOs__ today, tomorrow, whenever.<br>

it has __3__ components.
1. __Frontend - Nginx.__ <br>
holds the home page and will be incharge for an easy internet connection.
2. __Backend - Python__ <br>
the arms and legs, an engine. the Python holds the rest of the application and allows you to navigate between its pages, <br>
with SQL Alchemy, the Backend holds the crucial role of updating every DO in the Database through API requests.  <br>
3. __DB - mysql - AWS/RDS__ <br>
"Old Fashioned" mysql, it just works.<br>
can be ran locally with mysql container, or a Cluster's DB Instance.

### UI - It just clicks.
When we made the app we were really against an all included page, it made our app more complicated, but now its smarter, user friendly and better than ever. <br>

<img width="1705" alt="Image" src="https://github.com/user-attachments/assets/b1a23dd2-d5b1-4af7-a24e-ca502646dca6" />

<br> 

<br> 
<img width="1686" alt="Image" src="https://github.com/user-attachments/assets/a2aa5dfe-0033-424c-8180-e5d493276398" />
<br>

### Just do it.
<img width="1679" alt="Image" src="https://github.com/user-attachments/assets/b3f1195f-97c2-467b-a9ad-9403a6c7ad09" />
<br>

### How it would look like 

<img width="1680" alt="Image" src="https://github.com/user-attachments/assets/7c1c6e59-e19b-42ca-ab7d-f6919c1ed883" />
<br>

### From here and on - you own it.<br> Done, Done and Done.<br>

<p>
  <img src="https://github.com/user-attachments/assets/f13e7438-c4cb-4434-bd5b-f66ef3dc6da9" alt="Image 1" width="500" style="margin-right: 200px;">
  <img src="https://github.com/user-attachments/assets/6b302110-ce4c-4b3d-8e4a-e65162591bfb" alt="Image 2" width="500">
</p>

# GitOps in Action 

## Smart CI
As you know, the key concept of  __"CI-CD"__ is that there's never a "Last Update". <br>
We would love and we advocate contributers to refine Start-Doing, while keeping its simplicity.<br>
### Our CI - a GitHub Action. painless updates in your Cluster.  <br>
all it takes is a little push.<br>
The "Action" triggers from environment push. Each environemt has its own GitHub Branch.

### Our Action:
1. __Logs in__ an AWS Account (Join AWS credentials through GitHub Actions variables)
2. __Builds the Docker Images__ from start-doing.
3. __Tests__ the container's connection, when establlished, it
4. __Pushes__ the images to an AWS/ECR.

### Bonus CD Part
Smart CI does more then just tests.<br>
our __CD__ cluster tool is __ArgoCD.__ <br>
Our Argo-Application is Located in a different repo, checkout: [GitOps-ArgoCD](https://github.com/Virgin28/GitOps-ArgoCD)<br>
### Our Action CD part is:

5. __Clones__ our ArgoCD repo
6. __Checks__ which branch (environments dev staging or prod) the update was pushed from.
7. __Updates__ image tags in values.yaml for the certain environment, and
8. __Uses__ a GitHub Token that allows independent pushing. That way, it could
9. __Push__ the updated tags to the the envrionment we pushed from.<br>
<br>
When we Apply our ArgoCD application to the cluster, with Start-Doing manifests Front and Back images will be the latests. <br>
When an update occurs. the Argo-Application will RollUpdate our cluster's pods into the newer version.<br>
For safer updates, do not think twice - ArgoRollouts will be the best tool.

## Impeccable Helm Chart

### The Helm chart manifests
1. Frontend Deployment
2. Backend Deployment
3. Frontend Service
4. Backend Service
5. Ingress that is built on Nginx Controller that Loadbalances access for domain.
6. SecretStore - from ExternalSecrets helm release
7. ExternalSecret - Allows the Application pull the DB credentials so that way our Backend will

## Try the app on your own! With docker-compose

First of first,<br>
``` git clone https://github.com/Virgin28/GitOps.git ```

Second of which,<br>
``` cd GitOps ```

Third is third<br>
``` mv start-doing/docker-compose.yaml . ``` <br>
``` mv local-docker-compose start-doing/docker-compose.yaml ```<br>
``` cd start-doing ```

Fourth of a kind<br>
``` docker compose up --build ```

head to ```http://localhost:8080```

