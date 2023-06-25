from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import View
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['tier', 'tokens_balance']

class RegisterView(View):
    def get(self, request):
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
        return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
        
from django.contrib.auth.decorators import login_required

@login_required
def generate_content(request):
    profile = request.user.userprofile
    if profile.tokens_balance > 0:
        # Deduct a token from the user's balance
        profile.tokens_balance -= 1
        profile.save()
        # Check user's tier and generate content accordingly
        if profile.tier == 1:
            content = generate_tier1_content()
        elif profile.tier == 2:
            content = generate_tier2_content()
        elif profile.tier == 3:
            content = generate_tier3_content()
        elif profile.tier == 4:
            content = generate_tier4_content()
        return render(request, 'content.html', {'content': content})
    else:
        return redirect('purchase_tokens')

def generate_tier1_content():
    # Generate content for tier 1 users
    pass

def generate_tier2_content():
    # Generate content for tier 2 users
    pass

def generate_tier3_content():
    # Generate content for tier 3 users
    pass

def generate_tier4_content():
    # Generate content for tier 4 users
    pass

import openai

openai.api_key = "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"


def generate_tier1_content():
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt="Translate this English text to French: '{text}'",
      max_tokens=60
    )
    return response.choices[0].text.strip()

def generate_tier2_content():
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt="Write a blog post about the benefits of exercising regularly.",
      max_tokens=500
    )
    return response.choices[0].text.strip()

def generate_tier3_content():
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt="Summarize this research paper: '{text}'",
      max_tokens=200
    )
    return response.choices[0].text.strip()

def generate_tier4_content():
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt="Write a short story based on this prompt: 'In a world where humans coexist with AI...'",
      max_tokens=1000
    )
    return response.choices[0].text.strip()


from django import forms
from djstripe.models import PaymentIntent
from djstripe.settings import djstripe_settings
from djstripe.exceptions import CardError, PaymentError

class PurchaseTokensForm(forms.Form):
    token_amount = forms.ChoiceField(choices=[(i, i) for i in range(1, 11)])
    stripe_card = forms.StripeCardField()

def purchase_tokens(request):
    if request.method == 'POST':
        form = PurchaseTokensForm(request.POST)
        if form.is_valid():
            try:
                payment_intent = PaymentIntent.create(
                    amount=int(form.cleaned_data['token_amount']) * 100, # 1 token = 1 dollar
                    currency='usd',
                    payment_method=form.cleaned_data['stripe_card'].fingerprint,
                    confirm=True
                )
                if payment_intent.status == 'succeeded':
                    request.user.userprofile.tokens_balance += int(form.cleaned_data['token_amount'])
                    request.user.userprofile.save()
                    return redirect('content_generation')
            except (CardError, PaymentError) as e:
                form.add_error(None, e.user_message)
    else:
        form = PurchaseTokensForm()
    return render(request, 'purchase_tokens.html', {'form': form})
