# Project Details
Multiple Python Flask App on Minikube

Overview:
1. Implement two basic, dependent microservices.
2. Deploy the solution on a local container orchestrator(Minikube).
3. Create a diagram and briefly explain how this would be deployed using Continuous
Integration / Deployment on a cloud provider.


> This is a project to build Flask app using python flask framework and deploy it on Kubernetes cluster using minikube. 


### Prerequisites
You must have setup minikube on your local. Once it is done then start minikube and check below commands to verfiy kubernetes has been setup on local. 
* mikikube start
```
$ minikube.exe start
* minikube v1.1.1 on windows (amd64)
* Tip: Use 'minikube start -p <name>' to create a new cluster, or 'minikube delete' to delete this one.
* Restarting existing virtualbox VM for "minikube" ...
* Waiting for SSH access ...
* Configuring environment for Kubernetes v1.14.3 on Docker 18.06.3-ce
* Relaunching Kubernetes v1.14.3 using kubeadm ...
* Verifying: apiserver proxy etcd scheduler controller dns
* Done! kubectl is now configured to use "minikube"
```

```

```
# TASK 1

### This project consist of two steps:
1. Created two dockerized microservices using alpine python as base image and used flask framework to provide Restapi endpoints.

* Below are output of Dockerfile and python file(api.py) (Application1)
```
$ cat Dockerfile
# Using Base image alpine with installed python3
FROM frolvlad/alpine-python3

MAINTAINER "Mayank Koli"

#choosing /usr/src/app as working directory
WORKDIR /usr/src/app

# Mentioned python module name to run application
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Exposing applicaiton on 80 so that it can be accessible on 80
EXPOSE 80

#Copying code to working directory
COPY . .

#Making default entry as python will launch api.py
CMD [ "python3", "api.py" ]


$ cat api.py
#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests, random, json

app = Flask(__name__)

@app.route('/api', methods=['POST'])

def api():
    user_data = request.get_json()
    data = user_data['message']
    r = requests.post('http://localhost:5000/reverse', json={'message': data })
    json_resp = r.json()
    a = random.random()
    return jsonify({"rand": a, "message": json_resp.get("message")})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)

```


* Below are output of Dockerfile and python file(reverse.py) (Application2)
```
$ cat  ../flask2/Dockerfile
# Using Base image alpine with installed python3
FROM frolvlad/alpine-python3

MAINTAINER "Mayank Koli"

#choosing /usr/src/app as working directory
WORKDIR /usr/src/app

# Mentioned python module name to run application
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Exposing applicaiton on 5000 so that it can be accessible on default host(127.0.0.1) and port(5000).
EXPOSE 5000

#Copying code to working directory
COPY . .

#Making default entry as python will launch reverse.py
CMD [ "python3", "reverse.py" ]


$ cat reverse.py
#!/usr/bin/env python3

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/reverse', methods=['POST'])
def reverse():
    req_data = request.get_json()
    word = req_data['message']
    output = word[::-1]
    return jsonify({ "message" : output })

if __name__ == "__main__":
    app.run(debug=True, port=5000)


```

* Once images are built then I am provisioning them on kubernetes(minikube).

# TASK 2
2. I have simply made code which is well structured, extensible, testable, readable. You can find that I am  running two different container in same/one pod so that first app (which is accessible by public) can reach to second app (which is running on localhost and default port).

```
$ cat flask-app-deployment.yml
apiVersion: apps/v1
kind: Deployment   <---Deployment Object
metadata:
  name: flask-app  <---Provided name to this object so that it can easily found by name
  labels:
    app: flask-app
spec:
  replicas: 1      <---Its useful when you want to manage the scaling of pods
  selector:
    matchLabels:
      app: flask-app
  template:        <---Template for Pods specification which are included in other objects i.e. service.yml
    metadata:
      labels:
        app: flask-app
    spec:
      containers:  
      - name: flask-app1  <---The name of container you want to provide
        image: docker.io/manukoli1986/flask-app1:3  <---Image name 
        ports:
        - containerPort: 80  <--- Mentioned port so that others can connect to this app on 80 port
      - name: flask-app2
        image: docker.io/manukoli1986/flask-app2:3
        ports:
        - containerPort: 5000  <--- Mentioned port so that first app can connect on localhost using 5000 port used by second app 
---
apiVersion: v1
kind: Service   <--- Used so that group of pods can be point to a common name, either it dies or restarts your app will always be accessible by service name
metadata:
  name: flask-app   <--- expose service name
  labels:
    app: flask-app   <--- choose only those pods who have same labels
spec:
  ports:
    - port: 80      <--- Exposing port for client/public access
      targetPort: 80  <---Connecting this service to pods which are exposed to be connected on
  selector:
    app: flask-app
  type: LoadBalancer  <--- Choose how we want incoming traffic would reach to pods 
```

* Deploy them on minikuber using kubectl command
```
$ kubectl.exe create  -f .
deployment.apps/flask-app-deployment created
service/flask-app created

$ kubectl.exe get pods
NAME                                   READY   STATUS    RESTARTS   AGE
flask-app-deployment-66486467f-vp486   2/2     Running   0          153m
flask-app-deployment-66486467f-xpcj6   2/2     Running   0          153m

$ kubectl.exe get svc
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
flask-app       LoadBalancer   10.108.207.40   <pending>     80:32660/TCP   4m23s
kubernetes      ClusterIP      10.96.0.1       <none>        443/TCP        26d
```

#Application is UP and running, let's access it with commands and postman tool.
* postman tool
![alt text](https://github.com/manukoli1986/python-flaskapp/blob/master/images/postman.jpg)



* curl command
```
$ curl -X POST http://192.168.99.101:32660/api -H 'Content-Type: application/json'  -d '{"message" : "Game"}'
```
![alt text](https://github.com/manukoli1986/python-flaskapp/blob/master/images/curl.jpg)

# TASK 3
A) Produce a system diagram and a brief description of how you would deploy the solution
on a cloud provider such as AWS or GCP.

![alt text](https://github.com/manukoli1986/python-flaskapp/blob/master/images/cicd.jpg)

1. Developer commits code using a standard git push command.
2. Jenkins picks up that new code has been pushed to AWS CodeCommit.
3. Jenkins pulls a Docker image from Amazon ECR.
4. Jenkins rebuilds the Docker image incorporating the developer’s changes.
5. Jenkins pushes updated the Docker image to Amazon ECR.
6. Jenkins starts the task/service using the updated image in an Amazon EKS cluster using anisble.

B) Explain how you would integrate CI/CD to perform deployments, and how you would
ensure downtime was avoided?

As discribed above, the steps we can implement complete CICD and even more we can add more tool for over requirement i.e. Docker sign images, Docker smaller images, Multiimage Dockerfile, Nexus, JUnit Test for Images etc. For ensure we can adopt Blue Green Deployment strategy. we gives an idea blue and green where Blue would be treated as Live traffic serving and for Green we will bring new version of application. 


##Below are the steps mentioned:

1. Prepare the blue deployment and green deployment with VERSION=1 and TARGET_ROLE set to blue or green respectively.
2. Prepare the public service endpoint, which initially routes to one of the backend environments, say TARGET_ROLE=blue.
3. Then prepare a test endpoint so that we can visit the backend environments for testing. They are similar to the public service endpoint, but they are intended to be accessed internally by the dev/ops team only.
4. Update the application in the inactive environment, say green environment. Set TARGET_ROLE=green and VERSION=2 in the deployment config to update the green environment.
5. Test the deployment via the test-green test endpoint to ensure the green environment is ready to serve client traffic.
6. Switch the frontend Service routing to the green environment by updating the Service config with TARGET_ROLE=green.
7. Run additional tests on the public endpoint to ensure it is working properly.
8. Now the blue environment is idle and we can leave it with the old application so that we can roll back if there’s issue with the new application or reduce its replica count to save the occupied resources
