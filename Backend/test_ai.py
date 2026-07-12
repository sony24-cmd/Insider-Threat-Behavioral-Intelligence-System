from services.ai_service import predict_risk

result = predict_risk(
    login_count=5,
    logout_count=5,
    usb_connect=3,
    usb_disconnect=3,
    http_visits=12,
    total_events=25,
)

print(result)