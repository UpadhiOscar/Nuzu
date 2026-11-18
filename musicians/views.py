from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from .models import (
    MusicianProfile,
    MusicianService,
    NIGERIAN_STATES,
    PortfolioPhoto,
    PortfolioVideo,
)
from .forms import (
    MusicianProfileForm,
    PortfolioPhotoForm,
    PortfolioVideoForm,
)


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



@never_cache
@login_required
def edit_profile(request, pk):
    if not request.user.can_provide_services:
        messages.error(
            request,
            "You need a service-provider account to edit a musician profile."
        )
        return redirect("home")

    profile = get_object_or_404(
        MusicianProfile,
        pk=pk,
        user=request.user,
    )

    photo_form = PortfolioPhotoForm()
    video_form = PortfolioVideoForm()
    form = MusicianProfileForm(instance=profile)

    if request.method == "POST":
        action = request.POST.get("action")

        # Update musician information
        if action == "update_profile":
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
                return redirect("musician_detail", pk=profile.pk)

        # Upload photograph
        elif action == "upload_photo":
            photo_form = PortfolioPhotoForm(
                request.POST,
                request.FILES,
            )

            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.musician = profile
                photo.save()

                messages.success(request, "Photo uploaded successfully!")
                return redirect("edit_profile", pk=profile.pk)

        # Upload video
        elif action == "upload_video":
            video_form = PortfolioVideoForm(
                request.POST,
                request.FILES,
            )

            if video_form.is_valid():
                video = video_form.save(commit=False)
                video.musician = profile
                video.save()

                messages.success(request, "Video uploaded successfully!")
                return redirect("edit_profile", pk=profile.pk)
            else:
                print("VIDEO FORM ERRORS:", video_form.errors)
                print("UPLOADED FILES:", request.FILES)

        # Update photograph
        elif action == "update_photo":
            photo = get_object_or_404(
                profile.portfolio_photos,
                pk=request.POST.get("photo_id"),
            )

            photo_form = PortfolioPhotoForm(
                request.POST,
                request.FILES,
                instance=photo,
            )

            if photo_form.is_valid():
                photo_form.save()
                messages.success(request, "Photo updated successfully!")
                return redirect("edit_profile", pk=profile.pk)

        # Delete photograph
        elif action == "delete_photo":
            photo = get_object_or_404(
                profile.portfolio_photos,
                pk=request.POST.get("photo_id"),
            )
            photo.delete()

            messages.success(request, "Photo deleted successfully!")
            return redirect("edit_profile", pk=profile.pk)

        # Update video
        elif action == "update_video":
            video = get_object_or_404(
                profile.portfolio_videos,
                pk=request.POST.get("video_id"),
            )

            video_form = PortfolioVideoForm(
                request.POST,
                request.FILES,
                instance=video,
            )

            if video_form.is_valid():
                video_form.save()
                messages.success(request, "Video updated successfully!")
                return redirect("edit_profile", pk=profile.pk)
            else:
                print("VIDEO UPDATE FORM ERRORS:", video_form.errors)
                print("UPLOADED FILES:", request.FILES)

        # Delete video
        elif action == "delete_video":
            video = get_object_or_404(
                profile.portfolio_videos,
                pk=request.POST.get("video_id"),
            )
            video.delete()

            messages.success(request, "Video deleted successfully!")
            return redirect("edit_profile", pk=profile.pk)

    # Fetch fresh portfolio records from the database
    photos = PortfolioPhoto.objects.filter(
        musician=profile
    ).order_by("-uploaded_at")

    videos = PortfolioVideo.objects.filter(
        musician=profile
    ).order_by("-uploaded_at")

    return render(
        request,
        "musicians/edit_profile.html",
        {
            "form": form,
            "profile": profile,
            "musician": profile,
            "photos": photos,
            "videos": videos,
            "photo_form": photo_form,
            "video_form": video_form,
        },
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
        MusicianProfile.objects.prefetch_related(
            "services",
            "portfolio_photos",
            "portfolio_videos",
        ),
        pk=pk,
        is_available=True,
    )

    services = musician.services.filter(is_active=True)
    photos = musician.portfolio_photos.all()
    videos = musician.portfolio_videos.all()

    return render(
        request,
        "musicians/musician_detail.html",
        {
            "musician": musician,
            "services": services,
            "photos": photos,
            "videos": videos,
        },
    )


@login_required
def manage_portfolio(request, pk):
    musician = get_object_or_404(
        MusicianProfile,
        pk=pk,
        user=request.user,
    )

    photo_form = PortfolioPhotoForm()
    video_form = PortfolioVideoForm()

    editing_photo = None
    editing_video = None

    if request.method == "POST":
        action = request.POST.get("action")

        # Upload a new photograph
        if action == "upload_photo":
            photo_form = PortfolioPhotoForm(
                request.POST,
                request.FILES,
            )

            if photo_form.is_valid():
                photo = photo_form.save(commit=False)
                photo.musician = musician
                photo.save()

                messages.success(request, "Photo uploaded successfully!")
                return redirect("manage_portfolio", pk=musician.pk)

        # Upload a new video
        elif action == "upload_video":
            video_form = PortfolioVideoForm(
                request.POST,
                request.FILES,
            )

            if video_form.is_valid():
                video = video_form.save(commit=False)
                video.musician = musician
                video.save()

                messages.success(request, "Video uploaded successfully!")
                return redirect("manage_portfolio", pk=musician.pk)
            else:
                print("VIDEO FORM ERRORS:", video_form.errors)
                print("UPLOADED FILES:", request.FILES)

        # Edit or replace an existing photograph
        elif action == "update_photo":
            photo = get_object_or_404(
                musician.portfolio_photos,
                pk=request.POST.get("photo_id"),
            )

            photo_form = PortfolioPhotoForm(
                request.POST,
                request.FILES,
                instance=photo,
            )

            if photo_form.is_valid():
                photo_form.save()
                messages.success(request, "Photo updated successfully!")
                return redirect("manage_portfolio", pk=musician.pk)

            editing_photo = photo

        # Delete a photograph
        elif action == "delete_photo":
            photo = get_object_or_404(
                musician.portfolio_photos,
                pk=request.POST.get("photo_id"),
            )
            photo.delete()

            messages.success(request, "Photo deleted successfully!")
            return redirect("manage_portfolio", pk=musician.pk)

        # Edit or replace an existing video
        elif action == "update_video":
            video = get_object_or_404(
                musician.portfolio_videos,
                pk=request.POST.get("video_id"),
            )

            video_form = PortfolioVideoForm(
                request.POST,
                request.FILES,
                instance=video,
            )

            if video_form.is_valid():
                video_form.save()
                messages.success(request, "Video updated successfully!")
                return redirect("manage_portfolio", pk=musician.pk)

            editing_video = video

        # Delete a video
        elif action == "delete_video":
            video = get_object_or_404(
                musician.portfolio_videos,
                pk=request.POST.get("video_id"),
            )
            video.delete()

            messages.success(request, "Video deleted successfully!")
            return redirect("manage_portfolio", pk=musician.pk)

    photos = musician.portfolio_photos.all()
    videos = musician.portfolio_videos.all()

    return render(
        request,
        "musicians/manage_portfolio.html",
        {
            "musician": musician,
            "photos": photos,
            "videos": videos,
            "photo_form": photo_form,
            "video_form": video_form,
            "editing_photo": editing_photo,
            "editing_video": editing_video,
        },
    )
