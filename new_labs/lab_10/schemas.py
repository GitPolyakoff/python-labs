from exceptions import ValidationError

def validate_account_data(data: dict, partial: bool = False):
    required_fields = ["client_name", "currency", "balance", "status"]
    
    if not partial:
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Отсутствует обязательное поле: {field}")
                
    if "balance" in data and data["balance"] < 0:
        raise ValidationError("Баланс не может быть отрицательным")
        
    if "client_name" in data and not str(data["client_name"]).strip():
        raise ValidationError("Имя клиента не может быть пустым")
        
    if "status" in data and data["status"] not in ["active", "blocked", "closed"]:
        raise ValidationError("Неверный статус счета")