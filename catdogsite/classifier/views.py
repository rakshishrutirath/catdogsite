import os
import cv2
import joblib
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import UploadHistory

IMG_SIZE = 64
MODEL_PATH = os.path.join(settings.BASE_DIR, "cat_dog_model.pkl")
model = joblib.load(MODEL_PATH)


@login_required
def predict_image(request):
    result = None
    if request.method == "POST" and request.FILES.get("photo"):
        uploaded_file = request.FILES["photo"]

        # save it to a temp path just to run the prediction
        temp_path = os.path.join(settings.BASE_DIR, "temp_upload.jpg")
        with open(temp_path, "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        img = cv2.imread(temp_path)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img.flatten().reshape(1, -1)

        prediction = model.predict(img)[0]
        result = "Dog 🐶" if prediction == 1 else "Cat 🐱"

        os.remove(temp_path)

        # save a permanent history record — note uploaded_file.seek(0)
        # is needed because we already "read" the file above with .chunks()
        uploaded_file.seek(0)
        UploadHistory.objects.create(
            user=request.user,
            image=uploaded_file,
            result=result,
        )

    return render(request, "classifier/index.html", {"result": result})


@login_required
def history(request):
    entries = UploadHistory.objects.filter(user=request.user)
    return render(request, "classifier/history.html", {"entries": entries})