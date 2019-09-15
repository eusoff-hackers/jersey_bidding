from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime

# local
from jersey_bidder.models import User, Choice, JerseyNumber
from jersey_bidder.useradmin.forms import allocateForm
from jersey_bidder import db
from jersey_bidder.useradmin.utils import allocateByYear, generateMaleList, generateFemaleList, splitMaleAndFemale, availNumbers

useradmin = Blueprint('useradmin', __name__)

@useradmin.route("/useradmin/home", methods=['GET', 'POST'])
def adminHome():
    return render_template('adminHome.html')

@useradmin.route("/useradmin/allocate", methods=['GET', 'POST'])
def adminAllocate():
    form = allocateForm()
    form.yearToAllocate.choices = [(1, 1), (2, 2), (3, 3), (4, 4)]

    if form.validate_on_submit():
        failedAllocateUsers = allocateByYear(form.yearToAllocate.data)
        if failedAllocateUsers != None:

            overallStats = {}
            totalUserInYear = User.query.filter(
                User.year == form.yearToAllocate.data).count()

            totalAllocatedUserInYear = User.query.filter(
                (User.year == form.yearToAllocate.data) & (User.jerseyNumber_id != None)).count()

            overallStats.update({'totalUserInYear': totalUserInYear})
            overallStats.update(
                {'totalAllocatedUserInYear': totalAllocatedUserInYear})

            maleAndFemaleTuple = splitMaleAndFemale(failedAllocateUsers)
            failedMaleList = maleAndFemaleTuple[0]
            failedFemaleList = maleAndFemaleTuple[1]

            return render_template('allocateFailure.html', failedMales=failedMaleList, failedFemales=failedFemaleList, overallStats=overallStats)

        successMessage = "successfully allocated year " + \
            str(form.yearToAllocate.data) + " students"

        allUsersInYear = User.query.filter(
            User.year == form.yearToAllocate.data).all()
        return render_template('allocateSuccess.html', successMessage=successMessage, allUsersInYear=allUsersInYear)

    return render_template('allocatePage.html', form=form)


@useradmin.route("/useradmin/checkresult/male", methods=['GET', 'POST'])
def fullResultMale():
    list = generateMaleList()
    return render_template('fullResultMale.html', list=list)


@useradmin.route("/useradmin/checkresult/female", methods=['GET', 'POST'])
def fullResultFemale():
    list = generateFemaleList()
    return render_template('fullResultFemale.html', list=list)

@useradmin.route("/useradmin/checkresult/availJersey", methods=['GET', 'POST'])
def viewAvailNumbers():
    weiboon = User.query.get(4)
    listOfAvailNumbers = availNumbers(weiboon)
    return render_template('availNumbers.html', availNumbers=listOfAvailNumbers)