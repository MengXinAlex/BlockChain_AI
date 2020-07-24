"""
This python file handles all the request relative to upload model
"""
from .forms import ModelForm
from django.shortcuts import render, redirect
from .models import ML_model

from uploadData.models import evaluation_result, Data
from uploadData.forms import DataForm, editDataForm
from django.core.files import File
from django.urls import reverse
import numpy as np
from .evaluation.evaluate_model import get_confusion_matrix, get_model_and_data, get_precision_recall_accuracy, \
    get_score, get_similarity, get_uncertainty, get_missing_portion, clear_missing_data, sigmoid, get_model_uncertainty, \
    get_test_model_accuracy
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import os
from compile_solidity_utils import w3
import json
import ast
from django.shortcuts import HttpResponse


# Create your views here.


def get_model(request):
    # if it's post then process form data
    if request.method == 'POST':
        form = ModelForm(request.POST, request.FILES)
        if form.is_valid():
            # get the creator_id
            # TODO consider transaction maybe after
            instance = ML_model(creator_id=request.user.pk, model_name=request.FILES['model_name'], \
                                model_file=request.FILES('model_file'), \
                                specification=request.FILES('specification'), \
                                weight=request.FILESI('weight'))
            instance.save()
            # if success, redirect to upload origin data
            # return a http response


def home(request):
    """
    This page render the homepage of our website despite of you identity
    :param request: the front-end request from user
    :return: render a home page, if error occurs, go back to the login page
    """
    # get the model that user uploaded
    if User.is_authenticated:
        model_sets = ML_model.objects.filter(creator=request.user)
        context = {"model_sets": model_sets}
        return render(request, "uploadModel/home.html", context)
    else:
        # TODO redirect to login page
        redirect("http://localhost:8000/")


def error(request):
    if User.is_authenticated:
        return render(request, "uploadModel/error.html")
    else:
        # TODO redirect to login page
        redirect("http://localhost:8000/")


def error_data(request):
    if User.is_authenticated:
        return render(request, "uploadModel/error_data.html")
    else:
        # TODO redirect to login page
        redirect("http://localhost:8000/")


def test(request):
    # get the model that user uploaded
    if User.is_authenticated:
        model_sets = ML_model.objects.filter(creator=request.user)
        print(len(model_sets))
        context = {"model_sets": model_sets}
        return render(request, "uploadModel/home.html", context)
    else:
        # TODO redirect to login page
        redirect("http://localhost:8000/")


def model_detail(request, model_id):
    """
    This method handles the request when user want to see the detail of a model and click on some of the model displayed in the home page.
    :param request: request from user
    :param model_id: which model you are looking for? It's a primary key in the database
    :return: a template together with the context of this model
    """
    # the context for template, contain all the information we need in the front-end. rememember to update it like a dictionary
    context = {}

    # Check if Admin has uploaded data
    try:
        OR = Data.objects.get(relative_model=model_id, data_type="OR")
        if request.user == OR.uploader:
            context["user_data_exists"] = True
        result = evaluation_result.objects.get(model=model_id, data=OR.pk)
        result_file = result.result
        data = result
        cf = np.loadtxt(result_file, delimiter=",", dtype=int)
        precision, recall, accuracy = get_precision_recall_accuracy(cf)
        context["user_accuracy"] = accuracy * 100
        context["user_precision"] = precision[0] * 100
        context["user_recall"] = recall[0] * 100
        context["data"] = data

        # data_sets = Data.objects.all()
        # context = {"data_sets": data_sets}

         # send accuracy and uncertainty
        _accset = ast.literal_eval(result.accset)
        _uncset = ast.literal_eval(result.uncset)
        _new_accset = []
        _new_uncset = []
        for gg in _accset:
            _new_accset.append(gg/100)
        for gg in _uncset:
            _new_uncset.append(gg/100)
        
        

        context["user_accset"] = (_new_accset) 
        context["user_uncset"] = (_new_uncset)
        context["user_au"] = make_acc_unc_json(_new_accset,_new_uncset)
        context["user_ua"] = make_acc_unc_json1(_new_accset,_new_uncset)


        context["user_f1_score"] = 2 * (precision[0] * recall[0]) / (precision[0] + recall[0]) * 100
        

    except ObjectDoesNotExist:
        pass

    with open("data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )

    results = []
    average_acc = 0
    average_pre = 0
    average_rec = 0
    average_f1 = 0

    context["acc_list"] = []
    context["pre_list"] = []
    context["rec_list"] = []
    context["f1_list"] = []
    context["sub_list"] = []
    context["score_list"] = []

    n_submissions = int(user.functions.getTotalSubmissions(model_id).call())

    if n_submissions > 0:
        context["data_submitted"] = True
        context["dt_exists"] = True
        for i in range(n_submissions):
            result = user.functions.getSubmission(model_id, i).call()   
            average_acc += result[0]
            average_pre += result[1]
            average_rec += result[2]
            average_f1 += result[3]

            context["acc_list"].append(result[0])
            context["pre_list"].append(result[1])
            context["rec_list"].append(result[2])
            context["f1_list"].append(result[3])
            context["score_list"].append(result[4])
            context["sub_list"].append(i)


            wallet_address = str(user.functions.getSubmissionAccount(model_id, i).call())
            if request.user.wallet_address == wallet_address:
                context["user_data_exists"] = True
                # calculate average scores
                context["user_accuracy"] = result[0]
                context["user_precision"] = result[1]
                context["user_recall"] = result[2]
                context["user_f1_score"] = result[3]
                context["user_score"] = result[4]

                 # send accuracy and uncertainty
                accset, uncset = user.functions.getSubmissionAU(model_id, i).call()
                new_accset = []
                new_uncset = []
                for gg in accset:
                    new_accset.append(float(gg)/100)
                for gg in uncset:
                    new_uncset.append(float(gg)/100)

                context["user_accset"] = (new_accset) 
                context["user_uncset"] = (new_uncset)
                context["user_au"] = make_acc_unc_json(new_accset,new_uncset)
                context["user_ua"] = make_acc_unc_json1(new_accset,new_uncset)

            paid = user.functions.getPaid(model_id, i).call()
            results.append([wallet_address, result, paid])

        average_acc /= 100 * n_submissions
        average_pre /= 100 * n_submissions
        average_rec /= 100 * n_submissions
        average_f1 /= 100 * n_submissions

        context["average_acc"] = average_acc
        context["average_pre"] = average_pre
        context["average_rec"] = average_rec
        context["average_f1"] = average_f1
        context["results"] = results
    else:
        context["data_submitted"] = False

    try:
        # get the model specification
        print("getting model")
        model = ML_model.objects.get(pk=model_id)
        print("finishing getting model")
        print(model.model_name)
        specification_file = model.specification
        specification = {}
        context["split_data"] = model.split_data
        context["split_model"] = model.split_model
        print(specification_file)
        if specification_file:
            specification = json.load(specification_file.file)
        context["md_specification"] = specification
    except ObjectDoesNotExist:
        context["md_specification"] = {}
        print("No specification loaded")
    # Get the results from the data uploaded by the admin who created the model
    try:
        result_md = evaluation_result.objects.get(model=model_id, result_type="MD")
        result_file = result_md.result
        data = result_md
        cf = np.loadtxt(result_file, delimiter=",", dtype=int)
        precision, recall, accuracy = get_precision_recall_accuracy(cf)
        context["md_accuracy"] = accuracy
        context["md_precision"] = precision
        context["md_recall"] = recall
        context["data"] = data
        # if precision + recall == 0:
        #     context["md_f1_score"] = np.array([0])
        # else:
        context["md_f1_score"] = 2 * precision * recall / (precision + recall)

        context["md_exists"] = True
    except ObjectDoesNotExist:
        context["md_exists"] = False

    context["model"] = model
    if (model.creator == request.user):
        context["I_am_creator"] = True
        print("I am the creator of this model!")
    else:
        context["I_am_creator"] = False
        print(model.creator, "is the creator of this model!")

    return render(request, 'uploadModel/model_detail.html', context)

def buy_model_detail(request, model_id):
    """
    This method handles the request when user want to see the detail of a model and click on some of the model displayed in the home page.
    :param request: request from user
    :param model_id: which model you are looking for? It's a primary key in the database
    :return: a template together with the context of this model
    """
    # the context for template, contain all the information we need in the front-end. rememember to update it like a dictionary
    context = {}

    # Check if Admin has uploaded data
    try:
        OR = Data.objects.get(relative_model=model_id, data_type="OR")
        if request.user == OR.uploader:
            context["user_data_exists"] = True
        result = evaluation_result.objects.get(model=model_id, data=OR.pk)
        result_file = result.result
        data = result
        cf = np.loadtxt(result_file, delimiter=",", dtype=int)
        precision, recall, accuracy = get_precision_recall_accuracy(cf)
        context["user_accuracy"] = accuracy * 100
        context["user_precision"] = precision[0] * 100
        context["user_recall"] = recall[0] * 100
        context["data"] = data

        # data_sets = Data.objects.all()
        # context = {"data_sets": data_sets}

         # send accuracy and uncertainty
        _accset = ast.literal_eval(result.accset)
        _uncset = ast.literal_eval(result.uncset)
        _new_accset = []
        _new_uncset = []
        for gg in _accset:
            _new_accset.append(gg/100)
        for gg in _uncset:
            _new_uncset.append(gg/100)
        
        

        context["user_accset"] = (_new_accset) 
        context["user_uncset"] = (_new_uncset)
        context["user_au"] = make_acc_unc_json(_new_accset,_new_uncset)
        context["user_ua"] = make_acc_unc_json1(_new_accset,_new_uncset)


        context["user_f1_score"] = 2 * (precision[0] * recall[0]) / (precision[0] + recall[0]) * 100
        

    except ObjectDoesNotExist:
        pass

    with open("data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]

    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )

    results = []
    average_acc = 0
    average_pre = 0
    average_rec = 0
    average_f1 = 0

    context["acc_list"] = []
    context["pre_list"] = []
    context["rec_list"] = []
    context["f1_list"] = []
    context["sub_list"] = []
    context["score_list"] = []

    n_submissions = int(user.functions.getTotalSubmissions(model_id).call())

    if n_submissions > 0:
        context["data_submitted"] = True
        context["dt_exists"] = True
        for i in range(n_submissions):
            result = user.functions.getSubmission(model_id, i).call()   
            average_acc += result[0]
            average_pre += result[1]
            average_rec += result[2]
            average_f1 += result[3]

            context["acc_list"].append(result[0])
            context["pre_list"].append(result[1])
            context["rec_list"].append(result[2])
            context["f1_list"].append(result[3])
            context["score_list"].append(result[4])
            context["sub_list"].append(i)


            wallet_address = str(user.functions.getSubmissionAccount(model_id, i).call())
            if request.user.wallet_address == wallet_address:
                context["user_data_exists"] = True
                # calculate average scores
                context["user_accuracy"] = result[0]
                context["user_precision"] = result[1]
                context["user_recall"] = result[2]
                context["user_f1_score"] = result[3]
                context["user_score"] = result[4]

                 # send accuracy and uncertainty
                accset, uncset = user.functions.getSubmissionAU(model_id, i).call()
                new_accset = []
                new_uncset = []
                for gg in accset:
                    new_accset.append(float(gg)/100)
                for gg in uncset:
                    new_uncset.append(float(gg)/100)

                context["user_accset"] = (new_accset) 
                context["user_uncset"] = (new_uncset)
                context["user_au"] = make_acc_unc_json(new_accset,new_uncset)
                context["user_ua"] = make_acc_unc_json1(new_accset,new_uncset)

            paid = user.functions.getPaid(model_id, i).call()
            results.append([wallet_address, result, paid])

        average_acc /= 100 * n_submissions
        average_pre /= 100 * n_submissions
        average_rec /= 100 * n_submissions
        average_f1 /= 100 * n_submissions

        context["average_acc"] = average_acc
        context["average_pre"] = average_pre
        context["average_rec"] = average_rec
        context["average_f1"] = average_f1
        context["results"] = results
    else:
        context["data_submitted"] = False

    try:
        # get the model specification
        print("getting model")
        model = ML_model.objects.get(pk=model_id)
        print("finishing getting model")
        print(model.model_name)
        specification_file = model.specification
        specification = {}
        context["split_data"] = model.split_data
        context["split_model"] = model.split_model
        print(specification_file)
        if specification_file:
            specification = json.load(specification_file.file)
        context["md_specification"] = specification
    except ObjectDoesNotExist:
        context["md_specification"] = {}
        print("No specification loaded")
    # Get the results from the data uploaded by the admin who created the model
    try:
        result_md = evaluation_result.objects.get(model=model_id, result_type="MD")
        result_file = result_md.result
        data = result_md
        cf = np.loadtxt(result_file, delimiter=",", dtype=int)
        precision, recall, accuracy = get_precision_recall_accuracy(cf)
        context["md_accuracy"] = accuracy
        context["md_precision"] = precision
        context["md_recall"] = recall
        context["data"] = data
        # if precision + recall == 0:
        #     context["md_f1_score"] = np.array([0])
        # else:
        context["md_f1_score"] = 2 * precision * recall / (precision + recall)

        context["md_exists"] = True
    except ObjectDoesNotExist:
        context["md_exists"] = False

    context["model"] = model
    if (model.creator == request.user):
        context["I_am_creator"] = True
        print("I am the creator of this model!")
    else:
        context["I_am_creator"] = False
        print(model.creator, "is the creator of this model!")

    return render(request, 'uploadModel/buy_model_detail.html', context)


def uploading(request):
    """
    upload a model to the server, if the model is valid, redirect to this models' model detail page
    :param request:  request from front-end
    :return: redirect the request to model_detail otherwise redirect the request to homepage
    """
    if request.method == 'POST':
        my_model_form = ModelForm(request.POST, request.FILES, request.FILES)
        if my_model_form.is_valid():
            model_doc = my_model_form.save()
            return redirect(reverse('upload_model:model_detail', args=(model_doc.pk,)))
        else:
            messages.info(request, "The upload model is not valid!")
            return redirect(reverse("upload_model:home"))
    else:
        return redirect(reverse("upload_model:home"))

def download_model(request, model_id):
    model_file = ML_model.objects.get(pk=model_id).model_file.path 
    # file = open('models/SVM car/SVM_car', 'rb')
    file = open(model_file, 'rb')
   
    response = HttpResponse(model_file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="SVM_car"'
    return response

# def buy(request, user_id, model_id):
#     model_file = ML_model.objects.get(pk=model_id).model_file.path 
#     # file = open('models/SVM car/SVM_car', 'rb')
#     User.objects.get(pk=user_id).
#     messages.success(request,
#                                  "Successfully bought the model: {}, with ether: {} !".format(
#                                      model_id, 60))
#     return response


def upload_data_evaluate(request,data_pk):
#     """
#     upload the data provider evaluation 
#     :param request:  request from front-end
#     :return: saty on the same page
#     """
    if request.method == 'POST':
        form = evaluation_result.objects.get(pk=data_pk)
        form.model_score = request.POST['model_score']
        form.data_score = request.POST['data_score']
        form.save()
        messages.success(request,
                                 "Evaluation successfully submitted with model score: {}, data score: {} !".format(
                                     form.model_score, form.data_score))
        return redirect(reverse('upload_model:model_detail', args=(68,)))
        
    #     else:
    #         messages.info(request, "The upload model is not valid!")
    #         return redirect(reverse("upload_model:home"))
    # else:
    #     return redirect(reverse("upload_model:home"))
    return redirect(reverse("upload_model:model_detail", args=(68,)))



def upload_data(request):
    """
    This method handle upload the data. The data being uploaded will get evaluation result in the backend and be popped up to database automatically.
    :param request: the request from user(front-end)
    :return: a redirect to the model detail page which is the model that this data relative to
    """
    import logging
    logging.basicConfig(filename='mylog.log', level=logging.DEBUG)
    if request.method == "POST":
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            form_object = form.save()
            data_file = request.FILES["data_file"]
            model_file = ML_model.objects.get(pk=form_object.relative_model.pk).model_file
            label_file = ML_model.objects.get(pk=form_object.relative_model.pk).label
            split_data = ML_model.objects.get(pk=form_object.relative_model.pk).split_data
            split_model = ML_model.objects.get(pk=form_object.relative_model.pk).split_model
            model, data, label = get_model_and_data(model_file, data_file, label_file)
            # Get the portion of missing data
            missing = get_missing_portion(data)

            print("Missing Portion: " + str(missing))
            # Clear missing data
            data = clear_missing_data(data)
            accset, uncset = get_test_model_accuracy(model, data, label, split_data, split_model)
            try:
                confusion_matrix = get_confusion_matrix(model, data, label)
            except:
                return redirect(reverse("upload_model:error_data"))

            uncertainty = get_uncertainty(model, data, label, split_data)
            similarity = -1
            score = -1

            # user upload data
            if not request.user.get_is_staff():
                f = Data.objects.filter(relative_model=form_object.relative_model, data_type='OR')

                if f.count() == 0:
                    return redirect(reverse("upload_model:error"))

                original_data = Data.objects.get(relative_model=form_object.relative_model, data_type='OR').data_file
                o_data = np.genfromtxt(original_data, delimiter=",", dtype=float, missing_values=None)
                # o_data = np.fromfile(original_data, sep =',')
                weightedAttr = [0.5] * len(data[0])
                scoreWeighting = 0.5

                similarity = get_similarity(o_data, data, weightedAttr)
                # similarity = 0.97
                score = get_score(confusion_matrix, scoreWeighting, similarity)

                print("Similarity: " + str(similarity))
                print("Score: " + str(score))

            # TODO replace this attribute weighting with user input


            file = open("myfile.txt", "w+")
            django_file = File(file)
            for row in confusion_matrix:
                django_file.write(",".join(str(number) for number in row) + "\n")

            if request.user.get_is_staff():
                type = "MD"
            else:
                type = "DT"
            result = evaluation_result(data=form_object, model=form_object.relative_model, result_type=type, \
                                       similarity=similarity, score=score, result=django_file,
                                       document_count=np.sum(confusion_matrix), accset = accset, uncset = uncset)
            result.save()
            django_file.close()
            file.close()
            os.remove("myfile.txt")

            # STORING ON THE BLOCKCHAIN
            if not request.user.get_is_staff():
                wallet_address = w3.toChecksumAddress(request.user.wallet_address)
                sender_id = ML_model.objects.get(pk=form_object.relative_model.pk).creator_id

                User = get_user_model()
                sender = User.objects.get(pk=sender_id).wallet_address
                sender_address = w3.toChecksumAddress(sender)

                # Set default account
                w3.eth.defaultAccount = w3.personal.listAccounts[0]
                # w3.personal.unlockAccount(w3.eth.defaultAccount, '', 15000)
                # Open json file to get contract ABI (Application Binary Interface) and address
                with open("data.json", 'r') as f:
                    datastore = json.load(f)
                abi = datastore["abi"]
                contract_address = datastore["contract_address"]
                # Create the contract instance with the newly-deployed address
                user = w3.eth.contract(
                    address=contract_address, abi=abi,
                )
                result_file = result.result
                cf = np.loadtxt(result_file, delimiter=",", dtype=int)
                precision, recall, accuracy = get_precision_recall_accuracy(cf)
                # Submit the Results
                p = int(precision[0] * 100)
                r = int(recall[0] * 100)
                a = int(accuracy * 100)
                f1 = 2*(p*r)/(p+r)
                if p != 0 and r != 0:
                    f1 = int(2 * p * r / (p + r))
                id = form_object.relative_model.pk
                w3.personal.unlockAccount(w3.personal.listAccounts[0], '', 15000)
                w3.personal.unlockAccount(wallet_address, '', 15000)
                tx_hash = user.functions.submitData(id, wallet_address, a, p, r, f1, int(score), accset, uncset)
                print(tx_hash)
                tx_hash = tx_hash.transact()
                while w3.eth.getTransactionReceipt(tx_hash) == None:
                    print("Waiting to be mined")
                tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
                money = int(score * sigmoid(missing))
                print("money:" + str(money))
                transfer(sender_address, wallet_address, int(form_object.relative_model.pk), money)

                results = {}
                # Store results retrieved from Blockchain and send to data_evaluation page
                results["Accuracy"] = user.functions.getAccuracy(id, wallet_address).call()
                results["Precision"] = user.functions.getPrecision(id, wallet_address).call()
                results["Recall"] = user.functions.getRecall(id, wallet_address).call()
                results["Fscore"] = user.functions.getFscore(id, wallet_address).call()
                results["Rank"] = user.functions.getRank(wallet_address).call()
                results["Total"] = user.functions.getTotalSubmissions(id).call()
                results["accset"] = user.functions.getAccset(id,  wallet_address).call()
                results["uncset"] = user.functions.getUncset(id,  wallet_address).call()
                messages.success(request,
                                 "Data Successfully Submitted to Blockchain! Block Number: {}, Transaction hash: {} Payment successful, sent {} ether to you!".format(
                                     tx_receipt['blockNumber'], tx_receipt['transactionHash'].hex(), int(money) / 100))
            return redirect(reverse("upload_model:model_detail", args=(form_object.relative_model.pk,)))


def delete_model(request, model_id):
    """
    This method triggered by front-end[delete] button. It can only be triggered by Engineer(admin), as a consequence, the model with PK = model_id, its relative data, all the
    relative evaluation results will be deleted.
    :param request:
    :param model_id:  the model id of model to delete
    :return: redirect to home page
    """
    model = ML_model.objects.get(pk=model_id)
    if request.user.is_staff:
        if model is not None:
            model_name = model.model_name
            model.delete()
            messages.success(request, "model {} successfully deleted!".format(model_name))
        else:
            messages.warning(request, "Model doesn't exist")
    else:
        messages.warning(request, "You are not authorised for this action!")
    return redirect(reverse("upload_model:home"))


def reward(request, receiver, id, value):
    sender_address = w3.toChecksumAddress(request.user.wallet_address)
    receiver_address = w3.toChecksumAddress(receiver)

    w3.personal.unlockAccount(sender_address, '')
    w3.personal.unlockAccount(receiver_address, '')

    amount = w3.toWei(value / 100, "ether")
    w3.eth.sendTransaction({'from': sender_address, 'to': receiver_address, 'value': amount})
    # print("Sender Balance: {}".format(w3.fromWei(w3.eth.getBalance(sender_address), 'ether')), "Reciever Balance: {}".format(w3.fromWei(w3.eth.getBalance(receiver_address), 'ether')))

    w3.personal.lockAccount(receiver_address)
    w3.personal.lockAccount(sender_address)

    # Mark this submission as having been paid for
    w3.eth.defaultAccount = w3.personal.listAccounts[0]
    w3.personal.unlockAccount(w3.eth.defaultAccount, '', 15000)

    with open("data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]
    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )

    tx_hash = user.functions.setPaid(id, receiver_address)
    print(tx_hash)
    tx_hash = tx_hash.transact()
    w3.personal.lockAccount(w3.eth.defaultAccount)
    messages.success(request,
                     "Payment successful, sent {} ether to {}".format(w3.fromWei(amount, 'ether'), receiver_address))
    return redirect(reverse("upload_model:model_detail", args=(id,)))


def transfer(sender_address, receiver_address, id, value):
    w3.personal.unlockAccount(sender_address, '')
    w3.personal.unlockAccount(receiver_address, '')

    amount = w3.toWei(value / 100, "ether")
    w3.eth.sendTransaction({'from': sender_address, 'to': receiver_address, 'value': amount})
    # print("Sender Balance: {}".format(w3.fromWei(w3.eth.getBalance(sender_address), 'ether')), "Reciever Balance: {}".format(w3.fromWei(w3.eth.getBalance(receiver_address), 'ether')))

    w3.personal.lockAccount(receiver_address)
    w3.personal.lockAccount(sender_address)

    # Mark this submission as having been paid for
    w3.eth.defaultAccount = w3.personal.listAccounts[0]
    w3.personal.unlockAccount(w3.eth.defaultAccount, '', 15000)

    with open("data.json", 'r') as f:
        datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["contract_address"]
    user = w3.eth.contract(
        address=contract_address, abi=abi,
    )

    tx_hash = user.functions.setPaid(id, receiver_address)
    print(tx_hash)
    tx_hash = tx_hash.transact()
    w3.personal.lockAccount(w3.eth.defaultAccount)

def make_acc_unc_json(acc, unc):
    a_u_json = []
    for i in range(len(acc)):
        temp = [unc[i],acc[i]]
        a_u_json.append(temp)
    a_u_json.sort()
    json_final = json.dumps(a_u_json)
    return json_final

def make_acc_unc_json1(acc, unc):
    a_u_json = []
    for i in range(len(acc)):
        temp = [unc[i],acc[i]]
        a_u_json.append(temp)
    a_u_json.sort(key=lambda x:x[1])
    json_final = json.dumps(a_u_json)
    return json_final


