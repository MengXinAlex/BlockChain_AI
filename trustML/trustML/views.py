from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings

from uploadModel.models import ML_model

import os
import sys
import shutil
sys.path.append(os.getcwd()+'/models/dog_classifier/')
sys.path.append(os.getcwd()+'/trustML/')
import dog_classifier
from compile_solidity_utils import w3
import json
import numpy as np

def login(request):
    return render(request, 'login.html')
    
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
    
def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='/')
def user_home(request):
    # get all models
    model_sets = ML_model.objects.filter()
    context = {"model_sets":model_sets}
    return render(request,"user_home.html",context)

@login_required(login_url='/')
def user_profile(request):
    return render(request, 'user_profile.html')

@login_required(login_url='/')
def wallet(request):
    return render(request, 'wallet.html')

@login_required(login_url='/')
def buy_model(request):
    model_sets = ML_model.objects.filter()
    context = {"model_sets":model_sets}
    return render(request, 'buy_model.html',context)

@login_required(login_url='/')
def help(request):
    return render(request, 'help.html')

@login_required(login_url='/')
def admin_home(request):
    return render(request, 'admin_home.html')

@login_required(login_url='/')
def admin_profile(request):
    return render(request, 'admin_profile.html')

@login_required(login_url='/')
def admin_submissions(request):
    #reward = Reward()
    with open("data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]
    # Create the contract instance with the newly-deployed address
    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )
    results = []
    for i in range(int(user.functions.getTotalSubmissions().call())):
        results.append([str(user.functions.getSubmissionAccount(i).call()),user.functions.getSubmission(i).call()])
    print(results)
    """
    if request.method == 'POST':
        sender = w3.eth.accounts[1]
        accounts = request.form['number'].split(",")
        for i in accounts:
            receiver = address = w3.toChecksumAddress(results[int(i)][0])
            amount = w3.toWei(0.1, "ether")
            w3.eth.sendTransaction({'from': sender, 'to': receiver, 'value': amount})
        b = w3.fromWei(w3.eth.getBalance(sender), 'ether')
        return render_template("admin_profile.html", address = sender, balance = b)
    return render_template("admin_submission.html",submission = results, form = reward)
    """
    return render(request, 'admin_submissions.html', {'submission': results})


@login_required(login_url='/')
def model(request):
    path=settings.BASE_DIR+'/media/data/'  # insert the path to your directory
    img_list = [f for f in os.listdir(path)  if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png')]
    return render(request,'model.html', {'images': img_list})

def register(request):
    return render(request, 'register.html')

@login_required(login_url='/')
def result(request):
    path=settings.BASE_DIR+'/models/dog_classifier/'  # insert the path to your directory
    img_list = [f for f in os.listdir(path)  if f.endswith('results.png')]
    results = submit_data();
    return render(request,'result.html', {'images': img_list, "Accuracy": results["Accuracy"], "Precision": results["Precision"],
    "Recall": results["Recall"], "Fscore": results["Fscore"], "Rank": results["Rank"], "Total": results["Total"]})

def submit_data():
    "TODO get user address once set up in database"
    #address = w3.toChecksumAddress(userstore["address"])
    address = w3.eth.accounts[5]
    #Set default account
    w3.eth.defaultAccount = w3.eth.accounts[1]
    #Open json file to get contract ABI (Application Binary Interface) and address
    with open("data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]
    # Create the contract instance with the newly-deployed address
    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )
    # Generate some results
    data_quality = 60
    data_similarity = 70
    data_score = int((data_quality+data_similarity)/2)
    #Submit the Results
    tx_hash = user.functions.submitData(address,data_quality,data_similarity,data_score, 55)
    tx_hash = tx_hash.transact()
    w3.eth.waitForTransactionReceipt(tx_hash)

    results = {}
    #Store results retrieved from Blockchain and send to data_evaluation page
    results["Accuracy"] = user.functions.getAccuracy(address).call()
    results["Precision"] =  user.functions.getPrecision(address).call()
    results["Recall"] = user.functions.getRecall(address).call()
    results["Fscore"] = user.functions.getFscore(address).call()
    results["Rank"]  = user.functions.getRank(address).call()
    results["Total"] =  user.functions.getTotalSubmissions().call()
    return results

def data(request):
    path=settings.BASE_DIR+'/media/data/'  # insert the path to your directory
    img_list = [f for f in os.listdir(path)  if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png')]
    return render(request,'data.html', {'images': img_list})
    # return render(request, 'data.html')

def run(request):
    print(os.getcwd())
    dog_classifier.classify()
    return redirect('/result')

def clear(request):
    path = settings.BASE_DIR+'/media/data/'
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if (os.path.isfile(file_path) and (file_path.endswith('.jpeg') or file_path.endswith('.jpg') or file_path.endswith('.png'))):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    return redirect('/model')

def make_acc_unc_json(acc, unc):
    a_u_json = []
    for i in range(len(acc)):
        temp = {}
        temp["unc_p"] = unc[i]
        temp["acc_p"] = acc[i]
        a_u_json.append(temp)
    json_final = json.dumps(a_u_json)
    return json_final
