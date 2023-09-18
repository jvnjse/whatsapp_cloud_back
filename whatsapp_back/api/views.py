import requests, json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .serializers import (
    PhoneNumberSerializer,
    ExcelSerializer,
    ExcelImageSerializer,
    WhatsAppBulkMessageSerializer,
    WhatsAppBulkMessageImageSerializer,
    MessageTemplateSerializer,
    ImageUploadSerializer,
    CustomUserSerializer,
    UserLoginSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PhoneNumber, CustomUser
from openpyxl import load_workbook
from decouple import config

my_token = "your_verify_token"
bearer_token = config("TOKEN")
phone_number_id = config("PHONE_NO_ID")
business_id = config("BUSINESS_ID")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = {
                "message": "User registered successfully",
                "user": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = get_tokens_for_user(user)
            return Response(
                {
                    "token": token,
                    "is_manager": user.is_staff,
                    "message": "Login successful",
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def image_upload(request):
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def upload_image(request):
    url1 = (
        "https://graph.facebook.com/v18.0/2019843135044267/uploads?access_token="
        + bearer_token
        + "&file_length=0&file_type=image/jpg"
    )

    response1 = requests.post(url1)

    if response1.status_code != 200:
        return JsonResponse(
            {"error": "Failed to make the first POST request"}, status=500
        )

    try:
        response1_data = response1.json()
        upload_session_key = response1_data["id"]
    except ValueError:
        return JsonResponse({"error": "Invalid JSON in the first response"}, status=500)

    serializer = ImageUploadSerializer(data=request.data)
    if serializer.is_valid():
        image_file = serializer.validated_data["image_file"]

        url2 = "https://graph.facebook.com/v18.0/" + upload_session_key

        headers = {
            "Authorization": "OAuth " + bearer_token,
        }

        files = {"source": image_file}

        # Step 4: Make the second POST request to upload the image
        response2 = requests.post(url2, headers=headers, data=image_file)

        if response2.status_code != 200:
            return JsonResponse({"error": response2.json()}, status=500)

        # Step 5: Extract and return the JSON data from the second response
        try:
            response2_data = response2.json()
            return JsonResponse(response2_data)
        except ValueError:
            return JsonResponse(
                {"error": "Invalid JSON in the second response"}, status=500
            )

    return JsonResponse({"error": "Invalid data"}, status=400)


@api_view(["POST"])
def delete_template(request):
    try:
        template_name = request.GET.get("template_name")
        cleaned_string = template_name.replace('"', "")

        url = (
            "https://graph.facebook.com/v17.0/"
            + business_id
            + "/message_templates?name="
            + cleaned_string
        )
        print(url)
        headers = {
            "Authorization": "Bearer " + bearer_token,
            "Content-Type": "application/json",
        }
        response = requests.request("DELETE", url, headers=headers)
        response_data = response.json()
        return Response(
            {"message": response_data},
            status=status.HTTP_201_CREATED,
        )

    except:
        return HttpResponse("ERROR")


def index(request):
    # print(bearer_token)
    return HttpResponse("OK")


class PhoneNumberList(APIView):
    def get(self, request, format=None):
        phone_numbers = PhoneNumber.objects.all()
        serializer = PhoneNumberSerializer(phone_numbers, many=True)
        numbers = [item["number"] for item in serializer.data]
        return Response(numbers, status=status.HTTP_200_OK)


# numbers upload from excel
class PhoneNumberUpload(APIView):
    def post(self, request, format=None):
        serializer = ExcelSerializer(data=request.data)

        if serializer.is_valid():
            excel_file = serializer.validated_data["excel_file"]
            workbook = load_workbook(excel_file, read_only=True)
            worksheet = workbook.active

            for row in worksheet.iter_rows(values_only=True):
                raw_number = str(row[0])
                # print(raw_number)
                # replace 0 and add +91
                if raw_number.startswith("0"):
                    raw_number = "+91" + raw_number[1:]
                    # print(raw_number)
                # if no +91 add +91
                if not raw_number.startswith("+91"):
                    raw_number = "+91" + raw_number
                # model save
                PhoneNumber.objects.get_or_create(number=raw_number)

            return Response(
                {"message": "Phone numbers imported successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # class PhoneNumberUpload(APIView):


@api_view(["POST"])
def excel_sent_message(request):
    try:
        serializer = ExcelSerializer(data=request.data)

        if serializer.is_valid():
            excel_file = serializer.validated_data["excel_file"]
            template_name = serializer.validated_data["template_name"]
            workbook = load_workbook(excel_file, read_only=True)
            worksheet = workbook.active
            results = []

            for row in worksheet.iter_rows(values_only=True):
                raw_number = str(row[0])
                # replace 0 and add +91
                if raw_number.startswith("0"):
                    raw_number = "+91" + raw_number[1:]
                # if no +91 add +91
                if not raw_number.startswith("+91"):
                    raw_number = "+91" + raw_number
                # model save
                # PhoneNumber.objects.get_or_create(number=raw_number)
                PhoneNumber.objects.get_or_create(number=raw_number)

                data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": raw_number,
                    "type": "template",
                    "template": {"name": template_name, "language": {"code": "en"}},
                }
                # print(data)

                url = (
                    "https://graph.facebook.com/v17.0/" + phone_number_id + "/messages"
                )
                headers = {
                    "Authorization": "Bearer " + bearer_token,
                    "Content-Type": "application/json",
                }

                try:
                    response = requests.post(url, headers=headers, json=data)
                    response_data = response.json()
                    results.append(response_data)

                except json.JSONDecodeError:
                    return JsonResponse({"error": "Invalid JSON data"}, status=400)
                return Response(
                    {"message": "Phone numbers imported successfully"},
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
def excel_sent_message_images(request):
    try:
        serializer = ExcelImageSerializer(data=request.data)

        if serializer.is_valid():
            excel_file = serializer.validated_data["excel_file"]
            template_name = serializer.validated_data["template_name"]
            image_link = serializer.validated_data["image_link"]

            workbook = load_workbook(excel_file, read_only=True)
            worksheet = workbook.active
            results = []

            for row in worksheet.iter_rows(values_only=True):
                raw_number = str(row[0])
                # replace 0 and add +91
                if raw_number.startswith("0"):
                    raw_number = "+91" + raw_number[1:]
                # if no +91 add +91
                if not raw_number.startswith("+91"):
                    raw_number = "+91" + raw_number
                # model save
                # PhoneNumber.objects.get_or_create(number=raw_number)
                PhoneNumber.objects.get_or_create(number=raw_number)

                data = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": raw_number,
                    "type": "template",
                    "template": {
                        "name": template_name,
                        "components": [
                            {
                                "type": "HEADER",
                                # "format": "IMAGE",
                                "parameters": [
                                    {
                                        "type": "image",
                                        "image": {"link": image_link},
                                    }
                                ],
                            }
                        ],
                        "language": {"code": "en"},
                    },
                }
                # print(data)

                url = (
                    "https://graph.facebook.com/v17.0/" + phone_number_id + "/messages"
                )
                headers = {
                    "Authorization": "Bearer " + bearer_token,
                    "Content-Type": "application/json",
                }

                try:
                    response = requests.post(url, headers=headers, json=data)
                    response_data = response.json()
                    results.append(response_data)

                except json.JSONDecodeError:
                    return JsonResponse({"error": "Invalid JSON data"}, status=400)
                return Response(
                    {"message": "Phone numbers imported successfully"},
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
def excel_upload_message(request):
    try:
        serializer = ExcelSerializer(data=request.data)

        if serializer.is_valid():
            excel_file = serializer.validated_data["excel_file"]
            workbook = load_workbook(excel_file, read_only=True)
            worksheet = workbook.active
            results = []

            for row in worksheet.iter_rows(values_only=True):
                raw_number = str(row[0])
                # replace 0 and add +91
                if raw_number.startswith("0"):
                    raw_number = "+91" + raw_number[1:]
                # if no +91 add +91
                if not raw_number.startswith("+91"):
                    raw_number = "+91" + raw_number
                # model save
                # PhoneNumber.objects.get_or_create(number=raw_number)
                # print(raw_number)
                PhoneNumber.objects.get_or_create(number=raw_number)

            return Response(
                {"message": "Phone numbers imported successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# send bulk messages manually
@api_view(["POST"])
def send_whatsapp_bulk_messages(request):
    try:
        serializer = WhatsAppBulkMessageSerializer(data=request.data)

        if serializer.is_valid():
            template_name = serializer.validated_data.get("template_name")
            numbers = serializer.validated_data.get("numbers")
            # print(template_name)
            results = []

        for number in numbers:
            if number.startswith("0"):
                number = "+91" + number[1:]

            if not number.startswith("+91"):
                number = "+91" + number

            if not number:
                results.append({"error": "Missing 'number' parameter"})
                continue
            PhoneNumber.objects.get_or_create(number=number)

            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "template",
                "template": {"name": template_name, "language": {"code": "en"}},
            }
            url = "https://graph.facebook.com/v17.0/" + phone_number_id + "/messages"
            headers = {
                "Authorization": "Bearer " + bearer_token,
                "Content-Type": "application/json",
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response_data = response.json()
                results.append(response_data)
            except requests.exceptions.RequestException as e:
                results.append({"error": str(e)})
            except json.JSONDecodeError:
                results.append({"error": "Invalid JSON data"})

        for i, result in enumerate(results):
            if not isinstance(result, dict):
                results[i] = {"error": str(result)}

        return JsonResponse(results, status=200, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# image
@api_view(["POST"])
def send_whatsapp_bulk_messages_images(request):
    try:
        serializer = WhatsAppBulkMessageImageSerializer(data=request.data)

        if serializer.is_valid():
            template_name = serializer.validated_data.get("template_name")
            numbers = serializer.validated_data.get("numbers")
            image_link = serializer.validated_data.get("image_link")

            # print(template_name)
            results = []

        for number in numbers:
            if number.startswith("0"):
                number = "+91" + number[1:]

            if not number.startswith("+91"):
                number = "+91" + number

            if not number:
                results.append({"error": "Missing 'number' parameter"})
                continue
            PhoneNumber.objects.get_or_create(number=number)

            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "components": [
                        {
                            "type": "HEADER",
                            # "format": "IMAGE",
                            "parameters": [
                                {
                                    "type": "image",
                                    "image": {"link": image_link},
                                }
                            ],
                        }
                    ],
                    "language": {"code": "en"},
                },
            }
            url = "https://graph.facebook.com/v17.0/" + phone_number_id + "/messages"
            headers = {
                "Authorization": "Bearer " + bearer_token,
                "Content-Type": "application/json",
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response_data = response.json()
                results.append(response_data)
            except requests.exceptions.RequestException as e:
                results.append({"error": str(e)})
            except json.JSONDecodeError:
                results.append({"error": "Invalid JSON data"})

        for i, result in enumerate(results):
            if not isinstance(result, dict):
                results[i] = {"error": str(result)}

        return JsonResponse(results, status=200, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# send bulk messages from addded names from database
@api_view(["POST"])
def send_whatsapp_model_bulk_messages(request):
    try:
        template_name = request.GET.get("template_name")
        get_numbers = PhoneNumber.objects.values_list("number", flat=True)
        numbers = list(get_numbers)
        # print(template_name)

        if not numbers or not isinstance(numbers, list):
            return JsonResponse(
                {"error": "Missing or invalid 'numbers' parameter"}, status=400
            )
        results = []

        for number in numbers:
            if not number:
                results.append({"error": "Missing 'number' parameter"})
                continue

            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "template",
                "template": {"name": template_name, "language": {"code": "en"}},
            }

            url = "https://graph.facebook.com/v17.0/" + phone_number_id + "/messages"
            headers = {
                "Authorization": "Bearer " + bearer_token,
                "Content-Type": "application/json",
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response_data = response.json()
                results.append(response_data)
            except requests.exceptions.RequestException as e:
                results.append({"error": str(e)})
            except json.JSONDecodeError:
                results.append({"error": "Invalid JSON data"})

        for i, result in enumerate(results):
            if not isinstance(result, dict):
                results[i] = {"error": str(result)}

        return JsonResponse(results, status=200, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# send bulk messages from addded names from database
@api_view(["POST"])
def send_whatsapp_model_bulk_messages_images(request):
    try:
        template_name = request.GET.get("template_name")
        image_url = request.GET.get("image_url")
        print(image_url)
        print(template_name)
        get_numbers = PhoneNumber.objects.values_list("number", flat=True)
        numbers = list(get_numbers)
        # print(template_name)

        if not numbers or not isinstance(numbers, list):
            return JsonResponse(
                {"error": "Missing or invalid 'numbers' parameter"}, status=400
            )
        results = []

        for number in numbers:
            if not number:
                results.append({"error": "Missing 'number' parameter"})
                continue

            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "components": [
                        {
                            "type": "HEADER",
                            # "format": "IMAGE",
                            "parameters": [
                                {
                                    "type": "image",
                                    "image": {"link": image_url},
                                }
                            ],
                        }
                    ],
                    "language": {"code": "en"},
                },
            }
            print(data)

            url = "https://graph.facebook.com/v17.0/" + phone_number_id + "/messages"
            headers = {
                "Authorization": "Bearer " + bearer_token,
                "Content-Type": "application/json",
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response_data = response.json()
                results.append(response_data)
            except requests.exceptions.RequestException as e:
                results.append({"error": str(e)})
            except json.JSONDecodeError:
                results.append({"error": "Invalid JSON data"})

        for i, result in enumerate(results):
            if not isinstance(result, dict):
                results[i] = {"error": str(result)}

        return JsonResponse(results, status=200, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# get templates
def get_templates_message(request):
    url = "https://graph.facebook.com/v17.0/" + business_id + "/message_templates"
    headers = {
        "Authorization": "Bearer " + bearer_token,
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        templates = data.get("data", [])

        names = [template.get("name", "") for template in templates]
        components = [template.get("components", []) for template in templates]

        name_response = {"names": names, "components": components}

        # print(data)
        return JsonResponse({"data": name_response})
        # return JsonResponse({"data": templates})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def get_templates_list(request):
    url = "https://graph.facebook.com/v17.0/" + business_id + "/message_templates"
    headers = {
        "Authorization": "Bearer " + bearer_token,
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        templates = data.get("data", [])

        names = [template.get("name", "") for template in templates]
        components = [template.get("components", []) for template in templates]

        name_response = {"names": names, "components": components}

        # print(data)
        return JsonResponse({"data": templates})
        # return JsonResponse({"data": name_response})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["POST"])
def create_text_template(request):
    facebook_api_url = (
        "https://graph.facebook.com/v17.0/" + business_id + "/message_templates"
    )
    serializer = MessageTemplateSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        template_name = data.get("template_name")
        header_text = data.get("header_text")
        body_text = data.get("body_text")
        footer_text = data.get("footer_text")

        post_data = json.dumps(
            {
                "name": template_name,
                "category": "MARKETING",
                "language": "en",
                "components": [
                    {"type": "HEADER", "text": header_text},
                    {"type": "BODY", "text": body_text},
                    {"type": "FOOTER", "text": footer_text},
                ],
            }
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + bearer_token,
        }

        response = requests.post(facebook_api_url, data=post_data, headers=headers)
        response_data = response.json()

        if response.status_code == status.HTTP_200_OK:
            return Response(
                {"message": response_data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": response_data},
                status=response.status_code,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_image_template(request):
    facebook_api_url = (
        "https://graph.facebook.com/v17.0/" + business_id + "/message_templates"
    )
    serializer = MessageTemplateSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        template_name = data.get("template_name")
        header_text = data.get("header_text")
        body_text = data.get("body_text")
        footer_text = data.get("footer_text")

        post_data = json.dumps(
            {
                "name": template_name,
                "category": "MARKETING",
                "language": "en",
                "components": [
                    {
                        "type": "HEADER",
                        "format": "IMAGE",
                        "example": {"header_handle": [header_text]},
                    },
                    {"type": "BODY", "text": body_text},
                    {"type": "FOOTER", "text": footer_text},
                ],
            }
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + bearer_token,
        }

        response = requests.post(facebook_api_url, data=post_data, headers=headers)
        response_data = response.json()

        if response.status_code == status.HTTP_200_OK:
            return Response(
                {"message": response_data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": response_data},
                status=response.status_code,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_text_template_button_site(request):
    facebook_api_url = (
        "https://graph.facebook.com/v17.0/" + business_id + "/message_templates"
    )
    serializer = MessageTemplateSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        template_name = data.get("template_name")
        header_text = data.get("header_text")
        body_text = data.get("body_text")
        footer_text = data.get("footer_text")
        button_type = data.get("button_type")
        button_text = data.get("button_text")
        button_url = data.get("button_url")

        post_data = json.dumps(
            {
                "name": template_name,
                "category": "MARKETING",
                "components": [
                    {"type": "HEADER", "format": "TEXT", "text": header_text},
                    {
                        "type": "BODY",
                        "text": body_text,
                    },
                    {"type": "FOOTER", "text": footer_text},
                    {
                        "type": "BUTTONS",
                        "buttons": [
                            {
                                "type": "URL",
                                "text": button_text,
                                "url": button_url,
                            }
                        ],
                    },
                ],
                "language": "en",
            }
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + bearer_token,
        }

        response = requests.post(facebook_api_url, data=post_data, headers=headers)
        response_data = response.json()

        if response.status_code == status.HTTP_200_OK:
            return Response(
                {"message": response_data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": response_data},
                status=response.status_code,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_text_template_button_call(request):
    facebook_api_url = (
        "https://graph.facebook.com/v17.0/" + business_id + "/message_templates"
    )
    serializer = MessageTemplateSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        template_name = data.get("template_name")
        header_text = data.get("header_text")
        body_text = data.get("body_text")
        footer_text = data.get("footer_text")
        button_type = data.get("button_type")
        button_text = data.get("button_text")
        button_url = data.get("button_url")

        post_data = json.dumps(
            {
                "name": template_name,
                "category": "MARKETING",
                "components": [
                    {"type": "HEADER", "format": "TEXT", "text": header_text},
                    {
                        "type": "BODY",
                        "text": body_text,
                    },
                    {"type": "FOOTER", "text": footer_text},
                    {
                        "type": "BUTTONS",
                        "buttons": [
                            {
                                "type": "PHONE_NUMBER",
                                "text": button_text,
                                "phone_number": button_url,
                            }
                        ],
                    },
                ],
                "language": "en",
            }
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + bearer_token,
        }

        response = requests.post(facebook_api_url, data=post_data, headers=headers)
        response_data = response.json()

        if response.status_code == status.HTTP_200_OK:
            return Response(
                {"message": response_data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": response_data},
                status=response.status_code,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# privacy policy
def privacy(request):
    return JsonResponse(
        {
            "privacy & Policy": "Message FlowsWhen a user sends a message to one of these businesses, the message travels end-to-end encrypted between the user and the Cloud API. As per the Signal protocol, the user and the Cloud API, on behalf of the business, negotiate encryption keys and establish a secure communication channel. WhatsApp cannot access any message content exchanged between users and businesses.Once a message is received by the Cloud API, it gets decrypted and forwarded to the Business. Messages are only temporarily stored by the Cloud API as required to provide the base API functionality.Messages from a business to a user flow on the reverse path. Businesses send messages to Cloud API. The Cloud API service stores the messages temporarily and takes on the task to send the message to the WhatsApp platform. Messages are stored for any necessary retransmissions.All messages are encrypted by the Cloud API before being sent to WhatsApp using the Signal protocol with keys negotiated with the user (recipient).WhatsApp acts as the transport service. It provides the message forwarding software; both client and server. It has no visibility into the messages being sent. It protects the users by detecting unusual messaging patterns (like a business trying to message all users) or collecting spam reports from users.Cloud API, operated by Meta, acts as the intermediary between WhatsApp and the Cloud API businesses. In other words, those businesses have given Cloud API the power to operate on their behalf. Because of this, WhatsApp forwards all message traffic destined for those businesses to Cloud API. WhatsApp also expects to receive from Cloud API all message traffic from those businesses. This is the same client behavior that the On-Premise client has.WhatsApp gives Cloud API metering and billing information for the Cloud API businesses. It does not share any other messaging information.Meta, in providing the WhatsApp Cloud API service, acts as a Data Processor on behalf of the business. In other words, the businesses have requested Meta to provide programmatic access to the WhatsApp platform.Cloud API receives from WhatsApp the messages destined for the businesses that use Cloud API. Cloud API also sends to WhatsApp the messages sent by those businesses. Other parts of Meta (other than Cloud API) do not have access to the Cloud API business communications, including message content and metadata. Meta does not use any Cloud API data for advertising.Stored and Collected DataAll data collected, stored and accessed by Cloud API is controlled and monitored to ensure proper usage and maintain the high level of privacy expected from a WhatsApp client.Information about the businesses, including their phone numbers, business address, contacts, type, etc. is maintained by Meta and the Business Manager product and is subject to the terms of service set by Meta. Cloud API relies on Business Manager and other Meta systems to identify any access to Cloud API on behalf of the business.Messages sent or received via Cloud API are only accessed by Cloud API, no other part of Meta can use this information. Messages have a maximum retention period of 30 days in order to provide the base features and functionality of the Cloud API service; for example, retransmissions. After 30 days, these features and functionality are no longer available.Cloud API does not rely on any information about the user (customer/consumer) the business is communicating with other than the phone number used to identify the account. This information is used to deliver the messages via the WhatsApp client code. User phone numbers are used as sources or destinations of individual messages; as such they are deleted when messages are deleted. No other part of Meta has access to this information. Like the On-Premise client, the WhatsApp client code used by Cloud API collects messaging information about the business as required by WhatsApp. This is information used by WhatsApp to detect malicious activity. No message content is shared or sent to WhatsApp at any time and no WhatsApp employee has access to any message content."
        }
    )


# webhook handle
@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        challenge = request.GET.get("hub.challenge")
        token = request.GET.get("hub.verify_token")

        if mode and token:
            if mode == "subscribe" and token == my_token:
                return HttpResponse(challenge, content_type="text/plain")
            else:
                return HttpResponse(status=403)

    return HttpResponse("OK", content_type="text/plain")


# @csrf_exempt
# def whatsapp_message(request):
#     if request.method == "POST":
#         print("sdhjbcjhdc", request.body.decode("utf-8"))
#         print(json.loads(request.body.decode("utf-8")))
#         try:
#             body_param = json.loads(request.body.decode("utf-8"))

#             if "object" in body_param:
#                 entry = body_param.get("entry")
#                 if (
#                     entry
#                     and entry[0].get("changes")
#                     and entry[0]["changes"][0].get("value")
#                     and entry[0]["changes"][0]["value"].get("messages")
#                 ):
#                     phone_number_id = entry[0]["changes"][0]["value"]["metadata"][
#                         "phone_number_id"
#                     ]
#                     from_user = entry[0]["changes"][0]["value"]["messages"][0]["from"]
#                     msg_body = entry[0]["changes"][0]["value"]["messages"][0]["text"][
#                         "body"
#                     ]

#                     print("phone number", phone_number_id)
#                     print("from", from_user)
#                     print("message body", msg_body)

#                     # Define your Facebook Graph API endpoint
#                     facebook_api_url = (
#                         "https://graph.facebook.com/v13.0/{phone_number_id}/messages"
#                     )

#                     # Create the message payload
#                     message_payload = {
#                         "messaging_product": "whatsapp",
#                         "to": from_user,
#                         "text": {
#                             "body": "Hi.. I'm Prasath, your message is {msg_body}"
#                         },
#                     }

#                     # Send the POST request to the Facebook Graph API
#                     headers = {"Content-Type": "application/json"}
#                     params = {"access_token": token}
#                     response = requests.post(
#                         facebook_api_url,
#                         json=message_payload,
#                         headers=headers,
#                         params=params,
#                     )

#                     if response.status_code == 200:
#                         return HttpResponse(status=200)
#                     else:
#                         return HttpResponse(status=500)
#         except json.JSONDecodeError as e:
#             return HttpResponse(
#                 "Invalid JSON data", content_type="text/plain", status=400
#             )


# sent individual message
# @csrf_exempt
# @require_POST
# def send_whatsapp_message(request):
#     try:
#         post_data = json.loads(request.body.decode("utf-8"))
#         to = post_data.get("name")
#         # print("Received 'to' parameter: ", to)

#         PhoneNumber.objects.get_or_create(number=to)

#         if not to:
#             return JsonResponse({"error": "Missing 'to' parameter"}, status=400)

#         data = {
#             "messaging_product": "whatsapp",
#             "recipient_type": "individual",
#             "to": to,
#             "type": "template",
#             "template": {"name": "developer_test", "language": {"code": "en"}},
#         }

#         url = "https://graph.facebook.com/v17.0/123004784227116/messages"
#         headers = {
#             "Authorization": "Bearer "
#             + bearer_token,  # Include the Bearer token in the headers
#             "Content-Type": "application/json",
#         }
#         # print(headers)

#         response = requests.post(url, headers=headers, json=data)
#         response_data = response.json()
#         return JsonResponse(response_data, status=response.status_code)

#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON data"}, status=400)
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({"error": str(e)}, status=500)
