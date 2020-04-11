from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm,  AccountAuthenticationForm, AccountUpdateForm
from account.models import Account
from account.scraper import Scraper, Source

theGuardian = Source(
    "The Guardian",
    "https://www.theguardian.com",
    ("div", "fc-item__container"),
    ("span", "js-headline-text"),
    ("div", "fc-item__standfirst"),
    ("a", "fc-item__link"),
    ("source", "srcset")
)

bbc = Source(
    "BBC",
    "https://www.bbc.co.uk/news",
    ("div", "gs-c-promo gs-t-News nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline gs-c-promo--stacked@m gs-c-promo--flex"),
    ("h3", "gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"),
    ("p", "gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary gs-u-display-none gs-u-display-block@m"),
    ("a", "gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"),
    ("img", "src")
)

theIndependent = Source(
    "The Independent",
    "https://www.independent.co.uk",
    ("div", "article type-article media-image"),
    ("h2", ""),
    ("", ""),
    ("a", ""),
    ("amp-img", "amp-img img-focal-center i-amphtml-layout-responsive i-amphtml-layout-size-defined i-amphtml-element i-amphtml-layout")
)

sources = []
sources.append(theGuardian)
sources.append(bbc)
#sources.append(theIndependent)

categories = []
categories.append("politics")
categories.append("sport")
#categories.append("coronavirus")

def registration(request):
    context = {}

    if request.user.is_authenticated: # If user is logged in, redirect to home screen, they cannot register again!
        return redirect('home')
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else: # GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)

### HOME VIEW ###
def home(request):
    context = {}
    accounts = Account.objects.all()
    context['accounts'] = accounts

    scraper = Scraper(sources, categories)

    # checkRecent can take a "force-scrape" parameter to enforce the scraper to always scrape
    # if scraper.checkRecent("force-scrape"):
    if scraper.checkRecent("force-scrape"):
        print("Force Scraping")
    else:
        scraper.search()

    return render(request, 'home.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'accounts/login.html', context)

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['success_message'] = "Updated"
    else: # Display the saved user details from database
        form = AccountUpdateForm(
                                initial = {
                                'username':request.user.username,
                                "guardianSource": request.user.guardianSource,
                                "bbcSource": request.user.bbcSource,
                                "independentSource": request.user.independentSource,

                                "categoryCoronaVirus": request.user.categoryCoronaVirus,
                                "categoryPolitics": request.user.categoryPolitics,
                                "categorySport": request.user.categorySport,
                                            })
    context['account_form'] = form
    return render(request, 'accounts/account.html', context)

# Create your views here.
