
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import MusicianProfile, MusicianService, NIGERIAN_STATES
from .forms import MusicianProfileForm


@login_required
def create_profile(request):
    if not request.user.can_provide_services:
        messages.error(
            request,
            "You need a service-provider account to create a musician profile."
        )
        return redirect("home")

    if MusicianProfile.objects.filter(user=request.user).exists():
        messages.info(
            request,
            "You already have a musician profile."
        )
        return redirect("home")

    if request.method == "POST":
        form = MusicianProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            messages.success(
                request,
                "Your musician profile has been created successfully!"
            )
            return redirect("home")
    else:
        form = MusicianProfileForm()

    return render(
        request,
        "musicians/create_profile.html",
        {"form": form},
    )


@login_required
def edit_profile(request):
    try:
        profile = request.user.musicianprofile
    except MusicianProfile.DoesNotExist:
        messages.info(
            request,
            "Create your musician profile to get started."
        )
        return redirect("create_profile")

    if not request.user.can_provide_services:
        messages.error(
            request,
            "You need a service-provider account to edit a musician profile."
        )
        return redirect("home")

    if request.method == "POST":
        form = MusicianProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your musician profile has been updated."
            )
            return redirect("home")
    else:
        form = MusicianProfileForm(instance=profile)

    return render(
        request,
        "musicians/edit_profile.html",
        {"form": form, "profile": profile},
    )


def browse_musicians(request):
    musicians = MusicianProfile.objects.filter(
        is_available=True
    ).prefetch_related("services")

    instrument = request.GET.get("instrument", "").strip()
    state = request.GET.get("state", "").strip()
    event_date = request.GET.get("date", "").strip()

    if instrument:
        musicians = musicians.filter(
            services__instrument=instrument,
            services__is_active=True,
        ).distinct()

    if state:
        musicians = musicians.filter(state=state)

    context = {
        "musicians": musicians,
        "selected_instrument": instrument,
        "selected_state": state,
        "event_date": event_date,
        "instruments": MusicianService.Instrument.choices,
        "states": NIGERIAN_STATES,
    }

    return render(
        request,
        "musicians/browse_musicians.html",
        context,
    )


def musician_detail(request, pk):
    musician = get_object_or_404(
        MusicianProfile.objects.prefetch_related("services"),
        pk=pk,
        is_available=True,
    )

    services = musician.services.filter(is_active=True)

    return render(
        request,
        "musicians/musician_detail.html",
        {
            "musician": musician,
            "services": services,
        },
    )
